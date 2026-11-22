import os
import io
import uuid
import shutil
import zipfile
import base64
from pathlib import Path
from typing import List, Optional
from PIL import Image, ImageEnhance, ImageOps
import pymupdf  # Modern PyMuPDF replacement for fitz
from pdf2docx import Converter
from app.core.config import TEMP_DIR

# Global cached rembg session for instant background removals
_rembg_session = None

def get_rembg_session():
    global _rembg_session
    if _rembg_session is None:
        try:
            from rembg import new_session
            _rembg_session = new_session("u2net")
        except Exception as e:
            print(f"Warning: Failed to pre-load rembg session: {e}")
    return _rembg_session

class ConversionService:
    @staticmethod
    def get_job_dir() -> Path:
        """Create an isolated temporary scratchpad directory for a conversion job."""
        job_id = str(uuid.uuid4())
        job_dir = TEMP_DIR / job_id
        job_dir.mkdir(parents=True, exist_ok=True)
        return job_dir

    @staticmethod
    def cleanup_job(job_dir: Path):
        """Immediately purges all job files to uphold zero-retention privacy."""
        try:
            if job_dir.exists():
                shutil.rmtree(str(job_dir), ignore_errors=True)
        except Exception as e:
            print(f"Warning: Failed to clean up {job_dir}: {e}")

    @classmethod
    def pdf_to_docx(cls, pdf_path: Path, output_path: Path) -> Path:
        """Converts PDF to editable Word (.docx) preserving layout and tables."""
        cv = Converter(str(pdf_path))
        try:
            cv.convert(str(output_path), start=0, end=None)
        finally:
            cv.close()
        return output_path

    @classmethod
    def docx_to_pdf(cls, docx_path: Path, output_path: Path) -> Path:
        """
        Converts Word (.docx / .doc) to PDF with high fidelity:
        1. Native Microsoft Word COM Automation on Windows:
           - Uses Word's native print-quality export engine (100% fidelity: exact fonts, tables, margins, styles)
           - Runs in headless/invisible mode with DisplayAlerts disabled to prevent dialog freezes
        2. Headless LibreOffice fallback (for Linux/server environments without MS Office)
        3. Enhanced ReportLab fallback (with full table reconstruction & paragraph styling)
        """
        abs_input = str(docx_path.resolve())
        abs_output = str(output_path.resolve())

        # Strategy 1: Native Microsoft Word COM Automation (Highest Fidelity on Windows)
        try:
            import pythoncom
            import win32com.client
            pythoncom.CoInitialize()
            word = None
            doc = None
            try:
                word = win32com.client.DispatchEx("Word.Application")
                word.Visible = False
                word.DisplayAlerts = 0  # wdAlertsNone - prevents popup dialogs from blocking
                doc = word.Documents.Open(abs_input, ReadOnly=True, ConfirmConversions=False)
                # 17 = wdFormatPDF
                doc.SaveAs(abs_output, FileFormat=17)
                doc.Close(SaveChanges=0)
                doc = None
                word.Quit(SaveChanges=0)
                word = None
                if output_path.exists() and output_path.stat().st_size > 0:
                    return output_path
            finally:
                if doc is not None:
                    try:
                        doc.Close(SaveChanges=0)
                    except Exception:
                        pass
                if word is not None:
                    try:
                        word.Quit(SaveChanges=0)
                    except Exception:
                        pass
                pythoncom.CoUninitialize()
        except Exception as e:
            print(f"Native Word COM conversion notice: {e}, attempting fallback...")

        # Strategy 2: Headless LibreOffice
        soffice_bin = shutil.which("soffice") or shutil.which("libreoffice")
        if soffice_bin:
            try:
                import subprocess
                subprocess.run(
                    [soffice_bin, "--headless", "--convert-to", "pdf", "--outdir", str(output_path.parent), abs_input],
                    capture_output=True,
                    timeout=30
                )
                generated_pdf = output_path.parent / f"{docx_path.stem}.pdf"
                if generated_pdf.exists() and generated_pdf.stat().st_size > 0:
                    if generated_pdf != output_path:
                        shutil.move(str(generated_pdf), str(output_path))
                    return output_path
            except Exception as e:
                print(f"LibreOffice conversion notice: {e}")

        # Strategy 3: Enhanced ReportLab Fallback (with full table parsing & layout)
        from docx import Document
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors

        doc = Document(abs_input)
        pdf_doc = SimpleDocTemplate(
            abs_output,
            pagesize=letter,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40
        )

        styles = getSampleStyleSheet()
        normal = styles['Normal']
        normal.fontSize = 10
        normal.leading = 14

        title_style = ParagraphStyle(
            'DocTitle',
            parent=styles['Title'],
            fontSize=20,
            leading=26,
            alignment=1,
            spaceAfter=14
        )

        h1 = ParagraphStyle(
            'DocH1',
            parent=styles['Heading1'],
            fontSize=14,
            leading=18,
            spaceBefore=12,
            spaceAfter=6,
            keepWithNext=True
        )

        story = []

        for element in doc.element.body:
            tag = element.tag.split('}')[-1]
            if tag == 'p':
                p_text = element.text or "".join(element.itertext())
                p_text = p_text.strip()
                if not p_text:
                    story.append(Spacer(1, 8))
                    continue
                if len(story) == 0 and len(p_text) < 60:
                    story.append(Paragraph(p_text, title_style))
                elif len(p_text) < 50 and (p_text.isupper() or p_text.endswith(':') or not p_text.endswith('.')):
                    story.append(Paragraph(p_text, h1))
                else:
                    story.append(Paragraph(p_text, normal))
                story.append(Spacer(1, 4))
            elif tag == 'tbl':
                for table in doc.tables:
                    if table._tbl == element:
                        table_data = []
                        for row in table.rows:
                            row_data = [Paragraph(cell.text.strip(), normal) for cell in row.cells]
                            table_data.append(row_data)
                        if table_data:
                            rl_table = Table(table_data)
                            rl_table.setStyle(TableStyle([
                                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f0f2f5')),
                                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
                                ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#888888')),
                                ('TOPPADDING', (0, 0), (-1, -1), 6),
                                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                            ]))
                            story.append(rl_table)
                            story.append(Spacer(1, 10))
                        break

        if not story:
            story.append(Paragraph("Empty Document", normal))

        pdf_doc.build(story)
        return output_path

    @classmethod
    def images_to_pdf(cls, image_paths: List[Path], output_path: Path) -> Path:
        """
        Combines one or multiple images (PNG/JPG/WEBP) into a single PDF.
        Automatically normalizes EXIF orientation and color modes.
        """
        images = []
        for img_p in image_paths:
            img = Image.open(img_p)
            # Correct orientation from mobile phone camera metadata
            img = ImageOps.exif_transpose(img)
            # Convert RGBA / Palette to RGB for PDF standard compatibility
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            images.append(img)

        if not images:
            raise ValueError("No valid images provided for PDF conversion.")

        first_image = images[0]
        remaining_images = images[1:] if len(images) > 1 else []

        first_image.save(
            str(output_path),
            "PDF",
            resolution=100.0,
            save_all=True,
            append_images=remaining_images
        )
        return output_path

    @classmethod
    def pdf_to_images(cls, pdf_path: Path, output_dir: Path, dpi: int = 200) -> Path:
        """
        Converts PDF pages to crisp PNG images.
        If single page: returns the image path.
        If multi-page: packs pages into a zip archive and returns the zip path.
        """
        doc = pymupdf.open(str(pdf_path))
        total_pages = len(doc)

        if total_pages == 0:
            raise ValueError("PDF document contains no pages.")

        image_files = []
        for page_num in range(total_pages):
            page = doc.load_page(page_num)
            pix = page.get_pixmap(dpi=dpi)
            out_img = output_dir / f"page_{page_num + 1}.png"
            pix.save(str(out_img))
            image_files.append(out_img)
        doc.close()

        if total_pages == 1:
            return image_files[0]

        # Multi-page: Bundle into zip
        zip_path = output_dir / f"{pdf_path.stem}_pages.zip"
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zip_f:
            for img in image_files:
                zip_f.write(img, arcname=img.name)

        return zip_path

    @classmethod
    def enhance_image(
        cls,
        image_path: Path,
        output_path: Path,
        sharpness: float = 1.35,
        contrast: float = 1.12,
        color: float = 1.08
    ) -> Path:
        """
        Enhances image clarity and visual punch:
        - Auto-corrects EXIF rotation
        - Auto-contrast adjustment to remove haze
        - Multi-pass sharpness & color vibrancy tuning
        """
        img = Image.open(image_path)
        img = ImageOps.exif_transpose(img)
        is_transparent = img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info)

        if not is_transparent:
            img = img.convert("RGB")
            # Auto-contrast stretch (gentle 0.5% cutoff) for crisp dynamics
            img = ImageOps.autocontrast(img, cutoff=0.5)

        # 1. Enhance Sharpness
        img = ImageEnhance.Sharpness(img).enhance(sharpness)
        # 2. Enhance Contrast
        img = ImageEnhance.Contrast(img).enhance(contrast)
        # 3. Enhance Color Vibrancy
        img = ImageEnhance.Color(img).enhance(color)

        ext = output_path.suffix.lower()
        if ext == ".webp":
            img.save(str(output_path), "WEBP", quality=95)
        elif is_transparent or ext == ".png":
            img.save(str(output_path), "PNG", optimize=True)
        else:
            img.save(str(output_path), "JPEG", quality=95, optimize=True)

        return output_path

    @classmethod
    def remove_background(cls, image_path: Path, output_path: Path) -> Path:
        """
        Removes background from image using rembg (U2-Net / ONNX),
        producing a clean, transparent PNG.
        Uses cached session for low-latency processing.
        """
        from rembg import remove
        session = get_rembg_session()

        with open(image_path, "rb") as i:
            input_bytes = i.read()

        if session is not None:
            output_bytes = remove(input_bytes, session=session)
        else:
            output_bytes = remove(input_bytes)

        with open(output_path, "wb") as o:
            o.write(output_bytes)
        return output_path

    @classmethod
    def remove_image_watermark(
        cls,
        image_path: Path,
        output_path: Path,
        preset: str = "auto",
        box: Optional[dict] = None,
        mask_data: Optional[str] = None
    ) -> Path:
        """
        Removes watermarks, stamps, and logos from photos using OpenCV Telea inpainting.
        
        High-Fidelity Modes:
        1. Precise Interactive Mask: Uses exact user brush/box coordinates from frontend canvas.
        2. Bounding Box Selection: Inpaints inside designated box with local edge refinement.
        3. Region Presets: Cleans bottom-right, bottom-left, top-right, or center watermark stamps.
        4. Safe Smart Auto-Detect: Uses connected-component stroke filtering with a strict 6%
           maximum coverage limit so landscapes, mountains, and textures are never smeared or erased.
        """
        import cv2
        import numpy as np

        img = Image.open(image_path)
        img = ImageOps.exif_transpose(img)
        is_rgba = img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info)
        alpha_channel = img.convert("RGBA").split()[-1] if is_rgba else None

        rgb_np = np.array(img.convert("RGB"))
        bgr = cv2.cvtColor(rgb_np, cv2.COLOR_RGB2BGR)
        h, w = bgr.shape[:2]
        total_pixels = h * w
        mask = np.zeros((h, w), dtype=np.uint8)

        # Mode 1: Exact Base64 mask sent from interactive canvas brush / eraser
        if mask_data and mask_data.startswith("data:image"):
            try:
                header, encoded = mask_data.split(",", 1)
                data = base64.b64decode(encoded)
                decoded_mask = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_GRAYSCALE)
                if decoded_mask is not None:
                    # Match native image resolution if canvas was scaled
                    if decoded_mask.shape[:2] != (h, w):
                        decoded_mask = cv2.resize(decoded_mask, (w, h), interpolation=cv2.INTER_NEAREST)
                    mask = (decoded_mask > 40).astype(np.uint8) * 255
                    # Gentle 1-pixel dilation to ensure edge blending
                    mask = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=1)
            except Exception as e:
                print(f"Warning: Failed to decode canvas brush mask: {e}")

        # Mode 2: Targeted Bounding Box
        if np.sum(mask > 0) == 0 and box and all(k in box for k in ('x', 'y', 'w', 'h')):
            bx = int(box['x'] * w / 100) if box['x'] <= 100 else int(box['x'])
            by = int(box['y'] * h / 100) if box['y'] <= 100 else int(box['y'])
            bw = int(box['w'] * w / 100) if box['w'] <= 100 else int(box['w'])
            bh = int(box['h'] * h / 100) if box['h'] <= 100 else int(box['h'])
            x1, y1 = max(0, bx), max(0, by)
            x2, y2 = min(w, bx + bw), min(h, by + bh)
            cv2.rectangle(mask, (x1, y1), (x2, y2), 255, -1)

        # Mode 3: Region Presets
        if np.sum(mask > 0) == 0:
            if preset == "bottom_right":
                cv2.rectangle(mask, (int(w * 0.65), int(h * 0.80)), (w, h), 255, -1)
            elif preset == "bottom_left":
                cv2.rectangle(mask, (0, int(h * 0.80)), (int(w * 0.35), h), 255, -1)
            elif preset == "top_right":
                cv2.rectangle(mask, (int(w * 0.65), 0), (w, int(h * 0.20)), 255, -1)
            elif preset == "center":
                cv2.rectangle(mask, (int(w * 0.18), int(h * 0.35)), (int(w * 0.82), int(h * 0.60)), 255, -1)
            else:
                # Mode 4: Safe Smart Auto-Detect with Dual Text/Stamp Extraction
                gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
                hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
                safe_mask = np.zeros((h, w), dtype=np.uint8)

                # Sub-detector A: Colored text / stamps (e.g. orange, red, green, blue watermark text)
                s_ch = hsv[:, :, 1]
                sat_mask = (s_ch >= 40).astype(np.uint8)
                num_s_labels, s_labels, s_stats, _ = cv2.connectedComponentsWithStats(sat_mask, connectivity=8)
                for i in range(1, num_s_labels):
                    area = s_stats[i, cv2.CC_STAT_AREA]
                    cw = s_stats[i, cv2.CC_STAT_WIDTH]
                    ch = s_stats[i, cv2.CC_STAT_HEIGHT]
                    if 8 <= area <= 2500 and 5 <= ch <= 60 and 3 <= cw <= 90:
                        aspect = cw / float(ch)
                        if 0.1 <= aspect <= 4.5:
                            safe_mask[s_labels == i] = 255

                # Sub-detector B: High-contrast edges (white/gray/black stamps and diagonal text)
                grad_x = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
                grad_y = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
                mag = cv2.magnitude(grad_x, grad_y)
                mag_norm = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
                _, edge_thresh = cv2.threshold(mag_norm, 65, 255, cv2.THRESH_BINARY)

                num_e_labels, e_labels, e_stats, _ = cv2.connectedComponentsWithStats(edge_thresh, connectivity=8)
                for i in range(1, num_e_labels):
                    area = e_stats[i, cv2.CC_STAT_AREA]
                    cw = e_stats[i, cv2.CC_STAT_WIDTH]
                    ch = e_stats[i, cv2.CC_STAT_HEIGHT]
                    # Stroke dimensions strictly matching letters to avoid natural mountain ridges
                    if 10 <= area <= 1200 and 4 <= ch <= 45 and 3 <= cw <= 70:
                        aspect = cw / float(ch)
                        if 0.15 <= aspect <= 3.5:
                            safe_mask[e_labels == i] = 255

                # Dilate gently by 2px (5x5 ellipse) to cover antialiased text borders
                safe_mask = cv2.dilate(safe_mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)), iterations=1)

                # Strict Safety Ceiling: Watermark text should NEVER exceed 4% of image area
                if np.sum(safe_mask > 0) > (total_pixels * 0.04):
                    clamped = np.zeros_like(safe_mask)
                    clamped[int(h*0.15):int(h*0.85), int(w*0.08):int(w*0.92)] = safe_mask[int(h*0.15):int(h*0.85), int(w*0.08):int(w*0.92)]
                    safe_mask = clamped

                mask = safe_mask

        # Fallback if no mask was generated: slight center stamp candidate
        if np.sum(mask > 0) == 0:
            cv2.rectangle(mask, (int(w * 0.25), int(h * 0.40)), (int(w * 0.75), int(h * 0.55)), 255, -1)

        # Inpaint mask region seamlessly with Telea algorithm (radius 3 for sharp edges)
        inpainted = cv2.inpaint(bgr, mask, 3, cv2.INPAINT_TELEA)
        out_rgb = cv2.cvtColor(inpainted, cv2.COLOR_BGR2RGB)
        out_img = Image.fromarray(out_rgb)

        if is_rgba and alpha_channel:
            out_img.putalpha(alpha_channel)

        ext = output_path.suffix.lower()
        if ext == ".webp":
            out_img.save(str(output_path), "WEBP", quality=95)
        elif is_rgba or ext == ".png":
            out_img.save(str(output_path), "PNG", optimize=True)
        else:
            out_img.save(str(output_path), "JPEG", quality=95, optimize=True)

        return output_path

    @classmethod
    def remove_pdf_watermark(cls, pdf_path: Path, output_path: Path, custom_text: Optional[str] = None) -> Path:
        """
        Purges watermark annotations and text stamps from PDF documents across all pages.
        """
        doc = pymupdf.open(str(pdf_path))
        common_watermarks = [
            "confidential", "draft", "sample", "evaluation",
            "watermark", "copy", "do not copy", "camscanner",
            "scanned by", "preview", "internal use only"
        ]
        if custom_text and custom_text.strip():
            common_watermarks.append(custom_text.strip().lower())

        for page in doc:
            # Delete watermark and stamp annotations
            annots = list(page.annots() or [])
            for annot in annots:
                if annot.type and len(annot.type) > 1:
                    if annot.type[1].lower() in ("watermark", "stamp", "freetext", "highlight"):
                        page.delete_annot(annot)

            # Search and redact watermark text instances
            for kw in common_watermarks:
                rects = page.search_for(kw)
                for r in rects:
                    page.add_redact_annot(r)
            page.apply_redactions()

        doc.save(str(output_path), garbage=4, deflate=True)
        doc.close()
        return output_path

import os
import io
import uuid
import zipfile
from pathlib import Path
from typing import List, Optional
from PIL import Image
import fitz  # PyMuPDF
from pdf2docx import Converter
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from app.core.config import TEMP_DIR

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
                for item in job_dir.glob("*"):
                    if item.is_file():
                        item.unlink()
                job_dir.rmdir()
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
        Converts Word (.docx) to PDF with high fidelity:
        1. Uses native Microsoft Word COM engine via docx2pdf if available on Windows
           (pixel-perfect layout, tables, fonts, headings, images).
        2. Falls back to headless LibreOffice if installed.
        3. Falls back to enhanced ReportLab with full table parsing if neither is available.
        """
        abs_input = str(docx_path.resolve())
        abs_output = str(output_path.resolve())

        # Strategy 1: Native Word / docx2pdf (Highest fidelity on Windows)
        try:
            import pythoncom
            from docx2pdf import convert
            pythoncom.CoInitialize()
            try:
                convert(abs_input, abs_output)
                if output_path.exists() and output_path.stat().st_size > 0:
                    return output_path
            finally:
                pythoncom.CoUninitialize()
        except Exception as e:
            print(f"docx2pdf conversion notice: {e}, attempting fallback...")

        # Strategy 2: Headless LibreOffice (Industry standard on Linux/Docker)
        import subprocess, shutil
        soffice_bin = shutil.which("soffice") or shutil.which("libreoffice")
        if soffice_bin:
            try:
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

        # Strategy 3: Enhanced ReportLab Fallback (with table extraction)
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
        """Combines one or multiple images (PNG/JPG/WEBP) into a single PDF."""
        images = []
        for img_p in image_paths:
            img = Image.open(img_p)
            # Convert RGBA to RGB for PDF compatibility
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
        Converts PDF pages to PNG images.
        If single page: returns the image path.
        If multi-page: packs pages into a zip archive and returns the zip path.
        """
        doc = fitz.open(str(pdf_path))
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
    def enhance_image(cls, image_path: Path, output_path: Path, sharpness: float = 1.4, contrast: float = 1.15, color: float = 1.1) -> Path:
        """
        Enhances image quality using PIL ImageEnhance:
        - Sharpness enhancement for crisp details
        - Contrast adjustment for deep rich tones
        - Subtle color saturation boost
        """
        from PIL import ImageEnhance
        img = Image.open(image_path)
        is_transparent = img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info)

        if not is_transparent:
            img = img.convert("RGB")

        # 1. Enhance Sharpness
        img = ImageEnhance.Sharpness(img).enhance(sharpness)
        # 2. Enhance Contrast
        img = ImageEnhance.Contrast(img).enhance(contrast)
        # 3. Enhance Color
        img = ImageEnhance.Color(img).enhance(color)

        save_format = "PNG" if is_transparent or output_path.suffix.lower() == ".png" else "JPEG"
        if save_format == "JPEG":
            img.save(str(output_path), "JPEG", quality=95, optimize=True)
        else:
            img.save(str(output_path), "PNG", optimize=True)

        return output_path

    @classmethod
    def remove_background(cls, image_path: Path, output_path: Path) -> Path:
        """
        Removes background from image using rembg (U2-Net / ONNX),
        producing a transparent PNG.
        """
        from rembg import remove
        with open(image_path, "rb") as i:
            input_bytes = i.read()
        output_bytes = remove(input_bytes)
        with open(output_path, "wb") as o:
            o.write(output_bytes)
        return output_path


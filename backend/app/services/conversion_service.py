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
        Converts Word (.docx) to PDF.
        Extracts formatted paragraphs and styles using python-docx and builds
        a clean, portable PDF via ReportLab.
        """
        doc = Document(str(docx_path))
        pdf_doc = SimpleDocTemplate(
            str(output_path),
            pagesize=letter,
            rightMargin=54,
            leftMargin=54,
            topMargin=54,
            bottomMargin=54
        )

        styles = getSampleStyleSheet()
        normal_style = styles['Normal']
        heading1_style = styles['Heading1']
        heading2_style = styles['Heading2']

        story = []
        for paragraph in doc.paragraphs:
            text = paragraph.text.strip()
            if not text:
                story.append(Spacer(1, 10))
                continue

            # Map common heading styles
            style_name = paragraph.style.name.lower()
            if 'heading 1' in style_name:
                story.append(Paragraph(text, heading1_style))
            elif 'heading 2' in style_name:
                story.append(Paragraph(text, heading2_style))
            else:
                story.append(Paragraph(text, normal_style))
            story.append(Spacer(1, 6))

        if not story:
            story.append(Paragraph("Empty Document", normal_style))

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

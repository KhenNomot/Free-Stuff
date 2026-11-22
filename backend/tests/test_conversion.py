import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image
from app.services.conversion_service import ConversionService

def test_full_conversion_pipeline():
    test_dir = Path(__file__).parent / "test_scratch"
    test_dir.mkdir(parents=True, exist_ok=True)

    print("--- 1. Testing Image to PDF ---")
    img_path = test_dir / "sample.png"
    img = Image.new("RGB", (300, 300), color="blue")
    img.save(img_path)

    pdf_from_img = test_dir / "from_img.pdf"
    ConversionService.images_to_pdf([img_path], pdf_from_img)
    assert pdf_from_img.exists() and pdf_from_img.stat().st_size > 0
    print(f"✅ Created PDF from image: {pdf_from_img.stat().st_size} bytes")

    print("\n--- 2. Testing PDF Generation & PDF to Images ---")
    sample_pdf = test_dir / "document.pdf"
    c = canvas.Canvas(str(sample_pdf), pagesize=letter)
    c.drawString(100, 750, "FreeShits File Conversion Engine")
    c.drawString(100, 720, "Testing automated pipeline fidelity and layout extraction.")
    c.showPage()
    c.save()

    extracted_img = ConversionService.pdf_to_images(sample_pdf, test_dir)
    assert extracted_img.exists() and extracted_img.stat().st_size > 0
    print(f"✅ Extracted image from PDF: {extracted_img.name}")

    print("\n--- 3. Testing PDF to Word (.docx) ---")
    output_docx = test_dir / "converted.docx"
    ConversionService.pdf_to_docx(sample_pdf, output_docx)
    assert output_docx.exists() and output_docx.stat().st_size > 0
    print(f"✅ Converted PDF to DOCX: {output_docx.stat().st_size} bytes")

    print("\n--- 4. Testing Word (.docx) to PDF ---")
    output_pdf_from_doc = test_dir / "from_docx.pdf"
    ConversionService.docx_to_pdf(output_docx, output_pdf_from_doc)
    assert output_pdf_from_doc.exists() and output_pdf_from_doc.stat().st_size > 0
    print(f"✅ Converted DOCX back to PDF: {output_pdf_from_doc.stat().st_size} bytes")

    # Clean up test scratch
    for item in test_dir.glob("*"):
        if item.is_file():
            item.unlink()
    test_dir.rmdir()
    print("\n🎉 ALL CONVERSION PIPELINE TESTS PASSED!")

if __name__ == "__main__":
    test_full_conversion_pipeline()

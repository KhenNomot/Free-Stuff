import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import cv2
import numpy as np
import pymupdf
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

    print("\n--- 5. Testing Image Enhancer ---")
    enhanced_img = test_dir / "enhanced.png"
    ConversionService.enhance_image(img_path, enhanced_img)
    assert enhanced_img.exists() and enhanced_img.stat().st_size > 0
    print(f"✅ Enhanced Image created: {enhanced_img.stat().st_size} bytes")

    print("\n--- 6. Testing Background Removal ---")
    no_bg_img = test_dir / "no_bg.png"
    ConversionService.remove_background(img_path, no_bg_img)
    assert no_bg_img.exists() and no_bg_img.stat().st_size > 0
    print(f"✅ Background Removed image created: {no_bg_img.stat().st_size} bytes")

    print("\n--- 7. Testing Image Watermark Removal ---")
    wm_img_path = test_dir / "watermarked.png"
    # Create image with watermark text in bottom right
    base_img = np.zeros((300, 450, 3), dtype=np.uint8)
    base_img[:] = [150, 190, 230]
    cv2.putText(base_img, "STOCK WATERMARK", (250, 270), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    Image.fromarray(cv2.cvtColor(base_img, cv2.COLOR_BGR2RGB)).save(wm_img_path)

    clean_img_path = test_dir / "cleaned_image.png"
    ConversionService.remove_image_watermark(wm_img_path, clean_img_path, preset="bottom_right")
    assert clean_img_path.exists() and clean_img_path.stat().st_size > 0
    print(f"✅ Watermark removed from image: {clean_img_path.stat().st_size} bytes")

    print("\n--- 8. Testing PDF Watermark Removal ---")
    wm_pdf_path = test_dir / "watermarked.pdf"
    doc_wm = pymupdf.open()
    p = doc_wm.new_page()
    p.insert_text((50, 100), "Important Clean Financial Report", fontsize=16)
    p.insert_text((150, 300), "CONFIDENTIAL DRAFT", fontsize=28, color=(0.8, 0.8, 0.8))
    doc_wm.save(str(wm_pdf_path))
    doc_wm.close()

    clean_pdf_path = test_dir / "cleaned_doc.pdf"
    ConversionService.remove_pdf_watermark(wm_pdf_path, clean_pdf_path, custom_text="confidential")
    assert clean_pdf_path.exists() and clean_pdf_path.stat().st_size > 0

    doc_ver = pymupdf.open(str(clean_pdf_path))
    remaining_text = doc_ver[0].get_text()
    doc_ver.close()
    assert "CONFIDENTIAL" not in remaining_text
    assert "Financial Report" in remaining_text
    print(f"✅ Watermark removed from PDF: {clean_pdf_path.stat().st_size} bytes (CONFIDENTIAL purged)")

    # Clean up test scratch
    for item in test_dir.glob("*"):
        if item.is_file():
            item.unlink()
    test_dir.rmdir()
    print("\n🎉 ALL 8 CONVERSION & UTILITY PIPELINE TESTS PASSED!")

if __name__ == "__main__":
    test_full_conversion_pipeline()

import shutil
from pathlib import Path
from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks, status
from fastapi.responses import FileResponse
from app.core.config import MAX_FILE_SIZE_BYTES
from app.services.conversion_service import ConversionService

router = APIRouter(prefix="/api/convert", tags=["Conversions"])

def validate_file_size(file: UploadFile):
    """Enforce maximum upload limit."""
    file.file.seek(0, 2)
    size = file.file.tell()
    file.file.seek(0)
    if size > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File exceeds maximum allowed limit of {MAX_FILE_SIZE_BYTES // (1024*1024)}MB."
        )
    return size

@router.post("/pdf-to-docx")
def convert_pdf_to_docx(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only .pdf files are supported for this conversion.")
    
    validate_file_size(file)
    job_dir = ConversionService.get_job_dir()
    input_pdf = job_dir / file.filename
    output_docx = job_dir / f"{Path(file.filename).stem}.docx"

    with open(input_pdf, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        ConversionService.pdf_to_docx(input_pdf, output_docx)
    except Exception as e:
        ConversionService.cleanup_job(job_dir)
        raise HTTPException(status_code=500, detail=f"Conversion error: {str(e)}")

    background_tasks.add_task(ConversionService.cleanup_job, job_dir)

    return FileResponse(
        path=output_docx,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=output_docx.name
    )

@router.post("/docx-to-pdf")
def convert_docx_to_pdf(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    if not file.filename.lower().endswith((".docx", ".doc")):
        raise HTTPException(status_code=400, detail="Only .docx/.doc files are supported for this conversion.")

    validate_file_size(file)
    job_dir = ConversionService.get_job_dir()
    input_docx = job_dir / file.filename
    output_pdf = job_dir / f"{Path(file.filename).stem}.pdf"

    with open(input_docx, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        ConversionService.docx_to_pdf(input_docx, output_pdf)
    except Exception as e:
        ConversionService.cleanup_job(job_dir)
        raise HTTPException(status_code=500, detail=f"Conversion error: {str(e)}")

    background_tasks.add_task(ConversionService.cleanup_job, job_dir)

    return FileResponse(
        path=output_pdf,
        media_type="application/pdf",
        filename=output_pdf.name
    )

@router.post("/images-to-pdf")
def convert_images_to_pdf(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...)
):
    if not files:
        raise HTTPException(status_code=400, detail="At least one image file is required.")

    job_dir = ConversionService.get_job_dir()
    saved_images = []

    for f in files:
        if not f.filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
            ConversionService.cleanup_job(job_dir)
            raise HTTPException(status_code=400, detail=f"File {f.filename} is not a supported image format.")
        
        validate_file_size(f)
        img_path = job_dir / f.filename
        with open(img_path, "wb") as buffer:
            shutil.copyfileobj(f.file, buffer)
        saved_images.append(img_path)

    output_pdf = job_dir / "converted_images.pdf"

    try:
        ConversionService.images_to_pdf(saved_images, output_pdf)
    except Exception as e:
        ConversionService.cleanup_job(job_dir)
        raise HTTPException(status_code=500, detail=f"Image conversion error: {str(e)}")

    background_tasks.add_task(ConversionService.cleanup_job, job_dir)

    return FileResponse(
        path=output_pdf,
        media_type="application/pdf",
        filename="converted_images.pdf"
    )

@router.post("/pdf-to-images")
def convert_pdf_to_images(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only .pdf files are supported for this conversion.")

    validate_file_size(file)
    job_dir = ConversionService.get_job_dir()
    input_pdf = job_dir / file.filename

    with open(input_pdf, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        result_path = ConversionService.pdf_to_images(input_pdf, job_dir)
    except Exception as e:
        ConversionService.cleanup_job(job_dir)
        raise HTTPException(status_code=500, detail=f"Extraction error: {str(e)}")

    background_tasks.add_task(ConversionService.cleanup_job, job_dir)

    media_type = "application/zip" if result_path.suffix == ".zip" else "image/png"
    return FileResponse(
        path=result_path,
        media_type=media_type,
        filename=result_path.name
    )

@router.post("/enhance-image")
def enhance_image_endpoint(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    if not file.filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
        raise HTTPException(status_code=400, detail="Only image files (.png, .jpg, .webp) are supported.")

    validate_file_size(file)
    job_dir = ConversionService.get_job_dir()
    input_img = job_dir / file.filename
    output_img = job_dir / f"enhanced_{file.filename}"

    with open(input_img, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        ConversionService.enhance_image(input_img, output_img)
    except Exception as e:
        ConversionService.cleanup_job(job_dir)
        raise HTTPException(status_code=500, detail=f"Image enhancement error: {str(e)}")

    background_tasks.add_task(ConversionService.cleanup_job, job_dir)

    media_type = "image/png" if output_img.suffix.lower() == ".png" else "image/jpeg"
    return FileResponse(
        path=output_img,
        media_type=media_type,
        filename=output_img.name
    )

@router.post("/remove-bg")
def remove_bg_endpoint(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    if not file.filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
        raise HTTPException(status_code=400, detail="Only image files (.png, .jpg, .webp) are supported.")

    validate_file_size(file)
    job_dir = ConversionService.get_job_dir()
    input_img = job_dir / file.filename
    output_png = job_dir / f"{Path(file.filename).stem}_no_bg.png"

    with open(input_img, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        ConversionService.remove_background(input_img, output_png)
    except Exception as e:
        ConversionService.cleanup_job(job_dir)
        raise HTTPException(status_code=500, detail=f"Background removal error: {str(e)}")

    background_tasks.add_task(ConversionService.cleanup_job, job_dir)

    return FileResponse(
        path=output_png,
        media_type="image/png",
        filename=output_png.name
    )

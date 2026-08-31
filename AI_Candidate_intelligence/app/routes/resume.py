import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.resume_parser import extract_text_from_pdf


router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)


UPLOAD_FOLDER = "uploads"


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF resumes are supported"
        )

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    extracted_text = extract_text_from_pdf(file_path)

    if not extracted_text:
        raise HTTPException(
            status_code=400,
            detail="Could not extract text from resume"
        )

    return {
        "message": "Resume uploaded successfully",
        "filename": file.filename,
        "text_length": len(extracted_text),
        "extracted_text": extracted_text
    }
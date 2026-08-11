import os
import shutil

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.utils.document_loader import extract_text
from app.utils.text_processor import clean_text, chunk_text
from app.utils.vector_store import store_chunks


router = APIRouter()

UPLOAD_DIR = "data/uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload-jd")
async def upload_job_description(file: UploadFile = File(...)):

    allowed_extensions = [".pdf", ".docx", ".txt"]

    file_extension = os.path.splitext(file.filename)[1].lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, DOCX and TXT files are supported."
        )

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # 1. Extract text
        extracted_text = extract_text(file_path)

        if not extracted_text.strip():
            raise HTTPException(
                status_code=400,
                detail="No text could be extracted from the document."
            )

        # 2. Clean text
        cleaned_text = clean_text(extracted_text)

        # 3. Create chunks
        chunks = chunk_text(cleaned_text)

        # 4. Store chunks in ChromaDB
        stored_chunks = store_chunks(
            chunks,
            file.filename
        )

        return {
            "message": "Job description processed and stored successfully",
            "filename": file.filename,
            "characters": len(cleaned_text),
            "chunks_count": len(chunks),
            "stored_chunks": stored_chunks
        }

    except Exception as e:

        if os.path.exists(file_path):
            os.remove(file_path)

        raise HTTPException(
            status_code=500,
            detail=f"Failed to process document: {str(e)}"
        )
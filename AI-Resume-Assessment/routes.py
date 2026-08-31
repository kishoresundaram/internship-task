import os

import fitz

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.services.matching import extract_skills

from app.services.embedding import (
    create_collection,
    store_resume_embedding,
    search_similar_resumes
)

from app.db.database import get_db

from app.models.resume import Resume
from app.models.job import JobDescription


router = APIRouter()

UPLOAD_DIR = "uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


# ============================================================
# Resume Upload
# ============================================================

@router.post("/resume/upload")
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    # --------------------------------------------------------
    # Check file type
    # --------------------------------------------------------

    if not file.filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    # --------------------------------------------------------
    # Create file path
    # --------------------------------------------------------

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    # --------------------------------------------------------
    # Read uploaded file
    # --------------------------------------------------------

    file_content = await file.read()

    # --------------------------------------------------------
    # Save PDF
    # --------------------------------------------------------

    with open(file_path, "wb") as f:
        f.write(file_content)

    # --------------------------------------------------------
    # Extract text from PDF
    # --------------------------------------------------------

    try:

        document = fitz.open(file_path)

        extracted_text = ""

        for page in document:
            extracted_text += page.get_text()

        document.close()

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"PDF extraction failed: {str(e)}"
        )

    # --------------------------------------------------------
    # Save Resume to PostgreSQL
    # --------------------------------------------------------

    resume = Resume(
        filename=file.filename,
        file_path=file_path,
        extracted_text=extracted_text
    )

    db.add(resume)
    db.commit()
    db.refresh(resume)

    # --------------------------------------------------------
    # Store Resume Embedding in Qdrant
    # --------------------------------------------------------

    try:

        create_collection()

        store_resume_embedding(
            resume_id=resume.id,
            filename=resume.filename,
            text=resume.extracted_text or ""
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Qdrant embedding storage failed: {str(e)}"
        )

    # --------------------------------------------------------
    # Response
    # --------------------------------------------------------

    return {
        "message": "Resume uploaded successfully",
        "resume_id": resume.id,
        "filename": resume.filename,
        "text_length": len(extracted_text),
        "qdrant": "embedding stored successfully",
        "extracted_text": extracted_text
    }


# ============================================================
# Resume Skill Extraction
# ============================================================

@router.get("/resume/{resume_id}/skills")
def get_resume_skills(
    resume_id: int,
    db: Session = Depends(get_db)
):

    # --------------------------------------------------------
    # Find Resume
    # --------------------------------------------------------

    resume = db.query(Resume).filter(
        Resume.id == resume_id
    ).first()

    if not resume:

        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )

    # --------------------------------------------------------
    # Extract Skills
    # --------------------------------------------------------

    skills = extract_skills(
        resume.extracted_text or ""
    )

    # --------------------------------------------------------
    # Response
    # --------------------------------------------------------

    return {
        "resume_id": resume.id,
        "filename": resume.filename,
        "skills": skills,
        "skill_count": len(skills)
    }


# ============================================================
# Resume vs Job Description Assessment
# ============================================================

@router.post("/assess")
def assess_resume(
    resume_id: int,
    job_id: int,
    db: Session = Depends(get_db)
):

    # --------------------------------------------------------
    # Find Resume
    # --------------------------------------------------------

    resume = db.query(Resume).filter(
        Resume.id == resume_id
    ).first()

    if not resume:

        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )

    # --------------------------------------------------------
    # Find Job Description
    # --------------------------------------------------------

    job = db.query(JobDescription).filter(
        JobDescription.id == job_id
    ).first()

    if not job:

        raise HTTPException(
            status_code=404,
            detail="Job description not found"
        )

    # --------------------------------------------------------
    # Get Job Description Text
    # --------------------------------------------------------

    job_description = job.extracted_text or ""

    if not job_description.strip():

        raise HTTPException(
            status_code=400,
            detail="Job description has no extracted text"
        )

    # --------------------------------------------------------
    # Search Qdrant
    # --------------------------------------------------------

    try:

        results = search_similar_resumes(
            job_description=job_description,
            limit=5
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Qdrant search failed: {str(e)}"
        )

    # --------------------------------------------------------
    # Find Requested Resume
    # --------------------------------------------------------

    matched_resume = None

    for result in results:

        if result.payload.get("resume_id") == resume_id:

            matched_resume = result
            break

    if matched_resume is None:

        raise HTTPException(
            status_code=404,
            detail="Resume embedding not found in Qdrant"
        )

    # --------------------------------------------------------
    # Calculate Semantic Match Percentage
    # --------------------------------------------------------

    match_score = max(
        0,
        min(
            100,
            matched_resume.score * 100
        )
    )

    # --------------------------------------------------------
    # Extract Resume Skills
    # --------------------------------------------------------

    resume_skills = extract_skills(
        resume.extracted_text or ""
    )

    # --------------------------------------------------------
    # Extract Job Description Skills
    # --------------------------------------------------------

    job_skills = extract_skills(
        job_description
    )

    # --------------------------------------------------------
    # Normalize Skills
    # --------------------------------------------------------

    resume_skill_set = {
        skill.lower(): skill
        for skill in resume_skills
    }

    job_skill_set = {
        skill.lower(): skill
        for skill in job_skills
    }

    # --------------------------------------------------------
    # Matching Skills
    # --------------------------------------------------------

    matching_skills = [
        resume_skill_set[skill]
        for skill in job_skill_set
        if skill in resume_skill_set
    ]

    # --------------------------------------------------------
    # Missing Skills
    # --------------------------------------------------------

    missing_skills = [
        job_skill_set[skill]
        for skill in job_skill_set
        if skill not in resume_skill_set
    ]

    # --------------------------------------------------------
    # Calculate Skill Match Percentage
    # --------------------------------------------------------

    if len(job_skills) > 0:

        skill_match_percentage = (
            len(matching_skills) / len(job_skills)
        ) * 100

    else:

        skill_match_percentage = 0

    # --------------------------------------------------------
    # Final Assessment
    # --------------------------------------------------------

    return {

        "resume_id": resume.id,

        "resume_filename": resume.filename,

        "job_id": job.id,

        "job_filename": job.filename,

        "match_percentage": round(
            match_score,
            2
        ),

        "skill_match_percentage": round(
            skill_match_percentage,
            2
        ),

        "matching_skills": matching_skills,

        "missing_skills": missing_skills,

        "resume_skill_count": len(resume_skills),

        "job_skill_count": len(job_skills),

        "recommendation": (
            "Strong match"
            if match_score >= 75
            else "Moderate match"
            if match_score >= 50
            else "Low match"
        )
    }


# ============================================================
# Job Description Upload
# ============================================================

@router.post("/job/upload")
async def upload_job_description(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    # --------------------------------------------------------
    # Check file type
    # --------------------------------------------------------

    if not file.filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    # --------------------------------------------------------
    # Create upload directory
    # --------------------------------------------------------

    job_upload_dir = "job_descriptions"

    os.makedirs(
        job_upload_dir,
        exist_ok=True
    )

    # --------------------------------------------------------
    # Create file path
    # --------------------------------------------------------

    file_path = os.path.join(
        job_upload_dir,
        file.filename
    )

    # --------------------------------------------------------
    # Read uploaded file
    # --------------------------------------------------------

    file_content = await file.read()

    # --------------------------------------------------------
    # Save PDF
    # --------------------------------------------------------

    with open(file_path, "wb") as f:
        f.write(file_content)

    # --------------------------------------------------------
    # Extract text
    # --------------------------------------------------------

    try:

        document = fitz.open(file_path)

        extracted_text = ""

        for page in document:
            extracted_text += page.get_text()

        document.close()

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Job description extraction failed: {str(e)}"
        )

    # --------------------------------------------------------
    # Save Job Description to PostgreSQL
    # --------------------------------------------------------

    job = JobDescription(
        filename=file.filename,
        file_path=file_path,
        extracted_text=extracted_text
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    # --------------------------------------------------------
    # Response
    # --------------------------------------------------------

    return {

        "message": "Job description uploaded successfully",

        "job_id": job.id,

        "filename": job.filename,

        "text_length": len(extracted_text),

        "extracted_text": extracted_text
    }
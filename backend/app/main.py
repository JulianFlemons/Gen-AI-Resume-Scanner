from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from pydantic import BaseModel, Field
import os 
from services.resume_extraction import extract_text_from_text_resume

app = FastAPI(
    title = "ATS Resume Scanner",
    description = "This is a the API for the ATS Resume Scanner application",
    version = "0.1.0",
)

@app.get("/")
def root():
    return {"message": "Welcome to the AI Taloring Engine!",
            "status": "running"}
@app.get("/health")
def health():
    return {"message": "API is healthy and running",
            "status": "healthy"}


class CategoryScores(BaseModel):
    skills: float = Field(ge=0, le=10)
    experience: float = Field(ge=0, le=10)
    education: float = Field(ge=0, le=10)


class Skills(BaseModel):
    matched: list[str]
    missing: list[str]


class AIAnalysis(BaseModel):
    summary: str
    strengths: list[str]
    improvements: list[str]
    fit_rating: int = Field(ge=0, le=10)


class AnalyzeResponse(BaseModel):
    overall_score: float = Field(ge=0, le=10)
    category_scores: CategoryScores
    skills: Skills
    ai_analysis: AIAnalysis


@app.post("/api/v1/analyze", response_model=AnalyzeResponse)
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
):
    if not job_description.strip():
        raise HTTPException(
            status_code=400,
            detail="Job description cannot be empty.",
        )

    if not resume.filename:
        raise HTTPException(
            status_code=400,
            detail="A filename is required.",
        )

    if not resume.filename.lower().endswith((".pdf", ".docx")):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only PDF and DOCX files are allowed.",
        )
    
    file_content = await resume.read()
    if not file_content:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty.",
        )
    try:
        extracted_text = extract_text_from_text_resume(file_content, os.path.splitext(resume.filename)[1].lower())
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error extracting text from resume: {str(e)}",
        )
    return {"message": "Resume analysis is not implemented yet."}
    # TODO: validate the file, extract resume text, and run the analysis services.
    raise HTTPException(
        status_code=501,
        detail="Resume analysis is not implemented yet.",
    )

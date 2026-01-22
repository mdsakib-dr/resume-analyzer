from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from app.parser import parse_pdf, parse_text
from app.classifier import classify_resume
from app.experience import calculate_experience, experience_level

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(None),
    text: str = Form(None)
):
    if file:
        parsed = parse_pdf(file.file)
    elif text:
        parsed = parse_text(text)
    else:
        return {"error": "Provide either PDF file or resume text"}

    role, confidence = classify_resume(parsed["text"])

    years = calculate_experience(parsed["text"])

    return {
        "name": parsed["name"],
        "email": parsed["email"],
        "phone": parsed["phone"],
        "skills": parsed["skills"],
        "experience_years": years,
        "experience_level": experience_level(years),
        "classification": role,
        "confidence": confidence
    }

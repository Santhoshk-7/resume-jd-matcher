from fastapi import FastAPI, UploadFile, File, Form
from backend.parser import extract_text
from backend.matcher import analyze

app = FastAPI()

@app.post("/analyze")
async def analyze_resume(resume: UploadFile = File(...), jd: str = Form(...)):
    text = extract_text(resume.file)
    return analyze(text, jd)
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

SKILLS = [
    "python", "java", "javascript", "react", "node", "fastapi", "flask",
    "django", "sql", "mongodb", "docker", "kubernetes", "aws", "git",
    "machine learning", "deep learning", "nlp", "tensorflow", "pytorch",
    "pandas", "numpy", "scikit-learn", "rest api", "linux", "c++",
]

def find_skills(text: str) -> set:
    text = text.lower()
    return {s for s in SKILLS if s in text}

def analyze(resume: str, jd: str) -> dict:
    emb = model.encode([resume, jd])
    score = float(util.cos_sim(emb[0], emb[1])) * 100
    resume_skills = find_skills(resume)
    jd_skills = find_skills(jd)
    missing = sorted(jd_skills - resume_skills)
    return {
        "score": round(max(score, 0), 1),
        "matched": sorted(jd_skills & resume_skills),
        "missing": missing,
        "suggestions": [f"Add a bullet showing where you used {s}" for s in missing],
    }
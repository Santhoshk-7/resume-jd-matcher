import re
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

SKILLS = [
    # languages
    "python", "java", "javascript", "typescript", "c++", "c#", "go", "sql",
    "html", "css",
    # frontend
    "react", "next.js", "redux", "tailwind", "angular", "vue",
    # backend
    "node", "express", "fastapi", "flask", "django", "spring boot",
    "rest api", "graphql", "microservices", "jwt",
    # databases
    "mongodb", "mysql", "postgresql", "redis", "firebase",
    # devops / tools
    "docker", "kubernetes", "aws", "azure", "gcp", "git", "github",
    "ci/cd", "linux", "postman",
    # ML / data
    "machine learning", "deep learning", "nlp", "computer vision",
    "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy", "opencv",
    # cs fundamentals
    "data structures", "algorithms", "system design", "oop",
]

def find_skills(text: str) -> set:
    text = text.lower()
    return {s for s in SKILLS if re.search(rf"(?<![a-z]){re.escape(s)}(?![a-z])", text)}

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
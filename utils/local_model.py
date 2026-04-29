import re
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

SKILLS_DB = [
    "python","java","c++","machine learning","deep learning","nlp",
    "react","node","sql","tensorflow","pytorch","flask","fastapi",
    "docker","aws","html","css","javascript"
]

def extract_skills(text):
    text = text.lower()
    return list(set([s for s in SKILLS_DB if s in text]))

def detect_experience(text):
    text = text.lower()
    if "intern" in text or "fresher" in text:
        return "Fresher"
    if "year" in text:
        return "Junior"
    return "Fresher"

def analyse_resume(api_key=None, jd="", resume_text="", pdf_base64=None):

    if not jd or not resume_text:
        return None, "Missing input"

    jd = jd.lower()
    resume = resume_text.lower()

    # 🔹 Semantic similarity
    emb1 = model.encode(resume, convert_to_tensor=True)
    emb2 = model.encode(jd, convert_to_tensor=True)
    score = int(util.cos_sim(emb1, emb2).item() * 100)

    # 🔹 Skills
    resume_skills = extract_skills(resume)
    jd_skills = extract_skills(jd)

    matched = list(set(resume_skills) & set(jd_skills))
    missing = list(set(jd_skills) - set(resume_skills))

    # 🔹 Fake smart suggestions (rule-based)
    improvements = []
    if len(missing) > 0:
        improvements.append(f"Add missing skills: {', '.join(missing[:5])}")
    if "project" not in resume:
        improvements.append("Add project section with real-world work")
    if "experience" not in resume:
        improvements.append("Include internship or practical experience")

    return {
        "name": "Candidate",
        "email": "N/A",
        "phone": "N/A",
        "experience_level": detect_experience(resume),
        "predicted_field": "Software Engineering",
        "match_score": score,
        "extracted_skills": resume_skills,
        "matched_skills": matched,
        "missing_skills": missing,
        "resume_sections": {
            "has_objective": "objective" in resume,
            "has_education": "education" in resume,
            "has_experience": "experience" in resume,
            "has_projects": "project" in resume,
            "has_achievements": "achievement" in resume,
            "has_certifications": "certification" in resume,
        },
        "strengths": [
            "Relevant technical skills detected",
            "Good alignment with job description"
        ],
        "improvements": improvements,
        "course_recommendations": [
            {"title": "DSA", "platform": "GFG", "reason": "Improve coding"},
            {"title": "ML Basics", "platform": "Coursera", "reason": "Core ML skills"}
        ],
        "overall_summary": "Moderate match using semantic similarity and skill overlap."
    }, ""
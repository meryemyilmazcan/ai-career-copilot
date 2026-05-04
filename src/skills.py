SKILL_CATEGORIES = {
    "Programming": [
        "Python", "Java", "C#", "SQL"
    ],
    "AI/ML": [
        "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch",
        "NLP", "Computer Vision", "Data Analysis"
    ],
    "Cloud": [
        "Azure", "AWS", "GCP", "Docker"
    ],
    "Tools": [
        "Git", "REST APIs", "FastAPI", "Streamlit", "n8n"
    ]
}


def extract_skills(text: str):
    text_lower = text.lower()
    found_skills = []

    for category, skills in SKILL_CATEGORIES.items():
        for skill in skills:
            if skill.lower() in text_lower:
                found_skills.append(skill)

    return list(set(found_skills))


def extract_skills_by_category(text: str):
    text_lower = text.lower()
    categorized = {}

    for category, skills in SKILL_CATEGORIES.items():
        found = []
        for skill in skills:
            if skill.lower() in text_lower:
                found.append(skill)
        categorized[category] = found

    return categorized


def compare_skills(cv_skills, job_skills):
    matched = list(set(cv_skills) & set(job_skills))
    missing = list(set(job_skills) - set(cv_skills))
    return matched, missing


def compare_skills_by_category(cv_text: str, job_text: str):
    cv_by_cat = extract_skills_by_category(cv_text)
    job_by_cat = extract_skills_by_category(job_text)

    results = {}

    for category in SKILL_CATEGORIES.keys():
        cv_set = set(cv_by_cat.get(category, []))
        job_set = set(job_by_cat.get(category, []))

        matched = list(cv_set & job_set)
        missing = list(job_set - cv_set)

        results[category] = {
            "matched": matched,
            "missing": missing,
            "job_total": len(job_set)
        }

    return results  
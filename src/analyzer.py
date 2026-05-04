import re
from typing import Dict, List


SKILLS_DB = {
    "Programming": [
        "Python", "Java", "JavaScript", "TypeScript", "SQL", "HTML", "CSS"
    ],
    "AI/ML": [
        "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch",
        "Scikit-learn", "Pandas", "NumPy", "Computer Vision", "NLP",
        "LLM", "GenAI", "AI Agents", "OpenAI"
    ],
    "Tools": [
        "Git", "GitHub", "Docker", "Streamlit", "n8n", "Cursor",
        "Claude", "Excel", "Power BI", "BigQuery", "API"
    ],
    "Soft Skills": [
        "Communication", "Teamwork", "Problem Solving",
        "Analytical Thinking", "Fast Learning", "Attention to Detail",
        "Collaboration"
    ]
}


def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def extract_job_title(job_description: str) -> str:
    lines = job_description.strip().split("\n")

    for line in lines[:8]:
        line = line.strip()
        if 5 < len(line) < 90:
            return line

    return "AI / Data Internship Role"


def find_skills(text: str) -> Dict[str, List[str]]:
    found = {}
    lower_text = text.lower()

    for category, skills in SKILLS_DB.items():
        matched = []

        for skill in skills:
            if skill.lower() in lower_text:
                matched.append(skill)

        found[category] = sorted(list(set(matched)))

    return found


def flatten_skills(skills_dict: Dict[str, List[str]]) -> List[str]:
    result = []

    for skills in skills_dict.values():
        result.extend(skills)

    return sorted(list(set(result)))


def calculate_score(required_skills: List[str], cv_skills: List[str]) -> int:
    if not required_skills:
        return 50

    cv_skills_lower = [skill.lower() for skill in cv_skills]

    matched = [
        skill for skill in required_skills
        if skill.lower() in cv_skills_lower
    ]

    score = int((len(matched) / len(required_skills)) * 100)

    if score < 30:
        return max(score, 30)

    return min(score, 95)


def generate_suggestions(missing_skills: List[str]) -> List[str]:
    suggestions = []

    if not missing_skills:
        return [
            "Your CV is strongly aligned with this role.",
            "Prepare concrete project examples before the interview.",
            "Highlight your AI Career Copilot and multimodal AI project."
        ]

    for skill in missing_skills[:5]:
        suggestions.append(f"Build a small project or example using {skill}.")

    suggestions.append("Create a short portfolio page with screenshots, GitHub links, and demo videos.")
    suggestions.append("Prepare a 30-second pitch explaining your AI projects clearly.")

    return suggestions


def generate_project_idea(required_skills: List[str], missing_skills: List[str]) -> str:
    focus_skills = missing_skills[:3] if missing_skills else required_skills[:3]

    if focus_skills:
        skills_text = ", ".join(focus_skills)
    else:
        skills_text = "AI, automation, and Python"

    return (
        f"Build a mini project focused on {skills_text}. "
        "For example, create an AI assistant that analyzes job descriptions, compares them with a CV, "
        "detects missing skills, and generates a tailored cover letter."
    )


def generate_cover_letter(
    job_title: str,
    matched_skills: List[str],
    match_score: int
) -> str:
    matched_text = ", ".join(matched_skills[:6]) if matched_skills else "Python, AI, and practical software development"

    return f"""Dear Hiring Team,

I am writing to express my interest in the {job_title} position. I have a background in Computer Science with a strong focus on Artificial Intelligence, machine learning, and practical AI tool development.

My experience includes building AI-based projects such as a multimodal deep learning system combining image data and structured data, as well as an AI Career Copilot that analyzes job descriptions, compares them with a CV, extracts key skills, scores candidate-job fit, and generates tailored application materials.

This role matches my profile with a candidate-job fit score of {match_score}%, especially in areas such as {matched_text}. I enjoy building practical solutions that solve real problems, and I am motivated to contribute to AI-focused, data-driven, and automation-oriented projects.

I am also actively improving my skills and building portfolio projects to strengthen my practical experience. I would welcome the opportunity to discuss how my background, motivation, and project experience can contribute to your team.

Kind regards,
Meryem Yilmazcan
"""


def generate_cv(
    job_title: str,
    matched_skills: List[str],
    missing_skills: List[str]
) -> str:
    priority_skills = matched_skills + missing_skills[:3]
    skills_text = ", ".join(priority_skills) if priority_skills else "Python, AI, Machine Learning, Streamlit"

    return f"""Meryem Yilmazcan
Computer Science Graduate | AI & Machine Learning Projects
Warsaw, Poland | GitHub: github.com/meryemyilmazcan | LinkedIn: linkedin.com/in/meryem-yilmazcan

TARGET ROLE
{job_title}

PROFILE
Motivated Computer Science graduate with a strong focus on Artificial Intelligence, machine learning, automation, and practical AI tool development. Experienced in building AI-powered applications that solve real problems, including CV-job matching, skill extraction, cover letter generation, and multimodal deep learning systems.

TECHNICAL SKILLS
{skills_text}

PROJECTS
AI Career Copilot
- Built an AI-powered career assistant that analyzes CVs and job descriptions.
- Implemented candidate-job match scoring, missing skill detection, project suggestions, structured JSON output, CSV export, and tailored cover letter generation.
- Used Python, Streamlit, PyPDF2, Pandas, and rule-based skill extraction.

Multimodal Liver Steatosis Classification System
- Built a multimodal deep learning system combining ultrasound image data and biochemical markers.
- Developed CNN and MLP components and combined them using late fusion.
- Created an interactive Streamlit prototype for prediction and result visualization.

EXPERIENCE
AI Intern — Cognilize GmbH
- Worked on AI-related tasks using Python, PyTorch, and TensorFlow.
- Supported data preprocessing, model training, and practical AI solution development.
- Gained hands-on experience in building machine learning workflows.

EDUCATION
Computer Science, Vistula University
Specialization: Artificial Intelligence and biomedical data processing

LANGUAGES
Turkish: Native
English: B2
Polish: B1

STRENGTHS
Problem solving, analytical thinking, fast learning, teamwork, communication, practical project mindset
"""


def analyze_job(job_description: str, cv_text: str) -> Dict:
    job_description = clean_text(job_description)
    cv_text = clean_text(cv_text)

    job_title = extract_job_title(job_description)

    job_skills_by_category = find_skills(job_description)
    cv_skills_by_category = find_skills(cv_text)

    required_skills = flatten_skills(job_skills_by_category)
    cv_skills = flatten_skills(cv_skills_by_category)

    cv_skills_lower = [cv_skill.lower() for cv_skill in cv_skills]

    matched_skills = [
        skill for skill in required_skills
        if skill.lower() in cv_skills_lower
    ]

    missing_skills = [
        skill for skill in required_skills
        if skill.lower() not in cv_skills_lower
    ]

    match_score = calculate_score(required_skills, cv_skills)

    result = {
        "job_title": job_title,
        "match_score": match_score,
        "skills_by_category": job_skills_by_category,
        "cv_skills": cv_skills,
        "required_skills": required_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "suggestions": generate_suggestions(missing_skills),
        "project_idea": generate_project_idea(required_skills, missing_skills),
        "cover_letter": generate_cover_letter(
            job_title,
            matched_skills,
            match_score
        ),
        "generated_cv": generate_cv(
            job_title,
            matched_skills,
            missing_skills
        )
    }

    return result 
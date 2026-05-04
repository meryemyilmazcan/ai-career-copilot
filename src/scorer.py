import re


CATEGORY_SKILLS = {
    "Programming": [
        "python", "java", "c++", "c#", "javascript", "typescript", "sql",
        "html", "css", "git", "api", "oop"
    ],
    "AI/ML": [
        "machine learning", "deep learning", "artificial intelligence",
        "tensorflow", "pytorch", "scikit-learn", "sklearn", "nlp",
        "computer vision", "cnn", "llm", "data analysis",
        "data preprocessing", "model training", "model evaluation"
    ],
    "Cloud": [
        "aws", "azure", "gcp", "google cloud", "docker", "kubernetes",
        "ci/cd", "deployment", "cloud", "devops"
    ],
    "Tools": [
        "streamlit", "pandas", "numpy", "matplotlib", "power bi", "excel",
        "tableau", "jira", "notion", "github", "linux", "postgresql",
        "mysql", "mongodb"
    ]
}


GENERIC_KEYWORDS = [
    "teamwork", "communication", "problem solving", "analytical thinking",
    "collaboration", "fast learner", "attention to detail"
]


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def find_present_terms(text: str, terms: list) -> list:
    text_norm = normalize_text(text)
    present = []
    for term in terms:
        pattern = r"\b" + re.escape(term.lower()) + r"\b"
        if re.search(pattern, text_norm):
            present.append(term)
    return present


def category_score(cv_text: str, jd_text: str, category_terms: list) -> tuple[int, list, list]:
    cv_present = set(find_present_terms(cv_text, category_terms))
    jd_present = set(find_present_terms(jd_text, category_terms))

    matched = sorted(list(cv_present.intersection(jd_present)))
    missing = sorted(list(jd_present - cv_present))

    if not jd_present:
        return 0, matched, missing

    score = int((len(matched) / len(jd_present)) * 100)
    return score, matched, missing


def measure_experience_strength(cv_text: str) -> int:
    text = normalize_text(cv_text)

    points = 0

    action_verbs = [
        "developed", "built", "designed", "implemented", "optimized",
        "created", "trained", "analyzed", "improved", "collaborated",
        "deployed", "automated"
    ]
    verb_hits = sum(1 for verb in action_verbs if re.search(r"\b" + re.escape(verb) + r"\b", text))
    points += min(verb_hits * 5, 25)

    number_hits = len(re.findall(r"\b\d+[%+]?\b", cv_text))
    points += min(number_hits * 4, 20)

    project_words = ["project", "internship", "experience", "research", "thesis"]
    project_hits = sum(1 for word in project_words if re.search(r"\b" + re.escape(word) + r"\b", text))
    points += min(project_hits * 5, 20)

    return min(points, 40)


def evaluate_cv_against_jd(cv_text: str, cv_skills: dict, job_description: str) -> dict:
    category_scores = {}
    all_matched = []
    all_missing = []

    for category, terms in CATEGORY_SKILLS.items():
        score, matched, missing = category_score(cv_text, job_description, terms)
        category_scores[category] = score
        all_matched.extend(matched)
        all_missing.extend(missing)

    all_matched = sorted(list(set(all_matched)))
    all_missing = sorted(list(set(all_missing)))

    # Main skill score
    non_zero_categories = [score for score in category_scores.values() if score > 0]
    skill_match_score = int(sum(category_scores.values()) / len(category_scores)) if category_scores else 0

    # Extra CV quality score
    experience_score = measure_experience_strength(cv_text)

    # Weighted final score
    weighted_score = int((skill_match_score * 0.75) + (experience_score * 0.625))
    final_score = max(0, min(100, weighted_score))

    # Missing logic fix
    inferred_missing = []
    for category, score in category_scores.items():
        if score == 0:
            if category == "Cloud":
                inferred_missing.extend(["AWS / Azure / GCP", "Docker / Deployment"])
            elif category == "Tools":
                inferred_missing.extend(["GitHub / Jira / Linux", "Pandas / NumPy / Streamlit"])
            elif category == "Programming":
                inferred_missing.extend(["Core programming keywords"])
            elif category == "AI/ML":
                inferred_missing.extend(["AI/ML project-specific keywords"])

        elif score < 35:
            if category == "Cloud":
                inferred_missing.append("More cloud/deployment experience")
            elif category == "Tools":
                inferred_missing.append("More tooling ecosystem keywords")
            elif category == "Programming":
                inferred_missing.append("More programming alignment with the JD")
            elif category == "AI/ML":
                inferred_missing.append("More AI/ML alignment with the JD")

    missing_skills = sorted(list(set(all_missing + inferred_missing)))

    # Missing keywords from generic JD terms
    generic_missing = []
    jd_generic = find_present_terms(job_description, GENERIC_KEYWORDS)
    cv_generic = find_present_terms(cv_text, GENERIC_KEYWORDS)
    for kw in jd_generic:
        if kw not in cv_generic:
            generic_missing.append(kw)

    # Improvement suggestions
    improvement_suggestions = []

    if experience_score < 15:
        improvement_suggestions.append("Add stronger action verbs such as developed, built, implemented, or optimized.")

    if len(re.findall(r"\b\d+[%+]?\b", cv_text)) < 2:
        improvement_suggestions.append("Add more measurable achievements with numbers, percentages, or project outcomes.")

    if category_scores["Cloud"] == 0:
        improvement_suggestions.append("Your CV lacks cloud or deployment keywords such as AWS, Docker, CI/CD, or GCP.")

    if category_scores["Tools"] == 0:
        improvement_suggestions.append("Add more technical tools such as GitHub, Linux, Jira, Pandas, NumPy, or Streamlit where relevant.")

    if category_scores["Programming"] < 50:
        improvement_suggestions.append("Strengthen the programming section with clearer mention of languages, APIs, SQL, and software fundamentals.")

    if category_scores["AI/ML"] < 50:
        improvement_suggestions.append("Tailor the AI/ML section more closely to the role using keywords from the job description.")

    if not improvement_suggestions:
        improvement_suggestions.append("Your CV already shows solid alignment; focus on clearer project impact and stronger result-based bullets.")

    # Rewrite suggestions
    rewrite_suggestions = {
        "summary": (
            "Rewrite your CV summary to directly reflect the job description. "
            "Mention your strongest technical areas first, such as Python, AI/ML, backend development, data analysis, or deployment experience."
        ),
        "project_bullets": (
            "Rewrite project bullets using action verbs and measurable impact. "
            "Example format: 'Built a machine learning pipeline in Python using TensorFlow, improving model workflow efficiency and supporting real-world data analysis.'"
        )
    }

    # Why you fit
    why_you_fit = []
    if category_scores["Programming"] >= 50:
        why_you_fit.append("Your CV shows relevant programming foundations for the target role.")
    if category_scores["AI/ML"] >= 50:
        why_you_fit.append("You already demonstrate strong AI/ML alignment through core keywords and technical project language.")
    if "internship" in normalize_text(cv_text):
        why_you_fit.append("Your internship experience adds practical credibility beyond coursework.")
    if "project" in normalize_text(cv_text) or "thesis" in normalize_text(cv_text):
        why_you_fit.append("Your project or thesis work helps position you as a hands-on candidate.")

    # Why not a good fit yet
    not_a_good_fit = []
    if category_scores["Cloud"] == 0:
        not_a_good_fit.append("The CV does not currently show cloud or deployment exposure.")
    if category_scores["Tools"] == 0:
        not_a_good_fit.append("The tooling ecosystem looks underrepresented compared with typical technical job expectations.")
    if len(re.findall(r"\b\d+[%+]?\b", cv_text)) < 2:
        not_a_good_fit.append("The CV has limited measurable impact statements.")
    if not not_a_good_fit:
        not_a_good_fit.append("No major blockers detected for this sample role.")

    return {
        "final_score": final_score,
        "category_scores": category_scores,
        "matched_skills": all_matched,
        "missing_skills": missing_skills,
        "missing_keywords": generic_missing,
        "improvement_suggestions": improvement_suggestions,
        "rewrite_suggestions": rewrite_suggestions,
        "why_you_fit": why_you_fit,
        "not_a_good_fit": not_a_good_fit,
        "score_breakdown": {
            "skill_match_score": skill_match_score,
            "experience_score": experience_score,
            "weighted_score": final_score
        }
    }


def generate_cover_letter(
    cv_text: str,
    job_description: str,
    company_name: str = "",
    target_role: str = "",
    tone: str = "Formal"
) -> str:
    text = normalize_text(cv_text)

    company = company_name if company_name else "your company"
    role = target_role if target_role else "this role"

    intro_style = {
        "Formal": f"I am writing to express my interest in the {role} position at {company}.",
        "Confident": f"I am excited to apply for the {role} position at {company}, where I can contribute strong technical skills and hands-on project experience.",
        "Friendly": f"I would be glad to be considered for the {role} position at {company}."
    }

    experience_line = (
        "Through my academic background and technical projects, I have built practical experience in Python, machine learning, data analysis, and software development."
    )

    if "pytorch" in text or "tensorflow" in text:
        experience_line = (
            "Through academic work, technical projects, and hands-on experience, I have developed practical skills in Python, machine learning, and model development using tools such as PyTorch and TensorFlow."
        )

    if "internship" in text:
        experience_line += " My internship experience also strengthened my ability to work on real-world technical tasks in a collaborative environment."

    contribution_line = (
        f"I am particularly motivated by opportunities where I can apply my knowledge, continue learning, and contribute to meaningful work aligned with the needs of {company}."
    )

    closing_line = (
        "Thank you for your time and consideration. I would welcome the opportunity to discuss how my background and motivation can contribute to your team."
    )

    cover_letter = f"""Dear Hiring Team,

{intro_style.get(tone, intro_style["Formal"])}

{experience_line}

{contribution_line}

{closing_line}

Kind regards,
Candidate
"""
    return cover_letter  
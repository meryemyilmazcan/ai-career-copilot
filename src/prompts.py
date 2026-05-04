ANALYZE_PROMPT = """
You are an AI recruiter.

Return JSON only with:
- score (0-100)
- experience_alignment (short)
- strengths (list)
- weaknesses (list)
- why_not_fit (list of 3-5 concrete reasons)
- improvements (list of 5 actionable items)

CV:
{cv_text}

Job Description:
{job_text}
"""

COVER_LETTER_PROMPT = """
Write a concise, professional cover letter (150-220 words).
Tone: {tone}

CV:
{cv_text}

Job Description:
{job_text}
"""
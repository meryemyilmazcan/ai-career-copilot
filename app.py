import json
import streamlit as st
import pandas as pd
import PyPDF2

from src.analyzer import analyze_job


st.set_page_config(
    page_title="AI Career Copilot",
    page_icon="🚀",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a, #020617);
    color: #e5e7eb;
}
h1 {
    font-size: 44px !important;
    font-weight: 800;
}
.block-container {
    padding-top: 2rem;
}
.stButton>button {
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    color: white;
    border-radius: 12px;
    padding: 10px 22px;
    border: none;
    font-weight: 700;
}
.stProgress > div > div > div > div {
    background-color: #6366f1;
}
textarea {
    border-radius: 12px !important;
}
details {
    border-radius: 12px;
}
code {
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<h1>🚀 AI Career Copilot</h1>
<p style='color: #9ca3af; font-size:16px;'>
Upload CV + Job Description → Match Score, Missing Skills, Cover Letter & Tailored CV
</p>
""", unsafe_allow_html=True)


st.sidebar.title("⚙️ Settings")
st.sidebar.write(
    "AI Career Copilot combines CV analysis, job description analysis, "
    "skill matching, cover letter generation, and tailored CV creation."
)


# ---------------- CV UPLOAD ---------------- #

st.subheader("📄 Upload Your CV")

uploaded_file = st.file_uploader(
    "Upload your CV file",
    type=["pdf", "txt"]
)

cv_text = ""

if uploaded_file is not None:
    if uploaded_file.type == "text/plain":
        cv_text = uploaded_file.read().decode("utf-8")

    elif uploaded_file.type == "application/pdf":
        reader = PyPDF2.PdfReader(uploaded_file)
        for page in reader.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                cv_text += extracted_text + "\n"

    st.success("CV uploaded successfully!")


# ---------------- JOB DESCRIPTION ---------------- #

st.subheader("📌 Job Description")

job_description = st.text_area(
    "Paste the job description here:",
    height=280,
    placeholder="Paste internship or junior job description..."
)


# ---------------- ANALYSIS ---------------- #

if st.button("Analyze Job"):
    if not job_description.strip():
        st.warning("Please paste a job description first.")
    elif not cv_text.strip():
        st.warning("Please upload your CV first.")
    else:
        result = analyze_job(job_description, cv_text)

        st.success("Analysis completed!")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🎯 Job Title")
            st.write(result["job_title"])

            st.subheader("📊 Match Score")
            st.progress(result["match_score"] / 100)

            score = result["match_score"]

            if score >= 75:
                st.success(f"🔥 Strong Match: {score}%")
            elif score >= 50:
                st.warning(f"⚡ Medium Match: {score}%")
            else:
                st.error(f"❗ Low Match: {score}%")

        with col2:
            st.subheader("🧠 Project Suggestion")
            st.markdown(f"""
            <div style="background:#1e293b; padding:18px; border-radius:14px; line-height:1.7;">
                💡 {result["project_idea"]}
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        st.subheader("✅ Matched Skills")
        if result["matched_skills"]:
            st.markdown(" ".join([f"`{skill}`" for skill in result["matched_skills"]]))
        else:
            st.write("No matched skills found.")

        st.subheader("⚠️ Missing Skills")
        if result["missing_skills"]:
            st.markdown(" ".join([f"`{skill}`" for skill in result["missing_skills"]]))
        else:
            st.write("No major missing skills detected.")

        st.divider()

        st.subheader("📚 Skills by Category")
        for category, skills in result["skills_by_category"].items():
            with st.expander(category):
                if skills:
                    st.markdown(" ".join([f"`{skill}`" for skill in skills]))
                else:
                    st.write("No skills detected in this category.")

        st.divider()

        st.subheader("💡 Suggestions")
        for suggestion in result["suggestions"]:
            st.write(f"- {suggestion}")

        st.divider()

        st.subheader("📄 Tailored Cover Letter")
        st.text_area(
            "Generated Cover Letter",
            value=result["cover_letter"],
            height=360
        )

        st.divider()

        st.subheader("🧾 Generated CV / Resume")
        st.text_area(
            "Generated CV tailored to this job",
            value=result["generated_cv"],
            height=420
        )

        st.divider()

        st.subheader("🧱 Clean Structured Output")

        clean_json = {
            "job_title": result["job_title"],
            "match_score": result["match_score"],
            "matched_skills": result["matched_skills"],
            "missing_skills": result["missing_skills"],
            "project_idea": result["project_idea"]
        }

        st.code(json.dumps(clean_json, indent=2, ensure_ascii=False), language="json")

        df = pd.DataFrame({
            "Category": [
                "Job Title",
                "Match Score",
                "Matched Skills",
                "Missing Skills",
                "Project Suggestion"
            ],
            "Result": [
                result["job_title"],
                f"{result['match_score']}%",
                ", ".join(result["matched_skills"]),
                ", ".join(result["missing_skills"]),
                result["project_idea"]
            ]
        })

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="⬇️ Download Analysis as CSV",
            data=csv,
            file_name="career_copilot_analysis.csv",
            mime="text/csv"
        )

        st.download_button(
            label="⬇️ Download Generated CV as TXT",
            data=result["generated_cv"].encode("utf-8"),
            file_name="generated_tailored_cv.txt",
            mime="text/plain"
        )
import streamlit as st
import requests
from utils import generate_pdf_resume
from advisor_logic import generate_career_advice, generate_cover_letter

# Page config
st.set_page_config(page_title="AI Career Advisor", page_icon="💼")

# Sidebar navigation
st.sidebar.title("💼 AI Career Advisor")
section = st.sidebar.radio(
    "Navigate", 
    ["Career Advice", "Resume Builder", "Cover Letter Generator", "Job Finder & Auto Apply"]
)

# Language mapping
lang_code_map = {
    "English": "en", "French": "fr", "Spanish": "es", 
    "Yoruba": "yo", "Hausa": "ha", "Igbo": "ig"
}

# -------------------------------
# Section 1: Career Advice
# -------------------------------
if section == "Career Advice":
    st.title("🧠 Career Advice")
    st.markdown("Get personalized career advice from your AI assistant.")

    name = st.text_input("Your Name", key="ca_name")
    background = st.text_area("Your Background", key="ca_bg")
    interests = st.text_area("Your Interests or Career Goals", key="ca_interests")
    language = st.selectbox("Preferred Language", list(lang_code_map.keys()), key="ca_lang")
    lang_code = lang_code_map[language]

    if st.button("Generate Advice"):
        if not name or not background or not interests:
            st.warning("Please complete all fields.")
        else:
            with st.spinner("Generating advice..."):
                try:
                    advice = generate_career_advice(name, background, interests, language)
                    st.success("✅ Career advice generated!")
                    st.text_area("📋 Career Advice", value=advice, height=400)
                except Exception as e:
                    st.error(f"❌ Error: {e}")

# -------------------------------
# Section 2: Resume Builder
# -------------------------------
elif section == "Resume Builder":
    st.title("📄 Resume Builder")
    st.markdown("Generate a professional resume in PDF format.")

    name = st.text_input("Your Name", key="rb_name")
    summary = st.text_area("Professional Summary", key="rb_summary")
    skills = st.text_area("Skills (comma-separated)", key="rb_skills")
    education = st.text_area("Education", key="rb_education")
    experience = st.text_area("Work Experience", key="rb_experience")
    achievements = st.text_area("Achievements", key="rb_achievements")

    if st.button("Generate Resume"):
        if not name or not summary:
            st.warning("Please provide your name and summary.")
        else:
            resume_text = f"""Resume - {name}\n\nProfessional Summary:\n{summary}\n\nSkills:\n{skills}\n\nEducation:\n{education}\n\nExperience:\n{experience}\n\nAchievements:\n{achievements}"""
            pdf_path = generate_pdf_resume(resume_text, filename="resume.pdf")
            st.success("✅ Resume Generated!")
            with open(pdf_path, "rb") as f:
                st.download_button("📥 Download Resume", f, file_name="resume.pdf")

# -------------------------------
# Section 3: Cover Letter Generator
# -------------------------------
elif section == "Cover Letter Generator":
    st.title("✍️ Cover Letter Generator")
    st.markdown("Create a personalized cover letter for a specific job.")

    name = st.text_input("Your Name", key="cl_name")
    email = st.text_input("Your Email", key="cl_email")
    role = st.text_input("Target Job Role", key="cl_role")
    company = st.text_input("Company Name", key="cl_company")
    job_desc = st.text_area("Job Description", key="cl_description")
    tone = st.selectbox("Tone", ["Professional", "Friendly", "Passionate"], key="cl_tone")
    language = st.selectbox("Preferred Language", list(lang_code_map.keys()), key="cl_lang")
    lang_code = lang_code_map[language]

    if st.button("Generate Cover Letter"):
        if not all([name, email, role, company, job_desc]):
            st.warning("⚠️ Please fill in all fields.")
        else:
            with st.spinner("Generating..."):
                try:
                    letter = generate_cover_letter(name, email, role, company, job_desc, tone, lang_code)
                    st.text_area("📄 Cover Letter", letter, height=400)
                except Exception as e:
                    st.error(f"❌ Error: {e}")

# -------------------------------
# Section 4: Job Finder & Auto Apply
# -------------------------------
elif section == "Job Finder & Auto Apply":
    st.title("🔍 Job Finder & Auto Apply")
    st.markdown("Search for remote jobs and generate custom cover letters.")

    name = st.text_input("Your Name", key="job_name")
    email = st.text_input("Your Email", key="job_email")
    query = st.text_input("Job Title or Keywords", key="job_query")
    location = st.text_input("Preferred Location (optional)", key="job_location")
    remote = st.selectbox("Remote Only?", ["Yes", "No", "Any"], index=0, key="job_remote")
    language = st.selectbox("Preferred Language", list(lang_code_map.keys()), key="job_lang")
    lang_code = lang_code_map[language]

    if st.button("Search Jobs"):
        with st.spinner("Searching for jobs..."):
            jobs = search_jobs_remotive(query, location, remote)

        if not jobs:
            st.warning("No jobs found.")
        else:
            for i, job in enumerate(jobs):
                with st.expander(f"📌 {job['title']} at {job['company_name']}"):
                    st.markdown(f"**Location:** {job['candidate_required_location']}")
                    st.markdown(f"**Category:** {job['category']}")
                    st.markdown(f"[Apply Link]({job['url']})")
                    if st.button(f"✍️ Generate Cover Letter for Job {i+1}", key=f"job_button_{i}"):
                        with st.spinner("Generating tailored cover letter..."):
                            try:
                                job_title = job['title']
                                company = job['company_name']
                                job_desc = job.get("description", "")
                                cover_letter = generate_cover_letter(name, email, job_title, company, job_desc, "Professional", lang_code)
                                st.text_area("📄 Your Cover Letter", cover_letter, height=300)
                            except Exception as e:
                                st.error(f"Error: {e}")

# -------------------------------
# Helper: Remotive API Function
# -------------------------------
def search_jobs_remotive(query, location, remote):
    url = "https://remotive.io/api/remote-jobs"
    params = {"search": query}
    try:
        res = requests.get(url, params=params)
        data = res.json()
        jobs = data.get("jobs", [])
        if remote == "Yes":
            jobs = [job for job in jobs if "Remote" in job.get("job_type", "")]
        elif remote == "No":
            jobs = [job for job in jobs if "Remote" not in job.get("job_type", "")]
        return jobs[:5]
    except Exception as e:
        st.error(f"API Error: {e}")
        return []

# -------------------------------
# Footer
# -------------------------------
st.markdown(
    """
    <hr style="margin-top: 2em;"/>
    <div style="text-align: center; color: gray;">
        Made with ❤️ by <strong>RedCherry</strong>
    </div>
    """,
    unsafe_allow_html=True
)

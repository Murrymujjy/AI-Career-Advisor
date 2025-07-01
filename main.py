import streamlit as st
import requests
from utils import generate_pdf_resume
from advisor_logic import generate_career_advice, generate_cover_letter

from dotenv import load_dotenv
load_dotenv()

# ✅ Helper function moved to top
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

# Streamlit config
st.set_page_config(page_title="AI Career Advisor", page_icon="💼")

# Sidebar
st.sidebar.title("💼 AI Career Advisor")
section = st.sidebar.radio(
    "Navigate", 
    ["Career Advice", "Resume Builder", "Cover Letter Generator", "Job Finder & Auto Apply"]
)

# Header
st.title("💼 AI Career Advisor")
st.markdown("Get personalized career support powered by your local AI model (via LM Studio).")

# Common Inputs
name = st.text_input("Your Name", placeholder="e.g. Mujeebat")
email = st.text_input("Your Email", placeholder="e.g. murrymujjy@gmail.com")
background = st.text_area("Brief Background", placeholder="e.g. Nuclear Physics")
interests = st.text_area("Your Interests or Career Goals", placeholder="e.g. Machine Learning, Data Science")
language = st.selectbox("Preferred Language", ["English", "French", "Spanish", "Yoruba", "Hausa", "Igbo"])
lang_code_map = {
    "English": "en", "French": "fr", "Spanish": "es", 
    "Yoruba": "yo", "Hausa": "ha", "Igbo": "ig"
}
lang_code = lang_code_map.get(language, "en")

# Section 1: Career Advice
if section == "Career Advice":
    if st.button("🧠 Generate Career Advice"):
        if not name or not background or not interests:
            st.warning("⚠️ Please complete all fields.")
        else:
            with st.spinner("Generating advice..."):
                try:
                    advice = generate_career_advice(name, background, interests, language)
                    st.success("✅ Career advice generated!")
                    st.text_area("📋 Career Advice", value=advice, height=400)
                except Exception as e:
                    st.error(f"❌ Error: {e}")

# Section 2: Resume Builder
elif section == "Resume Builder":
    st.subheader("📄 Resume Builder")

    summary = st.text_area("Professional Summary", placeholder="e.g. Passionate Machine Learning engineer...")
    skills = st.text_area("Skills (comma-separated)", placeholder="e.g. Python, SQL, TensorFlow")
    education = st.text_area("Education", placeholder="e.g. BSc in Engineering Physics...")
    experience = st.text_area("Work Experience", placeholder="e.g. Interned at XYZ Ltd...")
    achievements = st.text_area("Achievements", placeholder="e.g. 1st prize in Zindi Hackathon...")

    if st.button("📄 Generate Resume"):
        if not name or not summary:
            st.warning("Please fill in your name and professional summary.")
        else:
            resume_text = f"""Resume - {name}\n\nProfessional Summary:\n{summary}\n\nSkills:\n{skills}\n\nEducation:\n{education}\n\nExperience:\n{experience}\n\nAchievements:\n{achievements}"""
            pdf_path = generate_pdf_resume(resume_text, filename="resume.pdf")
            st.success("✅ Resume Generated!")
            with open(pdf_path, "rb") as f:
                st.download_button("📥 Download Resume", f, file_name="resume.pdf")

# Section 3: Cover Letter Generator
elif section == "Cover Letter Generator":
    role = st.text_input("Target Job Role", placeholder="e.g. Data Scientist")
    company = st.text_input("Company Name", placeholder="e.g. Google")
    job_desc = st.text_area("Job Description", placeholder="Paste the job description here.")
    tone = st.selectbox("Tone of Letter", ["Professional", "Friendly", "Passionate"])

    if st.button("✍️ Generate Cover Letter"):
        if not all([name, email, role, company, job_desc]):
            st.warning("⚠️ Please fill in all fields.")
        else:
            with st.spinner("Generating..."):
                try:
                    letter = generate_cover_letter(name, email, role, company, job_desc, tone, lang_code)
                    st.text_area("📄 Cover Letter", letter, height=400)
                except Exception as e:
                    st.error(f"❌ Error: {e}")

# Section 4: Job Finder & Auto Apply
elif section == "Job Finder & Auto Apply":
    st.subheader("🔍 Job Finder & Auto Apply")
    st.write("Search for jobs online and generate personalized cover letters.")

    query = st.text_input("Job Title or Keywords", placeholder="e.g. Data Analyst")
    location = st.text_input("Location (optional)", placeholder="e.g. Remote or Lagos")
    remote = st.selectbox("Remote Only?", ["Yes", "No", "Any"], index=0)

    if st.button("Search Jobs"):
        with st.spinner("Searching..."):
            jobs = search_jobs_remotive(query, location, remote)

        if not jobs:
            st.warning("No jobs found.")
        else:
            for i, job in enumerate(jobs):
                with st.expander(f"📌 {job['title']} at {job['company_name']}"):
                    st.markdown(f"**Location:** {job['candidate_required_location']}")
                    st.markdown(f"**Category:** {job['category']}")
                    st.markdown(f"[Apply Link]({job['url']})")
                    if st.button(f"✍️ Generate Cover Letter for Job {i+1}"):
                        with st.spinner("Generating tailored cover letter..."):
                            try:
                                job_title = job['title']
                                company = job['company_name']
                                job_desc = job.get("description", "")
                                cover_letter = generate_cover_letter(name, email, job_title, company, job_desc, "Professional", lang_code)
                                st.text_area("📄 Your Cover Letter", cover_letter, height=300)
                            except Exception as e:
                                st.error(f"Error: {e}")

# Footer
st.markdown(
    """
    <hr style="margin-top: 2em;"/>
    <div style="text-align: center; color: gray;">
        Made with ❤️ by <strong>RedCherry</strong>
    </div>
    """,
    unsafe_allow_html=True
)

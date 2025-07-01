import streamlit as st
import requests
from advisor_logic import generate_career_advice
from resume_builder import generate_resume
from cover_letter import generate_cover_letter

# Set page config
st.set_page_config(page_title="AI Career Advisor", page_icon="💼")

# Sidebar navigation
st.sidebar.title("💼 AI Career Advisor")
section = st.sidebar.radio(
    "Navigate", 
    ["Career Advice", "Resume Builder", "Cover Letter Generator", "Job Finder & Auto Apply"]
)

# Header
st.title("💼 AI Career Advisor")
st.markdown("Get personalized career support powered by your local AI model (via LM Studio).")

# Common inputs
name = st.text_input("Your Name", placeholder="e.g. Mujeebat")
background = st.text_area("Brief Background", placeholder="e.g. Nuclear Physics")
interests = st.text_area("Your Interests or Career Goals", placeholder="e.g. Machine Learning, Data Science")
language = st.selectbox("Preferred Language", ["English", "French", "Spanish", "Yoruba", "Hausa", "Igbo"])

# Section logic
if section in ["Career Advice", "Resume Builder", "Cover Letter Generator"]:
    if st.button("🧠 Generate"):
        if not name or not background or not interests:
            st.error("⚠️ Please complete all fields.")
        else:
            with st.spinner("Thinking..."):
                try:
                    if section == "Career Advice":
                        response = generate_career_advice(name, background, interests, language)
                    elif section == "Resume Builder":
                        response = generate_resume(name, background, interests)
                    elif section == "Cover Letter Generator":
                        response = generate_cover_letter(name, background, interests)

                    st.success("✅ Response Generated!")
                    st.text_area("🔍 Output", value=response, height=500)
                except Exception as e:
                    st.error(f"❌ Failed to generate response: {e}")

# ----------------- JOB FINDER SECTION -----------------
elif section == "Job Finder & Auto Apply":
    st.subheader("🔍 Job Finder & Auto Apply")
    st.write("Search for jobs online and generate a personalized cover letter for each!")

    query = st.text_input("Job Title or Keywords", placeholder="e.g. Data Analyst")
    location = st.text_input("Location (optional)", placeholder="e.g. Remote or Lagos")
    remote = st.selectbox("Remote Only?", ["Yes", "No", "Any"], index=0)

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
                    st.markdown(f"**URL:** [Apply Here]({job['url']})")
                    st.markdown("---")

                    if st.button(f"✍️ Generate Cover Letter for Job {i+1}"):
                        with st.spinner("Generating tailored cover letter..."):
                            try:
                                job_title = job['title']
                                company = job['company_name']
                                job_desc = job.get("description", "")
                                cover_letter = generate_cover_letter(name, background, interests, job_title, company, job_desc)
                                st.text_area("📄 Your Cover Letter", cover_letter, height=300)
                            except Exception as e:
                                st.error(f"Error: {e}")

# ----------------- REMOTIVE HELPER FUNCTION -----------------
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

        return jobs[:5]  # Return top 5
    except Exception as e:
        st.error(f"API Error: {e}")
        return []

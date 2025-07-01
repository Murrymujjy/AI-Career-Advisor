# job_finder.py

import streamlit as st
import requests
import json
from advisor_logic import generate_cover_letter

st.title("🌍 Job Finder & Auto Apply")

st.markdown("Search for remote jobs online, and generate a custom cover letter using AI.")

# Input fields
job_keyword = st.text_input("🔍 Enter a Job Keyword", value="Machine Learning")
job_category = st.selectbox("📁 Choose a Category", [
    "Software Development", "Customer Service", "Design", "Marketing", "Sales", "Product", "Other"
])

# User profile for personalization
with st.expander("✍️ Your Profile (for Cover Letter)"):
    user_name = st.text_input("Your Name", value="Mujeebat")
    background = st.text_area("Brief Background", value="Background in Nuclear Physics, interested in AI/ML.")
    language = st.selectbox("Preferred Language", ["English (US)", "French", "Spanish", "Yoruba", "Hausa", "Igbo"])

# Button to trigger job search
if st.button("🔎 Search Jobs"):
    with st.spinner("Fetching remote jobs..."):
        api_url = f"https://remotive.io/api/remote-jobs?search={job_keyword}&category={job_category.replace(' ', '%20')}"
        response = requests.get(api_url)
        if response.status_code == 200:
            jobs = response.json().get("jobs", [])
            if jobs:
                st.success(f"Found {len(jobs)} jobs! Showing top 5.")
                for job in jobs[:5]:
                    with st.container():
                        st.markdown(f"### 🏢 {job['title']}")
                        st.markdown(f"- Company: {job['company_name']}")
                        st.markdown(f"- Location: {job['candidate_required_location']}")
                        st.markdown(f"- [🔗 Job Link]({job['url']})")

                        if st.button(f"✉️ Generate Cover Letter for {job['title']}", key=job['id']):
                            with st.spinner("Writing cover letter..."):
                                cover_letter = generate_cover_letter(
                                    name=user_name,
                                    background=background,
                                    job_title=job['title'],
                                    company_name=job['company_name'],
                                    language=language
                                )
                                st.markdown("#### 📄 AI-Generated Cover Letter:")
                                st.code(cover_letter, language="markdown")

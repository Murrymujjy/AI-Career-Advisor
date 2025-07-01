# job_finder.py

import streamlit as st
import requests
from advisor_logic import generate_cover_letter  # Reuse your AI logic

def job_finder_page():
    st.title("🔍 Job Finder & Auto Apply")
    st.write("Search for jobs and generate tailored cover letters!")

    query = st.text_input("Enter job title or keyword")
    location = st.text_input("Enter preferred location (optional)")
    remote = st.selectbox("Remote jobs?", ["Yes", "No", "Any"], index=0)

    if st.button("Search Jobs"):
        with st.spinner("Searching for jobs..."):
            jobs = search_jobs_remotive(query, location, remote)
        if not jobs:
            st.error("No jobs found.")
            return

        for i, job in enumerate(jobs):
            with st.expander(f"📌 {job['title']} at {job['company_name']}"):
                st.markdown(f"**Location:** {job['candidate_required_location']}")
                st.markdown(f"**Category:** {job['category']}")
                st.markdown(f"[Apply Here]({job['url']})")

                if st.button(f"✍️ Generate Cover Letter for Job {i+1}"):
                    with st.spinner("Generating cover letter..."):
                        cover_letter = generate_cover_letter(
                            job_title=job["title"],
                            company_name=job["company_name"],
                            description=job["description"]
                        )
                        st.text_area("📄 Cover Letter", cover_letter, height=300)

# Helper function to call Remotive API
def search_jobs_remotive(query, location, remote):
    url = "https://remotive.io/api/remote-jobs"
    params = {"search": query}
    if location:
        params["location"] = location
    try:
        res = requests.get(url, params=params)
        jobs = res.json().get("jobs", [])

        # Filter remote if needed
        if remote == "Yes":
            jobs = [job for job in jobs if "Remote" in job.get("job_type", "")]
        elif remote == "No":
            jobs = [job for job in jobs if "Remote" not in job.get("job_type", "")]

        return jobs[:5]  # limit results
    except Exception as e:
        st.error(f"API Error: {e}")
        return []

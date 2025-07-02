import streamlit as st
import requests
from advisor_logic import generate_cover_letter

def show():
    st.title("🔍 Job Finder & Auto Apply")
    st.markdown("Search for remote jobs and get a tailored cover letter.")

    # Job search form
    with st.form("job_search_form"):
        job_title = st.text_input("Job Title", "Machine Learning Engineer")
        location = st.text_input("Preferred Location (optional)", "")
        keywords = st.text_input("Keywords (comma-separated, optional)", "")
        submit_job_search = st.form_submit_button("Search Jobs")

    if submit_job_search:
        st.info("Searching for jobs...")

        # Remotive API URL
        remotive_url = f"https://remotive.io/api/remote-jobs?search={job_title}"
        try:
            res = requests.get(remotive_url)
            jobs = res.json().get("jobs", [])

            if jobs:
                st.success(f"Found {len(jobs)} job(s).")
                for job in jobs[:10]:
                    with st.expander(f"{job['title']} at {job['company_name']}"):
                        st.write(f"**Location:** {job['candidate_required_location']}")
                        st.write(f"**Category:** {job['category']}")
                        st.write(f"**Published:** {job['publication_date']}")
                        st.write(job['description'][:500] + "...")
                        apply_url = job.get("url")

                        # Cover letter generation form inside each job
                        with st.form(f"cover_letter_form_{job['id']}"):
                            user_name = st.text_input("Your Name", key=f"name_{job['id']}")
                            user_background = st.text_area("Your Background", key=f"background_{job['id']}")
                            user_skills = st.text_area("Relevant Skills or Experience", key=f"skills_{job['id']}")
                            submit_cover = st.form_submit_button("Generate Cover Letter")

                        if submit_cover:
                            with st.spinner("Generating tailored cover letter..."):
                                prompt = f"Write a professional cover letter for the role '{job['title']}' at {job['company_name']}. Candidate name is {user_name}. Background: {user_background}. Relevant experience: {user_skills}."
                                cover_letter = generate_cover_letter(prompt)
                                st.success("Cover letter generated!")
                                st.code(cover_letter, language="markdown")

                            if apply_url:
                                st.markdown(f"[Go to Job Page and Apply]({apply_url})", unsafe_allow_html=True)

            else:
                st.warning("No jobs found for the specified title.")

        except Exception as e:
            st.error(f"Error fetching jobs: {str(e)}")

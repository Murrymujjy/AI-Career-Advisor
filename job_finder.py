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
                            user_email = st.text_input("Your Email", key=f"email_{job['id']}")
                            user_background = st.text_area("Your Background", key=f"background_{job['id']}")
                            user_skills = st.text_area("Relevant Skills or Experience", key=f"skills_{job['id']}")
                            submit_cover = st.form_submit_button("Generate Cover Letter")

                        if submit_cover:
                            if not user_name or not user_email or not user_background or not user_skills:
                                st.warning("⚠️ Please fill in all the fields.")
                            else:
                                with st.spinner("Generating tailored cover letter..."):
                                    try:
                                        job_desc = job['description']
                                        cover_letter = generate_cover_letter(
                                            name=user_name,
                                            email=user_email,
                                            role=job['title'],
                                            company=job['company_name'],
                                            job_desc=job_desc,
                                            tone="Professional",
                                            language="English"
                                        )
                                        st.success("✅ Cover letter generated!")
                                        st.text_area("📄 Your Cover Letter", value=cover_letter, height=400)

                                        if apply_url:
                                            st.markdown(f"[🔗 Go to Job Page and Apply]({apply_url})", unsafe_allow_html=True)
                                    except Exception as e:
                                        st.error(f"❌ Error: {e}")
            else:
                st.warning("No jobs found for the specified title.")

        except Exception as e:
            st.error(f"❌ Error fetching jobs: {str(e)}")

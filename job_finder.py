import streamlit as st

def show():
    st.title("🧭 Job Finder & Auto Apply")
    st.markdown("Find your dream job and apply directly with AI support!")

    st.markdown("### 🔍 Search for a Job")
    job_query = st.text_input("Enter a job title, keyword, or role", placeholder="e.g. Data Analyst, Remote Developer")
    language = st.selectbox("Preferred Language", ["English", "French", "Spanish", "Yoruba", "Hausa", "Igbo"])

    if job_query:
        search_term = job_query.replace(" ", "+")
        st.markdown("### 🌐 Explore Job Boards")

        job_links = {
            "LinkedIn Jobs": f"https://www.linkedin.com/jobs/search/?keywords={search_term}",
            "Google Jobs": f"https://www.google.com/search?q={search_term}+jobs",
            "Upwork": f"https://www.upwork.com/search/jobs/?q={search_term}",
            "Remotive (Remote Jobs)": f"https://remotive.io/remote-jobs/search?search={search_term}",
            "Indeed Jobs": f"https://www.indeed.com/jobs?q={search_term}",
            "Jobberman Nigeria": f"https://www.jobberman.com/jobs?q={search_term}"
        }

        for platform, link in job_links.items():
            st.markdown(f"- 🔗 [{platform}]({link})", unsafe_allow_html=True)
        
        st.success("Click on any platform to explore relevant job listings!")

        st.markdown("---")
        st.info("💡 After finding a job, go to the **Cover Letter Generator** tab to create a personalized application letter.")

    else:
        st.markdown("👆 Enter a job title above to begin your search.")
        st.warning("No job keyword entered yet.")

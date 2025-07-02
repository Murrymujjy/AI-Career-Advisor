import streamlit as st
from streamlit_option_menu import option_menu

# Modular imports
from career_advice import show as show_career_advice
from resume_builder import show as show_resume_builder
from cover_letter import show as show_cover_letter
from job_finder import show as show_job_finder

# Page config
st.set_page_config(page_title="AI Career Advisor", page_icon="💼")

# Sidebar
st.sidebar.title("💼 AI Career Advisor")
section = st.sidebar.radio(
    "Navigate", 
    ["Career Advice", "Resume Builder", "Cover Letter Generator", "Job Finder & Auto Apply"]
)

# Header
st.title("💼 AI Career Advisor")
st.markdown("Get personalized career support powered by AI via Hugging Face.")

# Load each modular component
if section == "Career Advice":
    show_career_advice()

elif section == "Resume Builder":
    show_resume_builder()

elif section == "Cover Letter Generator":
    show_cover_letter()

elif section == "Job Finder & Auto Apply":
    show_job_finder()

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

# cover_letter.py

import streamlit as st
from cover_letter_logic import generate_cover_letter  # or advisor_logic if that's where your function lives

def show():
    st.subheader("✍️ Cover Letter Generator")

    name = st.text_input("Your Name", key="cover_name")
    email = st.text_input("Your Email", key="cover_email")
    job_title = st.text_input("Job Title", placeholder="e.g. Data Scientist")
    company_name = st.text_input("Company Name", placeholder="e.g. Google")
    job_description = st.text_area("Job Description")
    tone = st.selectbox("Tone of Letter", ["Professional", "Friendly", "Passionate"], index=0)
    language = st.selectbox("Language", ["English", "French", "Spanish", "Yoruba", "Hausa", "Igbo"], index=0)

    if st.button("Generate Cover Letter"):
        if not all([name, email, job_title, company_name, job_description]):
            st.warning("⚠️ Please fill in all fields.")
        else:
            with st.spinner("Generating your cover letter..."):
                try:
                    letter = generate_cover_letter(
                        name=name,
                        email=email,
                        job_title=job_title,
                        company_name=company_name,
                        job_description=job_description,
                        tone=tone,
                        language=language,
                    )
                    st.success("✅ Cover letter generated!")
                    st.text_area("📄 Your Cover Letter", letter, height=400)
                except Exception as e:
                    st.error(f"❌ Error: {e}")

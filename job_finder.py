# job_finder.py

import streamlit as st
import requests
import datetime
import os
from fpdf import FPDF
from docx import Document
from huggingface_hub import InferenceClient

st.set_page_config(page_title="Job Finder & Auto Apply", layout="centered")

HF_TOKEN = st.secrets["HF_TOKEN"]

client = InferenceClient(
    provider="novita",
    api_key=HF_TOKEN,
)

# Generate AI-powered cover letter
def generate_cover_letter(name, email, job_title, company_name, job_description, tone="Professional", language="English"):
    prompt = f"""
    You are a professional career assistant helping a candidate write a personalized cover letter.

    Candidate Information:
    - Name: {name}
    - Email: {email}

    Job Information:
    - Title: {job_title}
    - Company: {company_name}
    - Description: {job_description}

    Tone: {tone}
    Language: {language}

    Instructions:
    Write a concise, tailored, and engaging cover letter suitable for a professional job application. Address it to the company and show alignment with the job description. End with a call to action.
    """
    response = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-R1-0528",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1024,
    )
    return response.choices[0].message.content.strip()

def generate_pdf(content, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in content.split("\n"):
        pdf.multi_cell(0, 10, line)
    path = os.path.join("/tmp", filename)
    pdf.output(path)
    return path

def generate_word(content, filename):
    doc = Document()
    for line in content.split("\n"):
        doc.add_paragraph(line)
    path = os.path.join("/tmp", filename)
    doc.save(path)
    return path

# UI
def show():
    st.subheader("🔍 Job Finder & Auto Apply")
    search_term = st.text_input("Enter job title or keyword", placeholder="e.g. machine learning, data scientist")
    location = st.text_input("Location preference (optional)", placeholder="e.g. remote, US, Nigeria")

    if st.button("🔎 Search Jobs"):
        if not search_term:
            st.warning("Please enter a job title or keyword.")
        else:
            with st.spinner("Searching for jobs..."):
                remotive_url = f"https://remotive.io/api/remote-jobs?search={search_term}"
                response = requests.get(remotive_url)
                if response.status_code == 200:
                    jobs = response.json()["jobs"]
                    if location:
                        jobs = [job for job in jobs if location.lower() in job["candidate_required_location"].lower()]
                    if not jobs:
                        st.info("No jobs found with this search.")
                    else:
                        for job in jobs[:5]:  # Show top 5
                            st.markdown(f"### {job['title']} at {job['company_name']}")
                            st.markdown(f"📍 Location: {job['candidate_required_location']}")
                            st.markdown(f"📝 [Job Link]({job['url']})", unsafe_allow_html=True)
                            with st.expander("🧠 Generate Cover Letter for this Job"):
                                name = st.text_input("Your Name", key=f"name_{job['id']}")
                                email = st.text_input("Your Email", key=f"email_{job['id']}")
                                tone = st.selectbox("Tone", ["Professional", "Friendly", "Passionate"], key=f"tone_{job['id']}")
                                language = st.selectbox("Language", ["English", "French", "Spanish", "Yoruba", "Hausa", "Igbo"], key=f"lang_{job['id']}")

                                if st.button("✉️ Generate Cover Letter", key=f"generate_{job['id']}"):
                                    if not name or not email:
                                        st.warning("Please fill in your name and email.")
                                    else:
                                        with st.spinner("Generating cover letter..."):
                                            try:
                                                cover_letter = generate_cover_letter(
                                                    name, email, job["title"], job["company_name"], job["description"], tone, language
                                                )
                                                st.success("Cover letter generated!")
                                                st.text_area("📄 Your Cover Letter", cover_letter, height=300)

                                                timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                                                pdf_file = generate_pdf(cover_letter, f"cover_letter_{timestamp}.pdf")
                                                word_file = generate_word(cover_letter, f"cover_letter_{timestamp}.docx")

                                                with open(pdf_file, "rb") as f:
                                                    st.download_button("📥 Download as PDF", f, file_name=os.path.basename(pdf_file), mime="application/pdf")

                                                with open(word_file, "rb") as f:
                                                    st.download_button("📥 Download as Word", f, file_name=os.path.basename(word_file), mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

                                                st.markdown(f"[🔗 Apply on Remotive]({job['url']})", unsafe_allow_html=True)
                                                linkedin_search = f"https://www.linkedin.com/jobs/search/?keywords={job['title']}+{job['company_name']}"
                                                st.markdown(f"[🔗 Apply on LinkedIn]({linkedin_search})", unsafe_allow_html=True)

                                            except Exception as e:
                                                st.error(f"❌ Error generating letter: {e}")
                else:
                    st.error("Failed to fetch jobs from Remotive.")


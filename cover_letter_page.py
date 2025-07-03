# cover_letter_page.py

from huggingface_hub import InferenceClient
import streamlit as st
from fpdf import FPDF
from docx import Document
import os
import datetime

# Load HF token securely from Streamlit secrets
HF_TOKEN = st.secrets["HF_TOKEN"]

# Initialize client
client = InferenceClient(
    provider="novita",
    api_key=HF_TOKEN,
)

# AI cover letter generation function
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


# Helper to generate PDF
def generate_pdf(content, filename="cover_letter.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in content.split("\n"):
        pdf.multi_cell(0, 10, line)
    output_path = os.path.join("/tmp", filename)
    pdf.output(output_path)
    return output_path

# Helper to generate Word document
def generate_word(content, filename="cover_letter.docx"):
    doc = Document()
    for line in content.split("\n"):
        doc.add_paragraph(line)
    output_path = os.path.join("/tmp", filename)
    doc.save(output_path)
    return output_path

# Streamlit UI
def show():
    st.subheader("✍️ AI Cover Letter Generator")

    name = st.text_input("Your Name", placeholder="e.g. Mujeebat Muritala")
    email = st.text_input("Your Email", placeholder="e.g. murrymujjy@gmail.com")
    job_title = st.text_input("Target Job Title", placeholder="e.g. Data Scientist")
    company = st.text_input("Company Name", placeholder="e.g. Google")
    job_description = st.text_area("Job Description", placeholder="Paste the job description here.")
    tone = st.selectbox("Tone", ["Professional", "Friendly", "Passionate", "Formal", "Concise"])
    language = st.selectbox("Language", ["English", "French", "Spanish", "Yoruba", "Hausa", "Igbo"])

    apply_option = st.radio("Auto-Apply Option", ["None", "LinkedIn", "Remotive (with URL)"])
    apply_url = ""
    if apply_option == "Remotive (with URL)":
        apply_url = st.text_input("Paste Remotive Apply URL")

    if st.button("✉️ Generate Cover Letter"):
        if not all([name, email, job_title, company, job_description]):
            st.warning("⚠️ Please fill in all the fields.")
        else:
            with st.spinner("Generating your cover letter..."):
                try:
                    letter = generate_cover_letter(name, email, job_title, company, job_description, tone, language)
                    st.success("✅ Cover letter generated!")
                    st.text_area("📄 Your Cover Letter", letter, height=500)

                    # Create unique filenames
                    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                    pdf_file = generate_pdf(letter, f"cover_letter_{timestamp}.pdf")
                    word_file = generate_word(letter, f"cover_letter_{timestamp}.docx")

                    # Download buttons
                    with open(pdf_file, "rb") as f:
                        st.download_button("📥 Download as PDF", f, file_name=os.path.basename(pdf_file), mime="application/pdf")

                    with open(word_file, "rb") as f:
                        st.download_button("📥 Download as Word", f, file_name=os.path.basename(word_file), mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

                    # Apply Now button
                    if apply_option == "LinkedIn":
                        search_url = f"https://www.linkedin.com/jobs/search/?keywords={job_title}+{company}"
                        st.markdown(f"[🔗 Apply Now on LinkedIn]({search_url})", unsafe_allow_html=True)

                    elif apply_option == "Remotive (with URL)" and apply_url:
                        st.markdown(f"[🔗 Apply Now on Remotive]({apply_url})", unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"❌ Error: {e}")

# resume_builder.py

from huggingface_hub import InferenceClient 
import streamlit as st
from fpdf import FPDF
import os

# Load Hugging Face token securely
HF_TOKEN = st.secrets["HF_TOKEN"]

# Initialize Inference Client
client = InferenceClient(
    provider="novita",
    api_key=HF_TOKEN,
)

# Generate resume text using LLM
def generate_resume(name, background, interests):
    prompt = f"""
    You are a professional resume writer. Create a resume for the following person:

    Name: {name}
    Background: {background}
    Career Goals / Interests: {interests}

    The resume should include:
    - Objective
    - Education
    - Skills
    - Experience
    - Achievements (if any)

    Make it clean, formal, and well-structured in plain text format.
    """

    response = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-R1-0528",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        max_tokens=1024,
    )

    return response.choices[0].message.content.strip()

# Helper to convert text resume to downloadable PDF
def generate_pdf(text, filename="resume.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for line in text.split("\n"):
        pdf.multi_cell(0, 10, line)

    output_path = os.path.join("/tmp", filename)
    pdf.output(output_path)
    return output_path

# Streamlit UI
def show():
    st.subheader("📄 AI Resume Builder")

    name = st.text_input("Your Full Name", placeholder="e.g. Alexander Success")
    background = st.text_area("Your Academic/Professional Background", placeholder="e.g. BSc in Chemical Engineering, Machine Learning enthusiast...")
    interests = st.text_area("Career Interests / Goals", placeholder="e.g. Data Science, AI in healthcare, Nuclear engineering...")

    if st.button("✨ Generate Resume"):
        if not name or not background or not interests:
            st.warning("Please fill in all fields before generating your resume.")
        else:
            with st.spinner("Generating your resume..."):
                try:
                    resume = generate_resume(name, background, interests)
                    st.success("✅ Resume generated!")
                    st.text_area("📋 Your Resume", resume, height=500)

                    # Convert to PDF
                    pdf_path = generate_pdf(resume)
                    with open(pdf_path, "rb") as pdf_file:
                        st.download_button(
                            label="📥 Download Resume as PDF",
                            data=pdf_file,
                            file_name="resume.pdf",
                            mime="application/pdf"
                        )
                except Exception as e:
                    st.error(f"❌ Error: {e}")

# resume_builder.py

import streamlit as st
from huggingface_hub import InferenceClient
from fpdf import FPDF
import os

# Load Hugging Face token securely
HF_TOKEN = st.secrets["HF_TOKEN"]

# Initialize Hugging Face client
client = InferenceClient(
    provider="novita",
    api_key=HF_TOKEN,
)

# Generate resume using LLM
def generate_resume(name, background, interests, format_type, certifications, languages, references):
    extra_sections = ""
    if certifications:
        extra_sections += f"\nCertifications:\n- {certifications}"
    if languages:
        extra_sections += f"\nLanguages:\n- {languages}"
    if references:
        extra_sections += f"\nReferences:\n{references}"

    prompt = f"""
    You are a professional resume writer. Create a {format_type.lower()} resume for the following candidate:

    Name: {name}
    Background: {background}
    Career Interests: {interests}

    Include sections:
    - Objective
    - Education
    - Skills
    - Experience
    - Achievements

    {extra_sections}

    Write the resume in clean, professional, plain text format.
    """

    response = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-R1-0528",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        max_tokens=1024,
    )

    return response.choices[0].message.content.strip()

# Create a PDF from text
def generate_pdf(text, filename="resume.pdf", profile_image=None):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    if profile_image is not None:
        try:
            pdf.image(profile_image, x=160, y=10, w=30)
            pdf.ln(30)  # Add space below image
        except:
            pass  # Ignore image errors

    for line in text.split("\n"):
        pdf.multi_cell(0, 10, line.encode("latin-1", "replace").decode("latin-1"))

    output_path = os.path.join("/tmp", filename)
    pdf.output(output_path)
    return output_path

# Streamlit UI
def show():
    st.subheader("📄 AI Resume Builder")

    name = st.text_input("Your Full Name", placeholder="e.g. Alexander Success")
    background = st.text_area("Academic/Professional Background", placeholder="BSc in Physics, AI Research Assistant...")
    interests = st.text_area("Career Interests / Goals", placeholder="Data Science, AI in Healthcare, etc.")

    format_type = st.selectbox("Choose Resume Style", ["Modern", "Creative", "ATS-Friendly"])
    profile_image = st.file_uploader("Upload Profile Picture (Optional)", type=["jpg", "jpeg", "png"])

    with st.expander("➕ Add Optional Sections"):
        certifications = st.text_area("Certifications", placeholder="e.g. Google Data Analytics, PMP...")
        languages = st.text_input("Languages Spoken", placeholder="e.g. English, French, Yoruba")
        references = st.text_area("References", placeholder="e.g. Dr. James Doe, CEO at AI Labs...")

    if st.button("✨ Generate Resume"):
        if not name or not background or not interests:
            st.warning("Please fill in the required fields.")
        else:
            with st.spinner("Generating your resume..."):
                try:
                    resume_text = generate_resume(name, background, interests, format_type, certifications, languages, references)
                    st.success("✅ Resume generated!")
                    st.text_area("📋 Your Resume", resume_text, height=500)

                    # Save profile image temporarily if uploaded
                    image_path = None
                    if profile_image is not None:
                        image_path = os.path.join("/tmp", profile_image.name)
                        with open(image_path, "wb") as f:
                            f.write(profile_image.read())

                    pdf_path = generate_pdf(resume_text, profile_image=image_path)
                    with open(pdf_path, "rb") as pdf_file:
                        st.download_button(
                            label="📥 Download Resume as PDF",
                            data=pdf_file,
                            file_name="resume.pdf",
                            mime="application/pdf"
                        )
                except Exception as e:
                    st.error(f"❌ Error: {e}")

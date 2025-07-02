# cover_letter.py

from huggingface_hub import InferenceClient
import streamlit as st

# Load HF token securely from Streamlit secrets
HF_TOKEN = st.secrets["HF_TOKEN"]

# Create Hugging Face InferenceClient using Novita provider
client = InferenceClient(
    provider="novita",
    api_key=HF_TOKEN,
)

# Function to generate cover letter using AI
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


# Streamlit UI
def show():
    st.subheader("✍️ AI Cover Letter Generator")

    name = st.text_input("Your Name", placeholder="e.g. Mujeebat Muritala")
    email = st.text_input("Your Email", placeholder="e.g. murrymujjy@gmail.com")
    job_title = st.text_input("Target Job Title", placeholder="e.g. Data Scientist")
    company = st.text_input("Company Name", placeholder="e.g. Google")
    job_description = st.text_area("Job Description", placeholder="Paste the job description here.")
    tone = st.selectbox("Tone", ["Professional", "Friendly", "Passionate"])
    language = st.selectbox("Language", ["English", "French", "Spanish", "Yoruba", "Hausa", "Igbo"])

    if st.button("✉️ Generate Cover Letter"):
        if not all([name, email, job_title, company, job_description]):
            st.warning("⚠️ Please fill in all the fields.")
        else:
            with st.spinner("Generating your cover letter..."):
                try:
                    letter = generate_cover_letter(name, email, job_title, company, job_description, tone, language)
                    st.success("✅ Cover letter generated!")
                    st.text_area("📄 Your Cover Letter", letter, height=500)
                except Exception as e:
                    st.error(f"❌ Error: {e}")

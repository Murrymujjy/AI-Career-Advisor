from huggingface_hub import InferenceClient
import streamlit as st

# Load HF token securely from Streamlit secrets
HF_TOKEN = st.secrets["HF_TOKEN"]

# Create Hugging Face InferenceClient using Novita provider
client = InferenceClient(
    provider="novita",
    api_key=HF_TOKEN,
)

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

    # Send to Hugging Face model
    response = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-R1-0528",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1024,
    )

    return response.choices[0].message.content.strip()

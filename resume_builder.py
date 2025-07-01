from huggingface_hub import InferenceClient
import streamlit as st

# Load Hugging Face token securely from Streamlit secrets
HF_TOKEN = st.secrets["HF_TOKEN"]

# Initialize Hugging Face InferenceClient
client = InferenceClient(
    provider="novita",
    api_key=HF_TOKEN,
)

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

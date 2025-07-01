# advisor_logic.py

import os
from huggingface_hub import InferenceClient

# Setup Hugging Face Inference Client (replace "novita" if needed)
client = InferenceClient(
    provider="novita",
    api_key=os.environ.get("HF_TOKEN")
)

def generate_career_advice(name, background, interests, language="English"):
    prompt = f"""
    You are an AI Career Advisor. Help {name} with career advice.
    Background: {background}
    Interests: {interests}
    Respond in {language}.
    """

    response = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-R1-0528",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


def generate_cover_letter(name, email, role, company, job_desc, tone="Professional", language="English"):
    prompt = f"""
    Generate a {tone.lower()} cover letter for {name} ({email}) applying for the role of {role} at {company}.
    Job Description: {job_desc}
    Respond in {language}.
    """

    response = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-R1-0528",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

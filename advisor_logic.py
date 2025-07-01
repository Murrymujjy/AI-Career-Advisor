# advisor_logic.py

import requests

def generate_cover_letter(name, background, job_title, company_name, language="English (US)"):
    prompt = f"""
    You are an AI assistant helping write a personalized cover letter.

    Candidate Name: {name}
    Background: {background}
    Job Title: {job_title}
    Company: {company_name}
    Language: {language}

    Write a professional cover letter tailored to this job. The tone should be confident and polite.
    """

    # LM Studio local server
    response = requests.post(
        "http://localhost:1234/v1/chat/completions",
        headers={"Content-Type": "application/json"},
        json={
            "model": "local-model",  # Replace with your running model ID
            "messages": [
                {"role": "system", "content": "You are a helpful AI career assistant."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 700
        }
    )

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return "❌ Failed to generate cover letter."

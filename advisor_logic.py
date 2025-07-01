# advisor_logic.py

import requests

LLM_URL = "http://localhost:1234/v1/chat/completions"
MODEL_NAME = "local-model"  # Replace with the model you're running in LM Studio, e.g., "llama3"

def generate_career_advice(name, background, interests, language="English"):
    prompt = f"""
    You are an AI career advisor.

    Candidate Name: {name}
    Background: {background}
    Interests: {interests}
    Preferred Language: {language}

    Give concise, personalized career advice in bullet points. Be supportive, insightful, and clear.
    """

    response = requests.post(
        LLM_URL,
        headers={"Content-Type": "application/json"},
        json={
            "model": MODEL_NAME,
            "messages": [
                {"role": "system", "content": "You are a helpful career advisor."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 700
        }
    )

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return "❌ Failed to generate career advice."


def generate_cover_letter(name, background, job_title, company_name, language="English"):
    prompt = f"""
    You are an AI assistant helping write a personalized cover letter.

    Candidate Name: {name}
    Background: {background}
    Job Title: {job_title}
    Company: {company_name}
    Language: {language}

    Write a professional cover letter tailored to this job. The tone should be confident and polite.
    """

    response = requests.post(
        LLM_URL,
        headers={"Content-Type": "application/json"},
        json={
            "model": MODEL_NAME,
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

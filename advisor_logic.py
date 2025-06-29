import os
import openai

# Set your OpenRouter API key and base URL
openai.api_key = os.getenv("OPENROUTER_API_KEY")
openai.base_url = "https://openrouter.ai/api/v1"

def generate_career_advice(prompt: str) -> str:
    response = openai.ChatCompletion.create(
        model="openai/gpt-3.5-turbo",  # You can use other models like "mistralai/mistral-7b", "google/gemini-pro", etc.
        messages=[
            {"role": "system", "content": "You are a professional career advisor."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=600
    )
    return response.choices[0].message["content"].strip()

def generate_cover_letter(prompt: str) -> str:
    response = openai.ChatCompletion.create(
        model="openai/gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a professional cover letter writer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=600
    )
    return response.choices[0].message["content"].strip()

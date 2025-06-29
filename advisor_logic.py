import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI client with OpenRouter settings
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

def generate_career_advice(prompt: str) -> str:
    response = client.chat.completions.create(
        model="openrouter/openai/gpt-3.5-turbo",  # Or another OpenRouter-supported model
        messages=[
            {"role": "system", "content": "You are a professional career advisor."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=600
    )
    return response.choices[0].message.content.strip()

def generate_cover_letter(prompt: str) -> str:
    response = client.chat.completions.create(
        model="openrouter/openai/gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a professional cover letter writer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=600
    )
    return response.choices[0].message.content.strip()

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Set up OpenRouter-compatible client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")  # Ensure this is set in .env or environment
)

def generate_career_advice(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # ✅ Use plain name only
        messages=[
            {"role": "system", "content": "You are a supportive AI career coach. Respond with clear, practical advice."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=600
    )
    return response.choices[0].message.content.strip()

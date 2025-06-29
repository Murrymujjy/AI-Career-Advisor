import openai
import os

# ✅ Set OpenRouter API base and key
openai.api_base = "https://openrouter.ai/api/v1"
openai.api_key = os.getenv("OPENROUTER_API_KEY")  # or paste key directly (not recommended for prod)

# ✅ Supported models (pick one)
DEFAULT_MODEL = "mistralai/mixtral-8x7b"  # good free one
# "meta-llama/llama-3-70b-instruct" also works

def generate_career_advice(prompt: str):
    try:
        response = openai.ChatCompletion.create(
            model=DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": "You are a professional career advisor. Provide detailed, helpful, and clear career guidance."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )

        # ✅ Check structure
        if hasattr(response, "choices"):
            return response.choices[0].message.content.strip()
        else:
            return "❌ Invalid response: No choices field in response."

    except Exception as e:
        return f"❌ Error generating career advice: {e}"


def generate_cover_letter(prompt: str):
    try:
        response = openai.ChatCompletion.create(
            model=DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": "You are a professional cover letter writer. Write in a clear, professional tone."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6,
        )

        if hasattr(response, "choices"):
            return response.choices[0].message.content.strip()
        else:
            return "❌ Invalid response: No choices field in response."

    except Exception as e:
        return f"❌ Error generating cover letter: {e}"

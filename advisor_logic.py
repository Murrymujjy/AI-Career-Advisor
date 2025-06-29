import os
import openai

# ✅ Correct setup for new openai>=1.0.0
openai.api_key = os.getenv("OPENAI_API_KEY")

language_prefix = {
    "en": "",
    "en-GB": "Use British English.",
    "fr": "Répondez en français.",
    "yo": "Jọwọ dahun ni ede Yorùbá.",
    "ha": "Da amsa a cikin harshen Hausa.",
    "ig": "Biko, zaa azịza ya na asụsụ Igbo.",
    "es": "Responde en español.",
    "ar": "يرجى الرد باللغة العربية."
}


def generate_career_advice(name, background, interests, goals, lang_code):
    prefix = language_prefix.get(lang_code, "")
    prompt = f"""{prefix}
You are an AI Career Advisor. Provide a personalized, encouraging career guidance for this user:

Name: {name}
Background: {background}
Interests: {interests}
Goals: {goals}

Give 2–3 career suggestions, required skills, and steps they can take. Keep it simple and motivating.
"""

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # fallback if gpt-4 isn't available
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        # ✅ Debug logs
        print("DEBUG TYPE:", type(response))
        print("DEBUG RESPONSE:", response)

        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Error generating career advice: {e}"



def generate_cover_letter(name, email, role, company, job_description, tone, lang_code):
    prefix = language_prefix.get(lang_code, "")
    tone_text = "professional and formal" if tone == "Formal" else "friendly and casual"

    prompt = f"""{prefix}
Write a {tone_text} cover letter for this job application:

- Name: {name}
- Email: {email}
- Job Role: {role}
- Company: {company}
- Job Description: {job_description}

Structure: 3 paragraphs. Show enthusiasm, fit for the role, and a nice closing.
"""

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # safer than gpt-4
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        print("DEBUG TYPE:", type(response))  # Should be <class 'openai.types.chat.chat_completion.ChatCompletion'>
        print("DEBUG RESPONSE:", response)
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Error generating cover letter: {e}"


# advisor_logic.py

from openai import OpenAI
from translate import translate_text  # Custom function from utils.py or translation module

client = OpenAI()  # Assumes your OPENAI_API_KEY is set in environment

# Language prompts
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
    prompt = f"""
{prefix}
I am building a multilingual AI Career Advisor. Give a detailed yet friendly career guidance to a user based on the following:

Name: {name}
Background: {background}
Interests: {interests}
Goals: {goals}

Please offer 2–3 suggested career paths, required skills, and next steps. Make it helpful and encouraging.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Error generating career advice: {e}"


def generate_cover_letter(name, email, role, company, job_description, tone, lang_code):
    prefix = language_prefix.get(lang_code, "")
    tone_text = "professional and formal" if tone == "Formal" else "friendly and casual"

    prompt = f"""
{prefix}
I need a {tone_text} cover letter in the selected language for a job application.

Here are the details:
Name: {name}
Email: {email}
Job Role: {role}
Company: {company}
Job Description: {job_description}

Make the letter 3 paragraphs long. Include enthusiasm, how the user fits the role, and a nice closing.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Error generating cover letter: {e}"

from googletrans import Translator
from openai import OpenAI
import os

# Load your OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")

translator = Translator()

def translate_text(text, target_lang):
    try:
        translated = translator.translate(text, dest=target_lang)
        return translated.text
    except Exception:
        return text

def generate_career_advice(name, background, interests, goals, lang_code):
    prompt = f"""
    You are an expert career advisor.
    A user named {name} has the following profile:
    - Background: {background}
    - Interests: {interests}
    - Career Goals: {goals}

    Provide a personalized career advice in simple language. Use bullet points and be concise.
    """
    
    # Call OpenAI
    client = OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert career advisor."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7
    )
    result = response.choices[0].message.content.strip()
    return translate_text(result, lang_code)

def generate_cover_letter(name, email, role, company, job_description, tone, lang_code):
    prompt = f"""
    Write a {tone.lower()} cover letter for the job role of '{role}' at {company}.
    The applicant's name is {name} and email is {email}.
    The job description is:
    {job_description}

    Keep it to 3–4 paragraphs. Highlight alignment with job description and express enthusiasm.
    """
    
    client = OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert cover letter writer."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7
    )
    result = response.choices[0].message.content.strip()
    return translate_text(result, lang_code)

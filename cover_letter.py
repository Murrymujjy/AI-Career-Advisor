import requests

def generate_cover_letter(name, background, interests, job_title=None, company_name=None, job_description=None):
    if job_title and company_name:
        prompt = f"""
        Write a personalized cover letter for a job application.

        Candidate:
        - Name: {name}
        - Background: {background}
        - Interests: {interests}

        Job Posting:
        - Title: {job_title}
        - Company: {company_name}
        - Description: {job_description or 'N/A'}

        The letter should be concise, professional, engaging, and tailored to the job and company.
        """
    else:
        prompt = f"""
        Write a general personalized cover letter.

        Candidate:
        - Name: {name}
        - Background: {background}
        - Interests: {interests}

        Make it concise, professional, and engaging.
        """

    response = requests.post(
        "http://localhost:1234/v1/chat/completions",
        headers={"Content-Type": "application/json"},
        json={
            "model": "llama3",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 800,
        },
    )

    return response.json()["choices"][0]["message"]["content"]

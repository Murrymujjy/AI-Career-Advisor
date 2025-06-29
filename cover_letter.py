import requests

def generate_cover_letter(name, background, interests):
    prompt = f"""
    Write a personalized cover letter for:
    Name: {name}
    Background: {background}
    Career Interests: {interests}

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

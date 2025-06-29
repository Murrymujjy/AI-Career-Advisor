import requests

def generate_resume(name, background, interests):
    prompt = f"""
    Generate a professional resume for:
    Name: {name}
    Background: {background}
    Career Goals: {interests}

    Format it with headers like Objective, Education, Skills, and Experience.
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

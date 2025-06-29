import requests

def generate_career_advice(name, background, interests, language="English"):
    prompt = f"""
    You are a professional career advisor AI.
    User Name: {name}
    Background: {background}
    Interests/Career Goals: {interests}
    Preferred Language: {language}

    Provide personalized, practical career advice in {language}.
    """
    response = requests.post(
        "http://localhost:1234/v1/chat/completions",
        headers={"Content-Type": "application/json"},
        json={
            "model": "local-model",  # Replace with your LM Studio model name
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 800,
        },
    )
    return response.json()["choices"][0]["message"]["content"]

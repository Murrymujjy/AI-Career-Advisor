# advisor_logic.py

from googletrans import Translator

def translate_text(text, target_lang):
    translator = Translator()
    try:
        translated = translator.translate(text, dest=target_lang)
        return translated.text
    except Exception as e:
        return f"❗ Translation error: {e}"

def generate_career_advice(name, background, interests, goals, language="en"):
    if not name or not background or not interests or not goals:
        return "Please fill in all fields to get personalized advice."

    # English advice template
    advice = f"""
Hi {name}! 👋

🎓 **Based on your Background**
Your background in {background} gives you a strong foundation to explore different paths. Highlight your key experiences and transferable skills when applying for roles.

💡 **Your Interests**
You're interested in {interests}, which are high-demand and future-forward areas. You can align your learning and job search around this.

🎯 **Your Career Goals**
Your goal of {goals} is inspiring! Let's break it down into achievable steps.

---

🛣️ **Career Paths to Explore**
- Data Analyst
- Product Manager
- Technical Writer
- UX Designer

🔧 **Recommended Skills to Learn**
- Python, SQL, and Excel
- Communication & problem-solving
- Public speaking & storytelling

📚 **Suggested Courses**
- [Coursera Career Foundations](https://www.coursera.org)
- [Google Career Certificates](https://grow.google/certificates/)
- [Udemy Interview Skills](https://www.udemy.com)
- [LinkedIn Learning Resume Help](https://www.linkedin.com/learning)

---

📋 **Next Steps**
- Tailor your resume to highlight relevant skills
- Connect with professionals on LinkedIn
- Prepare for behavioral & technical interviews

---

🗣️ **We Value Your Feedback!**
If you found this helpful or want to share how we can improve, feel free to email us.

Best wishes on your career journey! 🚀
"""

    # Translate if needed
    if language != "en":
        return translate_text(advice, target_lang=language)
    return advice

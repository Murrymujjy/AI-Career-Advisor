from googletrans import Translator

def translate_text(text, dest_language):
    try:
        translator = Translator()
        translated = translator.translate(text, dest=dest_language)
        return translated.text
    except Exception as e:
        return f"⚠️ Translation failed: {str(e)}"

def generate_career_advice(name, background, interests, goals, language='en'):
    if not name or not background or not interests or not goals:
        return "Please fill in all fields to get personalized advice."

    base_response = f"""
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
- [Coursera: Google Career Certificates](https://coursera.org)
- [LinkedIn Learning: Resume & LinkedIn Mastery](https://linkedin.com/learning)
- [Udemy: Interview Skills](https://udemy.com)

---

📋 **Next Steps**
- Tailor your resume to highlight relevant skills
- Connect with professionals on [LinkedIn](https://linkedin.com)
- Prepare for behavioral & technical interviews

---

🗣️ **We Value Your Feedback!**
If you found this helpful or want to share how we can improve, feel free to reach out send us an email: [murrymujjy@gmail.com](mailto:murrymujjy@gmail.com)
or leave your email!

Good luck on your career journey! 🚀
"""

    if language != 'en':
        return translate_text(base_response, dest_language=language)
    return base_response

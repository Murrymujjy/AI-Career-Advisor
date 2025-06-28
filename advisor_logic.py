from deep_translator import GoogleTranslator

def generate_career_advice(name, background, interests, goals, lang_code="en"):
    if not all([name, background, interests, goals]):
        return "Please fill in all fields to get personalized advice."

    base_response = f"""
Hi {name}! 👋

🎓 **Your Background**
Your background in {background} gives you a strong foundation. Be sure to highlight key skills and achievements.

💡 **Your Interests**
You're interested in {interests} — a fast-growing and exciting field! You can align your learning and job search with this.

🎯 **Your Career Goals**
Your goal of {goals} is inspiring. Let's break it into actionable steps:

---

🛠️ **Recommended Paths**
- Data Analyst
- Product Manager
- UX Designer
- AI Research Assistant

📘 **Courses to Explore**
- [Google Career Certificates](https://grow.google/certificates/)
- [Coursera AI Specializations](https://www.coursera.org)
- [LinkedIn Learning](https://www.linkedin.com/learning/)

📈 **Next Steps**
- Polish your CV and LinkedIn profile
- Build a small project portfolio
- Practice interview questions

---

We believe in your journey. 🚀 Best of luck!
"""

    # Auto-translate
    if lang_code != "en":
        translated = GoogleTranslator(source="auto", target=lang_code).translate(base_response)
        return translated

    return base_response

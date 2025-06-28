# advisor_logic.py

def generate_career_advice(name, background, interests, goals):
    if not name or not background or not interests or not goals:
        return "Please fill in all fields to get personalized advice."

    return f"""
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
- Coursera: Career Foundations, Google Career Certificates
- Udemy: Job Interview Skills Training
- LinkedIn Learning: Resume & LinkedIn Mastery

---

📋 **Next Steps**
- Tailor your resume to highlight relevant skills
- Connect with professionals on LinkedIn
- Prepare for behavioral & technical interviews

---

🗣️ **We Value Your Feedback!**
If you found this helpful or want to suggest improvements:

- 📧 [Email us](mailto:murrymujjy@gmail.com)
- 📝 [Fill out our feedback form](https://example.com/feedback-form) *(replace with your actual form URL)*

Best wishes on your career journey! 🚀
"""

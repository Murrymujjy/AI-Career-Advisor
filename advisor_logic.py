# advisor_logic.py

def generate_career_advice(name, background, interests, goals):
    if not name or not background or not interests or not goals:
        return "❗ Please fill in all fields to receive a personalized career plan."

    return f"""
## 👋 Hi {name}

---

### 🎓 Your Background
Your experience in **{background}** offers a solid foundation. Be sure to highlight relevant transferable skills and academic strengths.

---

### 💡 Your Interests
You're interested in **{interests}**, which are in-demand fields. Staying curious and continuously learning will set you apart.

Explore resources on:
- [Coursera](https://www.coursera.org/)
- [LinkedIn Learning](https://www.linkedin.com/learning/)
- [edX](https://www.edx.org/)

---

### 🎯 Your Goals
Your goal to **{goals}** is admirable. With a structured plan, it's definitely achievable. Consider mentorship platforms like:
- [ADPList](https://www.adplist.org/)
- [GrowthMentor](https://www.growthmentor.com/)

---

### 🛣️ Career Paths to Explore
Here are a few roles aligned with your background and interests:
- Data Analyst
- Product Manager
- Technical Writer
- UX Designer

---

### 🔧 Recommended Skills to Learn
- Python, SQL, Excel
- Communication & Critical Thinking
- Resume Writing & Storytelling

Learn via:
- [Google Career Certificates](https://grow.google/certificates/)
- [Udemy](https://www.udemy.com/)
- [LinkedIn Learning](https://www.linkedin.com/learning/)

---

### 📋 Next Steps
- ✅ Tailor your resume using [Canva Resume Templates](https://www.canva.com/resumes/)
- ✅ Connect with professionals via [LinkedIn](https://www.linkedin.com/)
- ✅ Practice with [Interviewing.io](https://interviewing.io/) or [Pramp](https://www.pramp.com/)

---

🗣️ **We Value Your Feedback!**
If you found this helpful or want to share improvements, send us an email: [murrymujjy@gmail.com](mailto:murrymujjy@gmail.com)

Best of luck on your career journey! 🚀
"""

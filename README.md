# 💼 AI Career Advisor Bot

An intelligent, LangChain-powered chatbot that helps users explore suitable career paths based on their **background**, **skills**, and **interests** — no dataset required!

![Streamlit App Screenshot](https://github.com/Murrymujjy/Loan-bot/blob/main/screenshot.png) <!-- Optional: Replace with your screenshot -->

---

## 🚀 Live Demo

👉 [Launch the App](https://your-streamlit-link.streamlit.app)  
*(Replace this with your actual deployed link once live)*

---

## 🧠 How It Works

The bot uses **OpenAI's GPT model** to:
- Analyze user input (e.g., education, interests, skills)
- Suggest 3 relevant career paths
- Recommend skills and tools to explore

---

## ✨ Example Input

> I studied Physics and enjoy coding. I'm curious about healthcare and AI.

### ✅ Example Output

- **Suggested Careers**:  
  - Medical Physicist  
  - AI in Healthcare  
  - Health Data Analyst  

- **Recommended Skills**:  
  Python, Machine Learning, Bioinformatics

---

## 📦 Project Structure

```bash
career-advisor-bot/
│
├── app.py                # Streamlit app
├── requirements.txt      # Project dependencies
├── .env                  # OpenAI API Key (keep secret)
└── README.md             # Project documentation

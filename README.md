# 🎯 AI Career Advisor App

The **AI Career Advisor** is a multilingual, AI-powered web application that helps users:
- Get personalized career guidance
- Build professional resumes (from scratch or uploaded files)
- Generate tailored cover letters

Built with **Streamlit** and powered by **OpenAI**, this app supports 7 languages including local Nigerian languages like Yoruba, Hausa, and Igbo.

---

## 🚀 Features

### ✅ Career Advice Chatbot
- Inputs: name, background, interests, goals
- Outputs: AI-generated career advice in your selected language

### 📄 Resume Builder
- Upload your own PDF/DOCX resume and extract content
- Or build a new resume with AI guidance
- Download resumes as professional PDFs

### ✉️ Cover Letter Generator
- Customize tone: formal or casual
- Supports job role, company, and full job description
- Generates letters in English, French, Spanish, Yoruba, Hausa, and Igbo

---

## 🌐 Supported Languages

| Language      | Code |
|---------------|------|
| English (US)  | `en` |
| English (UK)  | `en-GB` |
| French        | `fr` |
| Spanish       | `es` |
| Yoruba (Yorùbá)   | `yo` |
| Hausa         | `ha` |
| Igbo          | `ig` |

---

## 🛠️ Tech Stack

- [Streamlit](https://streamlit.io) – interactive web app
- [OpenAI GPT](https://platform.openai.com) – AI responses
- [Langchain / Google Translate / Deep Translate] – optional AI translation
- [PyMuPDF](https://pymupdf.readthedocs.io) – PDF extraction
- [python-docx](https://python-docx.readthedocs.io) – DOCX extraction
- [fpdf](https://pyfpdf.readthedocs.io) – PDF resume generation

---

## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/mujeebatmuritala/ai-career-advisor.git
cd ai-career-advisor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run mainapp.py

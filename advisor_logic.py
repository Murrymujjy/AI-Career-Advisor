# mainapp.py
import streamlit as st
from advisor_logic import generate_career_advice, generate_cover_letter
from utils import extract_text_from_pdf, extract_text_from_docx, generate_pdf_resume

st.set_page_config(page_title="AI Career Advisor", page_icon="🎯")
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to", ["Career Advice", "Resume Builder", "Cover Letter"])

language_map = {
    "English (US)": "English",
    "English (UK)": "English",
    "Français": "French",
    "Español": "Spanish",
    "Yorùbá": "Yoruba",
    "Hausa": "Hausa",
    "Igbo": "Igbo"
}
selected_language = st.sidebar.selectbox("🌐 Choose your language", list(language_map.keys()))
lang_code = language_map[selected_language]

if page == "Career Advice":
    st.title("🎯 AI Career Advisor Chatbot")

    with st.form("career_form"):
        name = st.text_input("👤 Your Name")
        background = st.text_area("🎓 Your Background")
        interests = st.text_area("💡 Your Interests")
        goals = st.text_area("🎯 Your Career Goals")
        submit = st.form_submit_button("✨ Get Advice")

    if submit:
        if not all([name, background, interests, goals]):
            st.error("⚠️ Please fill in all fields.")
        else:
            st.info("🧠 Generating personalized advice...")
            response = generate_career_advice(name, background, interests, goals, lang_code)
            st.markdown(response)

elif page == "Resume Builder":
    st.title("📄 AI Resume Builder")
    option = st.radio("Choose", ["Upload Resume", "Build Resume with AI"])

    if option == "Upload Resume":
        file = st.file_uploader("Upload PDF or DOCX", type=["pdf", "docx"])
        if file:
            text = extract_text_from_pdf(file) if file.name.endswith(".pdf") else extract_text_from_docx(file)
            st.text_area("📄 Extracted Text", value=text, height=300)

    else:
        name = st.text_input("👤 Full Name")
        email = st.text_input("📧 Email")
        phone = st.text_input("📱 Phone")
        linkedin = st.text_input("🔗 LinkedIn")
        summary = st.text_area("📝 Summary")
        education = st.text_area("🎓 Education")
        skills = st.text_area("💡 Skills (comma separated)")
        experience = st.text_area("💼 Experience")

        if st.button("🚀 Generate Resume"):
            if not all([name, email, phone, summary, education, skills]):
                st.warning("⚠️ Please complete all required fields.")
            else:
                resume = f"""
{name}
Email: {email} | Phone: {phone}
{f'LinkedIn: {linkedin}' if linkedin else ''}

Summary:
{summary}

Education:
{education}

Skills:
{', '.join([s.strip() for s in skills.split(',')])}

Experience:
{experience or 'No experience listed.'}
"""
                st.text_area("📄 Resume Preview", value=resume, height=300)
                pdf = generate_pdf_resume(resume)
                with open(pdf, "rb") as f:
                    st.download_button("📥 Download PDF", f, file_name="resume.pdf")

elif page == "Cover Letter":
    st.title("✉️ AI Cover Letter Generator")

    with st.form("cover_form"):
        name = st.text_input("👤 Your Name")
        background = st.text_area("📚 Background")
        job_title = st.text_input("💼 Job Title")
        company = st.text_input("🏢 Company Name")
        tone = st.selectbox("🗣️ Tone", ["Formal", "Casual"])
        submit = st.form_submit_button("📨 Generate Cover Letter")

    if submit:
        if not all([name, background, job_title, company]):
            st.warning("⚠️ All fields are required.")
        else:
            st.info("🧠 Creating your cover letter...")
            letter = generate_cover_letter(name, background, job_title, company, tone.lower(), lang_code)
            st.text_area("📄 Cover Letter Preview", value=letter, height=300)

# Footer
st.markdown("""
---
Made with ❤️ by RedCherry
📬 [Feedback](mailto:murrymujjy@gmail.com)
""")

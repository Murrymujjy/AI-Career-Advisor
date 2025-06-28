import streamlit as st
from advisor_logic import generate_career_advice
from utils import extract_text_from_pdf, extract_text_from_docx, generate_pdf_resume

# Streamlit page config
st.set_page_config(page_title="AI Career Advisor", page_icon="🎯")

# Sidebar Navigation
selected = st.sidebar.radio("Navigate", ["Career Advisor", "Resume Builder"])

# ------------------ Career Advisor ------------------
if selected == "Career Advisor":
    st.title("🎯 AI Career Advisor Chatbot")
    st.markdown("""
    Welcome to the AI Career Advisor! Get professional guidance tailored to your background, interests, and career goals.

    🌐 You can choose your preferred language below.
    """)

    # Language selection
    language_map = {
        "English (US)": "en",
        "English (UK)": "en",
        "Français": "fr"
    }
    language_choice = st.selectbox("🌐 Choose your language", list(language_map.keys()))
    selected_language = language_map[language_choice]

    st.markdown("---")

    # Input form
    with st.form("career_advice_form"):
        name = st.text_input("👤 Your Name")
        background = st.text_area("🎓 Your Background (education or experience)")
        interests = st.text_area("💡 Your Interests (e.g., AI, UX, Marketing)")
        goals = st.text_area("🎯 Your Career Goals")

        submitted = st.form_submit_button("✨ Get My Career Advice")

    if submitted:
        if not all([name, background, interests, goals]):
            st.error("⚠️ Please complete all fields before submitting.")
        else:
            st.info("🧠 Generating personalized career guidance...")
            response = generate_career_advice(
                name=name,
                background=background,
                interests=interests,
                goals=goals,
                lang_code=selected_language
            )
            st.markdown(response, unsafe_allow_html=True)

# ------------------ Resume Builder ------------------
elif selected == "Resume Builder":
    st.title("📄 AI Resume Builder")
    resume_option = st.radio("Choose an option:", ["Upload Resume", "Build Resume with AI"])

    if resume_option == "Upload Resume":
        uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
        if uploaded_file:
            st.success("✅ Resume uploaded successfully!")

            if uploaded_file.name.endswith(".pdf"):
                extracted_text = extract_text_from_pdf(uploaded_file)
            else:
                extracted_text = extract_text_from_docx(uploaded_file)

            st.text_area("📄 Extracted Resume Text", value=extracted_text, height=300)

    elif resume_option == "Build Resume with AI":
        st.subheader("🛠️ Resume Generator")

        template = st.selectbox("🎨 Choose a template style", ["Classic", "Modern"])

        name = st.text_input("👤 Full Name")
        email = st.text_input("📧 Email Address")
        phone = st.text_input("📱 Phone Number")
        linkedin = st.text_input("🔗 LinkedIn Profile (optional)")
        summary = st.text_area("📝 Career Summary (2–3 sentences)")
        education = st.text_area("🎓 Education (e.g., BSc in Physics, OAU)")
        skills = st.text_area("💡 Key Skills (comma separated)")
        experience = st.text_area("💼 Work/Project Experience (optional)")

        if st.button("🚀 Generate My Resume"):
            if not all([name, email, phone, summary, education, skills]):
                st.warning("⚠️ Please fill in all required fields.")
            else:
                st.success("✅ Resume Generated Below:")
                st.markdown("---")

                resume_text = f"""
{name}
Email: {email} | Phone: {phone}
{f"LinkedIn: {linkedin}" if linkedin else ""}

Summary:
{summary}

Education:
{education}

Skills:
{', '.join([s.strip() for s in skills.split(',')])}

Experience:
{experience or 'No experience added.'}
"""

                st.text_area("📄 Resume Preview", value=resume_text, height=300)

                pdf_file = generate_pdf_resume(resume_text)
                with open(pdf_file, "rb") as f:
                    st.download_button("📥 Download Resume as PDF", f, file_name="resume.pdf", mime="application/pdf")

# ------------------ Feedback Section ------------------
st.markdown("---")
st.subheader("📬 Share Feedback")
st.markdown("""
We value your feedback! If you have suggestions or comments about this tool, please send us an email.

📧 [Send Feedback via Email](mailto:murrymujjy@gmail.com)
""")

# ------------------ Footer ------------------
st.markdown("""
---
Made with ❤️ by RedCherry
""")

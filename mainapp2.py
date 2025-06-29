import streamlit as st
from advisor_logic import generate_career_advice, generate_cover_letter

# Page configuration
st.set_page_config(page_title="AI Career Advisor", page_icon="🤖", layout="centered")

# Navigation
pages = ["💼 Career Advice", "📄 Resume Builder", "📝 Cover Letter Generator"]
selected_page = st.sidebar.selectbox("Navigate", pages)

# Language options
languages = {
    "English (US)": "English",
    "English (UK)": "English",
    "French": "French",
    "Spanish": "Spanish",
    "Yoruba": "Yoruba",
    "Hausa": "Hausa",
    "Igbo": "Igbo"
}

# Page: Career Advice
if selected_page == "💼 Career Advice":
    st.title("💼 AI Career Advisor")
    st.markdown("Get personalized career advice powered by AI.")

    name = st.text_input("Your Name")
    background = st.text_area("Brief Background")
    interests = st.text_area("Your Interests or Career Goals")
    language = st.selectbox("Preferred Language", list(languages.keys()))

    if st.button("Get Career Advice"):
        if not name or not background or not interests:
            st.error("⚠️ Please complete all fields before submitting.")
        else:
            st.info("🧠 Generating personalized career guidance...")
            prompt = f"My name is {name}. I have a background in {background}. My interests include {interests}. Please give me career advice in {languages[language]}."
            response = generate_career_advice(prompt)

            st.success("✅ Career Advice Generated!")
            st.markdown(response)

# Page: Cover Letter Generator
elif selected_page == "📝 Cover Letter Generator":
    st.title("📝 Cover Letter Generator")
    st.markdown("Generate a professional cover letter for your application.")

    name = st.text_input("Your Name", key="cl_name")
    job_title = st.text_input("Job Title You're Applying For")
    company_name = st.text_input("Company Name")
    background = st.text_area("Brief Background or Resume Summary", key="cl_bg")
    language = st.selectbox("Preferred Language", list(languages.keys()), key="cl_lang")

    if st.button("Generate Cover Letter"):
        if not name or not job_title or not company_name or not background:
            st.error("⚠️ Please complete all fields before submitting.")
        else:
            st.info("✍️ Generating your custom cover letter...")
            prompt = (
                f"Generate a professional cover letter in {languages[language]} for a person named {name} "
                f"who is applying for the position of {job_title} at {company_name}. "
                f"The background of the person is: {background}."
            )
            response = generate_cover_letter(prompt)

            st.success("✅ Cover Letter Generated!")
            st.markdown(response)

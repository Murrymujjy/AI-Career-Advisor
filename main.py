import streamlit as st
from advisor_logic import generate_career_advice
from resume_builder import generate_resume
from cover_letter import generate_cover_letter

st.set_page_config(page_title="AI Career Advisor", page_icon="💼")

st.sidebar.title("💼 AI Career Advisor")
section = st.sidebar.radio("Navigate", ["Career Advice", "Resume Builder", "Cover Letter Generator"])

st.title("💼 AI Career Advisor")
st.markdown("Get personalized career advice powered by your local AI model via LM Studio.")

name = st.text_input("Your Name", placeholder="e.g. Mujeebat")
background = st.text_area("Brief Background", placeholder="e.g. Nuclear Physics")
interests = st.text_area("Your Interests or Career Goals", placeholder="e.g. Machine Learning, Data Science")
language = st.selectbox("Preferred Language", ["English", "French", "Spanish", "Yoruba", "Hausa", "Igbo"])

if st.button("🧠 Generate"):
    if not name or not background or not interests:
        st.error("⚠️ Please complete all fields.")
    else:
        with st.spinner("Thinking..."):
            try:
                if section == "Career Advice":
                    response = generate_career_advice(name, background, interests, language)
                elif section == "Resume Builder":
                    response = generate_resume(name, background, interests)
                elif section == "Cover Letter Generator":
                    response = generate_cover_letter(name, background, interests)

                st.success("✅ Response Generated!")
                st.text_area("🔍 Output", value=response, height=500)
            except Exception as e:
                st.error(f"❌ Failed to generate response: {e}")

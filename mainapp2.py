import streamlit as st
from advisor_logic import generate_career_advice

# Language selection
st.set_page_config(page_title="AI Career Advisor", page_icon="🎯")

st.title("🎯 AI Career Advisor Chatbot")

st.markdown("""
Welcome to the AI Career Advisor! Get professional guidance tailored to your background, interests, and career goals.

🌐 You can choose your preferred language below.
""")

# Language dropdown
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

# Call logic function on submit
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
            language=selected_language
        )
        st.markdown(response, unsafe_allow_html=True)

# Feedback section
st.markdown("---")
st.subheader("📬 Share Feedback")
st.markdown("""
We value your feedback! If you have suggestions or comments about this tool, please send us an email.

📧 [Send Feedback via Email](mailto:murrymujjy@gmail.com)
""")

# Footer
st.markdown("""
---
Made with ❤️ using [Streamlit](https://streamlit.io/) and [OpenAI](https://openai.com/)
""")

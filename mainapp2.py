# app.py

import streamlit as st
from advisor_logic import generate_career_advice

st.set_page_config(page_title="AI Career Advisor", page_icon="🎯")
st.title("🎯 AI Career Advisor Chatbot")

st.write("Fill in the details below to get personalized career advice:")

language_map = {
    "English (US)": "en",
    "English (UK)": "en",  # Treated the same for simplicity
    "Français": "fr"
}

language_choice = st.selectbox("🌐 Choose your language", list(language_map.keys()))
selected_language = language_map[language_choice]


name = st.text_input("Your Name")
background = st.text_area("What's your academic or professional background?")
interests = st.text_area("What are your career interests?")
goals = st.text_area("What are your long-term career goals?")

if st.button("Get Advice"):
    advice = generate_career_advice(name, background, interests, goals)
    st.markdown(advice)

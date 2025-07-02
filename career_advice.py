import streamlit as st
from advisor_logic import generate_career_advice

def show():
    st.subheader("🧠 Career Advice")

    # Common inputs
    name = st.text_input("Your Name", key="ca_name", placeholder="e.g. Mujeebat")
    background = st.text_area("Brief Background", key="ca_background", placeholder="e.g. Nuclear Physics")
    interests = st.text_area("Your Interests or Career Goals", key="ca_interests", placeholder="e.g. Machine Learning, Data Science")
    language = st.selectbox("Preferred Language", ["English", "French", "Spanish", "Yoruba", "Hausa", "Igbo"], key="ca_lang")

    if st.button("💡 Generate Career Advice"):
        if not name or not background or not interests:
            st.warning("⚠️ Please complete all fields.")
        else:
            with st.spinner("Generating advice..."):
                try:
                    advice = generate_career_advice(name, background, interests, language)
                    st.success("✅ Career advice generated!")
                    st.text_area("📋 Career Advice", value=advice, height=400)
                except Exception as e:
                    st.error(f"❌ Error: {e}")

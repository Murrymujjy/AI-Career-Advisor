import streamlit as st
from advisor_logic import generate_career_advice

st.set_page_config(page_title="AI Career Advisor", page_icon="💼")

st.title("💼 AI Career Advisor")
st.markdown("Get personalized career advice powered by AI.")

# Inputs
name = st.text_input("Your Name", "")
background = st.text_area("Brief Background", "")
interests = st.text_area("Your Interests or Career Goals", "")
language = st.selectbox("Preferred Language", ["English (US)", "English (UK)", "French", "Spanish", "Yoruba", "Hausa", "Igbo"])

# On Submit
if st.button("Get Career Advice"):
    if not name or not background or not interests:
        st.error("⚠️ Please complete all fields before submitting.")
    else:
        st.info("🧠 Generating personalized career guidance...")

        # Build prompt
        prompt = f"""
        Name: {name}
        Background: {background}
        Interests/Career Goals: {interests}
        Preferred Language: {language}

        Provide a career recommendation tailored to this person. Be practical and supportive.
        """

        try:
            response = generate_career_advice(prompt)
            st.success("✅ Career Advice Generated!")
            st.markdown(response)
        except Exception as e:
            st.error(f"❌ Error generating career advice: {e}")

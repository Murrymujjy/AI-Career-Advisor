import streamlit as st

st.title("🤖 AI Chatbot for Farmer Credit Scoring")

st.markdown("Ask questions like:")
st.markdown("- *Will a 40-year-old farmer in rural area with secondary education get a loan?*")
st.markdown("- *What is the credit score of a woman with access to phone and tertiary education?*")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi there! I'm your offline credit scoring assistant. Ask me about any farmer profile and I’ll give you a simulated answer."}
    ]

# Display messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Simulated rule-based reply
def get_simulated_reply(user_input):
    user_input = user_input.lower()

    score = 0
    if "age" in user_input:
        if any(x in user_input for x in ["young", "below 25", "under 25"]):
            score -= 1
        elif any(x in user_input for x in ["40", "middle age", "experienced"]):
            score += 1

    if "education" in user_input:
        if "tertiary" in user_input or "degree" in user_input:
            score += 2
        elif "secondary" in user_input:
            score += 1
        elif "none" in user_input:
            score -= 1

    if "rural" in user_input:
        score += 1
    if "urban" in user_input:
        score += 0  # neutral

    if "phone" in user_input:
        if "no phone" in user_input:
            score -= 1
        elif "has phone" in user_input or "access to phone" in user_input:
            score += 1

    if "woman" in user_input and "support" in user_input:
        score += 1

    if score >= 3:
        return "✅ This farmer is highly likely to be eligible for a loan!"
    elif score >= 1:
        return "🟡 This farmer has a moderate chance of getting a loan."
    else:
        return "⚠️ This farmer might be considered high risk."

# Chat input
prompt = st.chat_input("Type your question here...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            reply = get_simulated_reply(prompt)
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})

st.markdown("---")
st.markdown("<div style='text-align: center;'>📌 Made with ❤️ by <strong>Team Numerixa</strong></div>", unsafe_allow_html=True)

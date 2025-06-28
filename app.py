# app.py

import os
import streamlit as st
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

# Load environment variables
load_dotenv()

# Set up OpenAI model
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.4)

# App UI
st.set_page_config(page_title="Career Advisor Bot", page_icon="💼")
st.title("💼 AI Career Advisor Bot")
st.markdown("Enter your background, interests, or skills, and I'll suggest career paths and learning directions.")

# Input
user_input = st.text_area("🧠 Describe your education, skills, or interests:")

# Generate response
if st.button("Get Advice") and user_input:
    with st.spinner("Thinking..."):
        prompt = (
            f"You are an expert career advisor. Given the following background, suggest:\n"
            f"- 3 relevant career paths\n"
            f"- Key skills to learn\n"
            f"- (Optional) Tools or fields to explore\n\n"
            f"User input: {user_input}"
        )
        response = llm([HumanMessage(content=prompt)])
        st.markdown("### 🎯 Career Suggestions")
        st.write(response.content)

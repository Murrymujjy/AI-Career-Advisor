# app.py

import os
import streamlit as st
from dotenv import load_dotenv
from langchain.agents import Tool, initialize_agent
# from langchain.chat_models import ChatOpenAI
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.agents.agent_types import AgentType

load_dotenv()

# Custom loan logic
def check_loan_eligibility(loan_type, age, years_in_community, phone_access, sector):
    try:
        age = int(age)
        years_in_community = int(years_in_community)
    except:
        return "❌ Invalid age or years. Use numbers."

    if (
        age >= 18 and
        years_in_community >= 2 and
        phone_access.lower() == "yes" and
        sector.lower() in ["agriculture", "trading", "livestock"]
    ):
        return "✅ You are likely to qualify for a loan!"
    else:
        return "❌ You may not meet the criteria."

def loan_tool_func(input_str: str):
    try:
        parts = [x.strip() for x in input_str.split(",")]
        loan_type, age, years, phone, sector = parts
        return check_loan_eligibility(loan_type, age, years, phone, sector)
    except:
        return "❗Use format: loan_type, age, years_in_community, phone_access(Yes/No), sector"

loan_tool = Tool(
    name="LoanPrequalChecker",
    func=loan_tool_func,
    description="Check loan eligibility. Format: loan_type, age, years, phone_access, sector"
)

llm = ChatOpenAI(temperature=0.2, model_name="gpt-3.5-turbo")
memory = ConversationBufferMemory(memory_key="chat_history")

agent = initialize_agent(
    tools=[loan_tool],
    llm=llm,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=False
)

st.set_page_config(page_title="Loan Bot", page_icon="🤖")
st.title("🤖 Loan Pre-Qualification Bot")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.chat_input("Check your loan eligibility...")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)

    response = agent.run(user_input)

    with st.chat_message("assistant"):
        st.write(response)

    st.session_state.chat_history.append((user_input, response))

for user_msg, bot_msg in st.session_state.chat_history:
    with st.chat_message("user"):
        st.markdown(user_msg)
    with st.chat_message("assistant"):
        st.markdown(bot_msg)

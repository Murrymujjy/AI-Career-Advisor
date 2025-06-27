import os
import streamlit as st
from langchain.agents import initialize_agent, Tool
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.agents.agent_types import AgentType
from dotenv import load_dotenv

load_dotenv()

# Custom loan logic function
def check_loan_eligibility(loan_type, age, years_in_community, phone_access, sector):
    try:
        age = int(age)
        years_in_community = int(years_in_community)
    except:
        return "❌ Invalid age or years value. Please enter numbers."

    if (
        age >= 18 and
        years_in_community >= 2 and
        phone_access.lower() == "yes" and
        sector.lower() in ["agriculture", "trading", "livestock"]
    ):
        return "✅ You are likely to qualify for a loan!"
    else:
        return "❌ You may not meet the prequalification criteria."

# Define a LangChain Tool
def loan_tool_func(input_str: str):
    """Extracts parameters from user input string and checks eligibility."""
    try:
        parts = [x.strip() for x in input_str.split(",")]
        loan_type, age, years, phone, sector = parts
        return check_loan_eligibility(loan_type, age, years, phone, sector)
    except:
        return "❗Please input in format: loan_type, age, years_in_community, phone_access(Yes/No), sector"

loan_tool = Tool(
    name="LoanPrequalChecker",
    func=loan_tool_func,
    description="Use this tool to determine loan eligibility. Input: loan_type, age, years, phone_access, sector"
)

# LangChain setup
llm = ChatOpenAI(temperature=0.2, model_name="gpt-3.5-turbo")
memory = ConversationBufferMemory(memory_key="chat_history")

agent = initialize_agent(
    tools=[loan_tool],
    llm=llm,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=False,
    memory=memory
)

# Streamlit UI
st.set_page_config(page_title="LangChain Loan Chatbot", page_icon="🤖")
st.title("🤖 Smart Loan Pre-Qualification Bot")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.chat_input("Ask about your loan eligibility...")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)

    response = agent.run(user_input)

    with st.chat_message("assistant"):
        st.write(response)

    st.session_state.chat_history.append((user_input, response))

# Chat history
for user_msg, bot_msg in st.session_state.chat_history:
    with st.chat_message("user"):
        st.markdown(user_msg)
    with st.chat_message("assistant"):
        st.markdown(bot_msg)

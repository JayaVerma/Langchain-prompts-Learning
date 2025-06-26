import streamlit as st
from dotenv import load_dotenv

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder

# Load API key
load_dotenv()

# Initialize Chat Model
chat = ChatOpenAI(temperature=0.5)

# Streamlit App Setup
st.set_page_config(page_title="Study Assistant Chatbot", layout="centered")
st.title("📚 Study Assistant Chatbot")

# Session State for Chat History
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Define prompt template with system message and placeholder
prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        "You are a helpful and friendly AI tutor. Explain concepts clearly and help the student understand anything they ask."
    ),
    MessagesPlaceholder(variable_name="history"),
    HumanMessage(content="{input}")
])

# User Input
user_input = st.chat_input("Ask me anything you’re studying...")

# Display Chat History
for msg in st.session_state.chat_history:
    if isinstance(msg, HumanMessage):
        st.chat_message("user").write(msg.content)
    elif isinstance(msg, AIMessage):
        st.chat_message("assistant").write(msg.content)

# Handle New Message
if user_input:
    st.chat_message("user").write(user_input)
    st.session_state.chat_history.append(HumanMessage(content=user_input))

    # Format the prompt with current history
    messages = prompt.format_messages(
        history=st.session_state.chat_history,
        input=user_input
    )

    # Get AI response
    response = chat(messages)
    st.chat_message("assistant").write(response.content)

    # Append response to chat history
    st.session_state.chat_history.append(AIMessage(content=response.content))

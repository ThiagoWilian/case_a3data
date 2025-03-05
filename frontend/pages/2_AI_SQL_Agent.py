# frontend/pages/chat_agent_sql.py
from core.settings import settings
import streamlit as st
import requests

st.title("💬 Chatbot")

user_input = st.text_input("Digite sua pergunta:")

if st.button("Perguntar"):
    if user_input:
        response = requests.post(f"{settings.API_URL}/chat", json={"question": user_input})
        bot_reply = response.json().get("response")
        st.write(f"🤖 Chatbot: {bot_reply}")

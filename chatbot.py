import os
from pathlib import Path
from google import genai
import streamlit as st
from dotenv import load_dotenv

# ---------- LOAD ENV FILE ----------
load_dotenv(dotenv_path=Path("naveen/.env"))

# ---------- LOAD API KEY ----------
api_key = os.getenv("gemini_key")

if api_key is None:
    raise ValueError("Gemini API key not found. Please set environment variable.")

os.environ["GOOGLE_API_KEY"] = api_key

# ---------- INITIALIZE CLIENT ----------
if "client" not in st.session_state:
    st.session_state.client = genai.Client()

client = st.session_state.client

# ---------- SYSTEM PROMPT ----------
system_prompt = """You are a professional AI Career Advisor.

Your role:
- Help users choose the right career path
- Suggest in-demand skills
- Provide personalized learning roadmaps
- Give resume and interview guidance

Restriction:
Answer ONLY career, skills, education, and job-related queries.
If user asks anything else say:
"I can help only with career guidance and professional growth."
"""

# ---------- UI ----------
st.title("🎯 AI Career Advisor")
st.write("Ask about careers, skills, job roles, or learning paths.")

# ---------- CREATE CHAT SESSION ----------
if "chat_session" not in st.session_state:
    st.session_state.chat_session = client.chats.create(
        model="gemini-1.5-flash",
        config=genai.types.GenerateContentConfig(
            system_instruction=system_prompt,
        )
    )

# ---------- MESSAGE STORAGE ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- DISPLAY CHAT HISTORY ----------
for role, text in st.session_state.messages:
    if role == "user":
        st.markdown(f"**You:** {text}")
    else:
        st.markdown(f"**Advisor:** {text}")

# ---------- CHAT INPUT ----------
user_input = st.chat_input("Type your career question here...")

if user_input:
    st.session_state.messages.append(("user", user_input))

    chat = st.session_state.chat_session
    response = chat.send_message(user_input)

    bot_reply = response.text
    st.session_state.messages.append(("bot", bot_reply))

    st.rerun()
import os
import warnings

warnings.filterwarnings("ignore")
os.environ["PYTHONWARNINGS"] = "ignore"

import streamlit as st
import base64
from inferencia_interfaz import responder_pregunta  # Your actual response function


st.set_page_config(page_title="Friends Assistant", layout="centered", initial_sidebar_state="collapsed")

# === Apply styles and full-page background ===
def apply_styles():
    with open("Interfaz-Images/a.png", "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode()

    st.markdown(
        f"""
        <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
        <style>
        html, body, .stApp {{
            height: 100%;
            background-image: url("data:image/jpg;base64,{encoded_image}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            margin: 0;
            padding: 0;
        }}
        .block-container {{
            background-color: rgba(255, 255, 255, 0.85);  /* optional: semi-transparent background */
            padding: 2rem;
            border-radius: 12px;
            margin-top: 2rem;
        }}
        .chat-message {{
            display: flex;
            align-items: flex-start;
            margin: 10px 0;
        }}
        .chat-icon {{
            font-family: 'Material Icons';
            font-size: 28px;
            padding: 6px;
            color: #555;
        }}
        .chat-bubble {{
            padding: 10px 15px;
            border-radius: 15px;
            max-width: 70%;
            font-size: 16px;
            line-height: 1.5;
        }}
        .user-message {{
            justify-content: flex-end;
            text-align: right;
        }}
        .user-bubble {{
            background-color: #007bff;
            color: white;
            margin-left: auto;
        }}
        .assistant-message {{
            justify-content: flex-start;
            text-align: left;
        }}
        .assistant-bubble {{
            background-color: #eaeaea;
            color: black;
            margin-right: auto;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

apply_styles()

st.title("Welcome to Friends' Chatbot")

# === Initialize chat history ===
if "messages" not in st.session_state:
    st.session_state.messages = []

# === Display chat history ===
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f"""
            <div class="chat-message user-message">
                <div class="chat-bubble user-bubble">{msg['content']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div class="chat-message assistant-message">
                <div class="chat-icon">smart_toy</div>
                <div class="chat-bubble assistant-bubble">{msg['content']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

# === Chat input ===
if prompt := st.chat_input("Ask something about the TV show Friends..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(
        f"""
        <div class="chat-message user-message">
            <div class="chat-bubble user-bubble">{prompt}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.spinner("..."):
        response,*_ = responder_pregunta(prompt)

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.markdown(
        f"""
        <div class="chat-message assistant-message">
            <div class="chat-icon">smart_toy</div>
            <div class="chat-bubble assistant-bubble">{response}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

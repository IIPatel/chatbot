import streamlit as st
import requests
import json

# Set page configuration
st.set_page_config(page_title="AI Chat Assistant", layout="centered")

# Custom CSS for better styling
st.markdown("""
    <style>
    .stTextInput>div>div>input {
        border-radius: 10px;
    }
    .css-1d391kg {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 0.5rem;
    }
    .user-message {
        background-color: #2196F3;
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .assistant-message {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for messages if it doesn't exist
if 'messages' not in st.session_state:
    st.session_state.messages = []

# App title
st.title("AI Chat Assistant")

# API Configuration
API_KEY = st.secrets["API_KEY"]  # Store your API key in Streamlit secrets
API_URL = "https://api.nexusmind.tech/v1/chat/completions"

def get_ai_response(messages):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "messages": [
            {"role": "system", "content": "You are a helpful AI assistant."}
        ] + messages,
        "model": "gpt-4o",
        "stream": False
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

# Display chat messages
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="user-message">✋ {message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="assistant-message">🎈 {message["content"]}</div>', unsafe_allow_html=True)

# Chat input
user_input = st.text_input("Type your message...", key="user_input")

if st.button("Send"):
    if user_input:
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Get AI response
        with st.spinner("AI is thinking..."):
            ai_response = get_ai_response(st.session_state.messages)
            
        if ai_response:
            # Add AI response to chat
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
        
        # Rerun to update the chat display
        st.experimental_rerun()

# Clear chat button
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.experimental_rerun()
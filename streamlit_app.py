import streamlit as st
from openai import OpenAI
import time
import json

# Set page config FIRST
st.set_page_config(
    page_title="BizBot Pro | AI Customer Support",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Initialize client after page config
@st.cache_resource
def get_client():
    return OpenAI(
        base_url="https://api.electronhub.top/v1/",
        api_key=st.secrets["API_KEY"]
    )

client = get_client()

# Rest of the code remains the same
MODEL_MAP = {
    "default": "claude-3-haiku-20240307",
    "complex": "gpt-4o",
    "fallback": "gemini-1.5-flash"
}

def get_best_model(query):
    if len(query) > 1000:
        return "gpt-3.5-turbo-16k"
    elif any(keyword in query.lower() for keyword in ["technical", "urgent", "complex"]):
        return MODEL_MAP["complex"]
    return MODEL_MAP["default"]

def main():
    # Custom styling
    st.markdown("""
    <style>
        [data-testid="stHeader"] {background: #1a237e;}
        .stChatInput {border-radius: 20px;}
        .stButton>button {background: #4CAF50!important; color: white!important;}
    </style>
    """, unsafe_allow_html=True)
    
    # Rest of your existing main() function
    # ... (keep the rest of your code unchanged)

if __name__ == "__main__":
    main()
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
    
    # Session state initialization
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "usage" not in st.session_state:
        st.session_state.usage = {"tokens": 0, "conversations": 0}
    
    # Sidebar - Business Configuration
    with st.sidebar:
        st.image("https://i.imgur.com/xyz/logo.png", width=150)  # Default logo
        st.header("Business Setup")
        
        # Brand customization
        business_name = st.text_input("Business Name", "My Business")
        brand_color = st.color_picker("Brand Color", "#4B89DC")
        logo = st.file_uploader("Upload Logo (PNG)", type=["png"])
        
        # Model selection
        st.divider()
        with st.expander("⚙️ Advanced Settings"):
            model_choice = st.radio("AI Model Priority", 
                ["Cost-Effective", "Balanced", "High Accuracy"])
            
        # Analytics
        st.divider()
        st.subheader("Analytics")
        col1, col2 = st.columns(2)
        col1.metric("Total Chats", st.session_state.usage["conversations"])
        col2.metric("Tokens Used", f"{st.session_state.usage['tokens']:,}")
    
    # Main chat interface
    st.header(f"💬 {business_name} Support")
    
    # Chat messages display
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input and processing
    if prompt := st.chat_input("How can I help you today?"):
        try:
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.usage["conversations"] += 1
            
            # Get model based on query
            selected_model = get_best_model(prompt)
            
            # Generate response
            with st.chat_message("assistant"):
                response = client.chat.completions.create(
                    model=selected_model,
                    messages=[{"role": "system", "content": f"You are {business_name}'s support assistant. Current time: {time.strftime('%Y-%m-%d %H:%M')}"}] 
                              + st.session_state.messages,
                    stream=True,
                )
                
                full_response = ""
                container = st.empty()
                for chunk in response:
                    if chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        container.markdown(full_response + "▌")
                
                container.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                st.session_state.usage["tokens"] += response.usage.total_tokens
                
        except Exception as e:
            # Fallback to Gemini-1.5-Flash
            st.error("⚠️ Primary model failed - using backup")
            response = client.chat.completions.create(
                model=MODEL_MAP["fallback"],
                messages=st.session_state.messages
            )
            st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})

if __name__ == "__main__":
    main()
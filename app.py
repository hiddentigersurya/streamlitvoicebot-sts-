import streamlit as st
import os
from utils import get_answer, text_to_speech, autoplay_audio, speech_to_text
from audio_recorder_streamlit import audio_recorder
from streamlit_float import *

# Float feature initialization
float_init()

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi! How may I assist you today?"}
        ]
    # if "audio_initialized" not in st.session_state:
    #     st.session_state.audio_initialized = False

initialize_session_state()

# Add custom CSS styles
st.markdown(
    """
    <style>
    .stApp {
        max-width: 900px;
        max-height: 92%;
        margin: 0 auto;
        padding: 2rem;
        background-color: #f5f5f5;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }

    .stApp h1 {
        color: #333333;
        font-size: 2rem;
        margin-bottom: 2rem;
    }

    .stApp .stChatMessage {
        margin-bottom: 1rem;
    }

    .stApp .stChatMessage.user {
        background-color: #e6f7ff;
        border-radius: 10px;
        padding: 0.5rem 1rem;
    }

    .stApp .stChatMessage.assistant {
        background-color: #f0f0f0;
        border-radius: 10px;
        padding: 0.5rem 1rem;
    }

    .stApp .stChatMessage.assistant .stMarkdown {
        color: #333333;
    }

    .stApp .stSpinner {
        color: #333333;
    }

    .stApp .stButton {
        background-color: #333333;
        color: #ffffff;
        border-radius: 5px;
        padding: 0.5rem 1rem;
    }

    .stApp .stButton:hover {
        background-color: #555555;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Conversational Chatbot 🤖")

# Create footer container for the microphone
footer_container = st.container()
with footer_container:
    audio_bytes = audio_recorder()


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if audio_bytes:
    # Write the audio bytes to a file
    with st.spinner("Transcribing..."):
        webm_file_path = "temp_audio.mp3"
        with open(webm_file_path, "wb") as f:
            f.write(audio_bytes)

        transcript = speech_to_text(webm_file_path)
        if transcript:
            st.session_state.messages.append({"role": "user", "content": transcript})
            with st.chat_message("user"):
                st.write(transcript)
            os.remove(webm_file_path)

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking🤔..."):
            final_response = get_answer(st.session_state.messages)
        with st.spinner("Generating audio response..."):    
            audio_file = text_to_speech(final_response)
            autoplay_audio(audio_file)
        st.write(final_response)
        st.session_state.messages.append({"role": "assistant", "content": final_response})
        os.remove(audio_file)

# Float the footer container and provide CSS to target it with
footer_container.float("bottom: 0rem; position: fixed; width: 100%;")

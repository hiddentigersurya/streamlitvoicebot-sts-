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

initialize_session_state()

st.title("AI Conversational Chatbot 🤖")

# Create fixed header container for the microphone and text
header_container = st.container()
with header_container:
    st.markdown(
        """
        <div style="position: fixed; top: 1rem; left: 50%; transform: translateX(-50%); text-align: center; z-index: 1000;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/8/8f/Microphone.svg" alt="Microphone" style="width: 100px;">
            <p style="font-size: 1.2rem;">Click to Talk to AI</p>
        </div>
        """, unsafe_allow_html=True
    )

# Create container for the conversation
conversation_container = st.container()
with conversation_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

# Record audio when mic is clicked
audio_bytes = audio_recorder()
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

# Add CSS for styling and automatic scrolling
st.markdown(
    """
    <style>
    .stContainer {
        margin-top: 200px; /* Adjust based on the size of the fixed header */
    }
    .stChatMessage {
        overflow-y: auto;
        max-height: 70vh; /* Adjust as needed */
    }
    .stChatMessage div {
        overflow-y: auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

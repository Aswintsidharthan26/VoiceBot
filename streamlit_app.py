import streamlit as st
import requests
import sounddevice as sd
import numpy as np
import wave
import time
# Backend API URLs
CHAT_URL = "http://127.0.0.1:8000/chat/"
STT_URL = "http://127.0.0.1:8000/stt/"
TTS_URL = "http://127.0.0.1:8000/tts/"

st.title("🎙📝 AI Voice & Chatbot")
st.write("Talk or type to your AI assistant!")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 🎤 **Voice Recording Function**
def record_audio(filename="speech.wav", duration=5, samplerate=44100):
    print("🎤 Recording... Speak now! and wait for 5 seconds...")
    msg_placeholder = st.empty()  # Create a placeholder for the message
    
    # Show the recording message
    msg_placeholder.write("🎤 Recording... Speak now! and wait for 5 seconds...")
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype=np.int16)
    time.sleep(duration)

    sd.wait()  # Wait until recording is finished
    msg_placeholder.empty()

    # Save the recording
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(samplerate)
        wf.writeframes(recording.tobytes())

    print("✅ Recording saved as", filename)
    return filename

# 🎤 **Voice Input**
if st.button("🎙 Start Recording"):
    audio_file = record_audio()
    
    if audio_file:
        # st.write("Transcribing voice...")

        with open(audio_file, "rb") as f:
            response = requests.post(STT_URL, files={"file": f})
            # st.write(response.json()['transcription'])
        if response.status_code == 200:
            # user_input = response.json().get("text", "")
            try:
                user_input = response.json()['transcription']
                if user_input:
                    st.session_state.messages.append({"role": "user", "content": user_input})
                    with st.chat_message("user"):
                        st.markdown(user_input)
                        
                    # st.write("Sending to chatbot...")
                    # Call chatbot API
                    chat_response = requests.post(CHAT_URL, json={"message": user_input})
                    bot_reply = chat_response.json().get("response", "No response")

                    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                    with st.chat_message("assistant"):
                        st.markdown(bot_reply)

                    # Convert response to speech
                    tts_response = requests.post(TTS_URL, json={"message": bot_reply})
                    # st.write(tts_response)
                    audio_url = tts_response.json().get("audio_url", "")

                    if audio_url:
                        st.audio(audio_url, format="audio/mp3")
            except:
                st.error("Failed to transcribe audio!")
        else:
            st.error("Failed to transcribe audio!")


# 📝 **Text Chat Input**
user_text = st.chat_input("Type your message...")

if user_text:
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    st.write("Sending to chatbot...")
    # Call chatbot API
    chat_response = requests.post(CHAT_URL, json={"message": user_text})
    bot_reply = chat_response.json().get("response", "No response")
    # st.write("Bot is responding...")
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
    # st.write("BOT RESPONSE DONE")
    # Convert response to speech
    tts_response = requests.post(TTS_URL, json={"message": bot_reply})
    # st.write(tts_response)
    print("RESPONSE AUDIO",tts_response)
    audio_url = tts_response.json().get("audio_url", "")

    if audio_url:
        st.audio(audio_url, format="audio/mp3")

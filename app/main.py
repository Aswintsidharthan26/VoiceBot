from pydantic import BaseModel
from groq import Groq
import os
import requests
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Form
from fastapi import FastAPI, UploadFile, File
import speech_recognition as sr
from gtts import gTTS
import pygame
import tempfile
import os

app = FastAPI()

# CORS to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load API Keys from environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY", "7fca19e777c34178b7003150d1a8472c")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Request Model
class ChatRequest(BaseModel):
    message: str


base_prompt = """
You are Aswin T. Sidharthan. Answer all questions as yourself, keeping responses concise, confident, and true to your personality.

- **Life Story:** "I love solving problems with AI, automation, and backend development. My journey is about researching and implementing new technologies, engineering AI solutions, and developing innovative products to make systems smarter and more efficient."
- **Superpower:** "Breaking down complex problems into simple, effective solutions."
- **Top 3 Areas of Growth:** "AI engineering and automation, structured project execution, and leadership."
- **Misconception About You:** "That I prefer working alone—I actually enjoy smart collaborations."
- **How You Push Boundaries:** "By tackling projects just beyond my comfort zone and constantly learning."

Always respond in a way that aligns with these traits. Keep answers short, direct, and natural.
"""


# Chatbot API
@app.post("/chat/")
async def chat(request: ChatRequest):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        # messages=[{"role": "user", "content": request.message}],
        messages=[
        {"role": "system", "content": base_prompt},
        {"role": "user", "content": request.message}
        ],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=False,
    )
    print(response.choices[0].message.content)
    return {"response": response.choices[0].message.content}

# Speech-to-Text (STT) API using AssemblyAI


# Speech-to-Text (STT) using Google Speech Recognition
@app.post("/stt/")
async def speech_to_text(file: UploadFile = File(...)):
    try:
        recognizer = sr.Recognizer()
        print("FILE", file)
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            temp_audio.write(await file.read())
            temp_audio_path = temp_audio.name

        # Convert speech to text
        with sr.AudioFile(temp_audio_path) as source:
            audio_data = recognizer.record(source)
        # print("AUDIO DATA", audio_data)
        text = recognizer.recognize_google(audio_data)
        # print("Transcription:", text)
        # Clean up temporary file
        os.remove(temp_audio_path)

        return {"transcription": text}

    except sr.UnknownValueError:
        return {"error": "Could not understand the audio"}
    except sr.RequestError as e:
        return {"error": f"Google Speech-to-Text API error: {e}"}



class TTSRequest(BaseModel):
    message: str

# Text-to-Speech (TTS) using Google Text-to-Speech
@app.post("/tts/")
async def text_to_speech(req: TTSRequest):
    try:
        output_file = "output.mp3"
        text = req.message
        # Convert text to speech
        tts = gTTS(text=text, lang="en")
        print("OUTPUT***********************",tts)
        tts.save(output_file)

        # Play the audio using pygame
        pygame.mixer.init()
        pygame.mixer.music.load(output_file)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            continue  # Wait until audio finishes playing

        return {"message": "Text converted to speech and played successfully!"}

    except Exception as e:
        return {"error": f"Text-to-Speech conversion failed: {e}"}

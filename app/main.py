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
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

# CORS to allow frontend communication
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, set to your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_index():
    return FileResponse("static/index.html")

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
from pydub import AudioSegment

@app.post("/stt/")
async def speech_to_text(file: UploadFile = File(...)):
    try:
        print("FILE***********************",file)
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp_audio:
            temp_audio.write(await file.read())
            temp_audio_path = temp_audio.name

        # Convert to WAV using pydub
        audio = AudioSegment.from_file(temp_audio_path)
        wav_path = temp_audio_path.replace(".webm", ".wav")
        audio.export(wav_path, format="wav")

        # Convert speech to text
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)

        # Clean up
        os.remove(temp_audio_path)
        os.remove(wav_path)

        return {"text": text}
    except Exception as e:
        return {"error": str(e)}




class TTSRequest(BaseModel):
    text: str

# Text-to-Speech (TTS) using Google Text-to-Speech
from fastapi import BackgroundTasks

@app.post("/tts/")
async def text_to_speech(req: TTSRequest, background_tasks: BackgroundTasks):
    try:
        output_file = "output.mp3"
        text = req.text

        # Convert text to speech
        tts = gTTS(text=text, lang="en")
        tts.save(output_file)

        # Delete file after response is sent (optional cleanup)
        background_tasks.add_task(os.remove, output_file)

        # Send the audio file to the frontend
        return FileResponse(output_file, media_type="audio/mpeg", filename="output.mp3")

    except Exception as e:
        return {"error": f"Text to speech conversion failed: {str(e)}"}

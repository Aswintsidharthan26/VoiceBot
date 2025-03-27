import sounddevice as sd
import numpy as np
import wave
import requests
import time
from gtts import gTTS

# AssemblyAI API Key
ASSEMBLYAI_API_KEY = "7fca19e777c34178b7003150d1a8472c"

# Function to Record Audio
def record_audio(filename="speech.wav", duration=5, samplerate=44100):
    print("🎤 Recording... Speak now!")
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype=np.int16)
    sd.wait()  # Wait until recording is finished

    # Save the recording
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(samplerate)
        wf.writeframes(recording.tobytes())

    print("✅ Recording saved as", filename)
    return filename

# Function to Transcribe Audio using AssemblyAI
import speech_recognition as sr

def transcribe_audio(filename):
    print("🔄 Transcribing audio using Google Speech-to-Text...")

    recognizer = sr.Recognizer()

    with sr.AudioFile(filename) as source:
        audio_data = recognizer.record(source)  # Read the entire audio file

    try:
        text = recognizer.recognize_google(audio_data)
        print("✅ Transcription:", text)
        return text
    except sr.UnknownValueError:
        print("❌ Could not understand the audio.")
    except sr.RequestError as e:
        print(f"❌ Error with Google Speech-to-Text API: {e}")

    return None


# Function to Convert Text to Speech using Google TTS
import pygame

def text_to_speech(text, output_file="output.mp3"):
    print("🔊 Converting text to speech...")
    tts = gTTS(text=text, lang="en")
    print(tts)
    tts.save(output_file)
    print("✅ Speech saved as", output_file)

    # Play the audio using pygame
    pygame.mixer.init()
    pygame.mixer.music.load(output_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue  # Wait until the audio finishes playing


# Main Workflow
if __name__ == "__main__":
    audio_file = record_audio(duration=5)  # Record for 5 seconds
    transcribed_text = transcribe_audio(audio_file)
    # transcribed_text = "Hi how are you doing"
    if transcribed_text:
        text_to_speech(transcribed_text)

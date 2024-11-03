# backend/utils/speech_synthesis.py
from gtts import gTTS
from pydub import AudioSegment

def text_to_speech(text, filename):
    tts = gTTS(text=text, lang='en')
    tts.save(f"{filename}.mp3")
    # Optional: Convert to a more compatible format
    AudioSegment.from_mp3(f"{filename}.mp3").export(f"{filename}.wav", format="wav")
    return f"{filename}.wav"

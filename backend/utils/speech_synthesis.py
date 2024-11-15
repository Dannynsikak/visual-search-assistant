from gtts import gTTS
from pydub import AudioSegment

def text_to_speech(text, filename, lang='en', speed=1.0, volume=1.0):
    # Generate audio
    tts = gTTS(text=text, lang=lang)
    mp3_path = f"{filename}.mp3"
    tts.save(mp3_path)
    
    # Adjust speed and volume
    audio = AudioSegment.from_mp3(mp3_path)
    audio = audio.speedup(playback_speed=speed).apply_gain(volume)
    wav_path = f"{filename}.wav"
    audio.export(wav_path, format="wav")
    
    return {"mp3": mp3_path, "wav": wav_path}  # Return both formats

from TTS.api import TTS
from pydub import AudioSegment

def text_to_speech(text, filename, lang='en', speed=1.0, volume=1.0):
    model_name = TTS.list_models()[0]  # Select the first available model
    tts = TTS(model_name)

    # Generate audio
    wav_path = f"{filename}.wav"
    tts.tts_to_file(text=text, file_path=wav_path)

    # Adjust speed and volume using pydub
    audio = AudioSegment.from_file(wav_path)
    audio = audio.speedup(playback_speed=speed).apply_gain(volume)
    adjusted_wav_path = f"{filename}_adjusted.wav"
    audio.export(adjusted_wav_path, format="wav")
    
    # Optionally, export an MP3 version as well
    mp3_path = f"{filename}_adjusted.mp3"
    audio.export(mp3_path, format="mp3")

    return {"wav": adjusted_wav_path, "mp3": mp3_path}

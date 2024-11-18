import uuid
from transformers import VisionEncoderDecoderModel, AutoTokenizer, ViTImageProcessor
import torch
from PIL import Image, UnidentifiedImageError
from TTS.api import TTS
import os
import time
from scipy.io import wavfile

# Load the model, feature extractor,tokenizer and Coqui TTS
model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
# Loading the Coqui TTS Model
model_name = TTS.list_models()[0]
tts = TTS(model_name, gpu=False)

# Check if GPU is available
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

available_speakers = [
    "Daisy Studious", "Sofia Hellen", "Asya Anara",
    "Eugenio Mataracı","Viktor Menelaos", "Damien Black"
]

available_languages = ["US English", "Spanish (LatAm)"]

# Defining Variables to Hold Selected Voice and Localization
selected_speaker = available_speakers[0]
selected_language = available_languages[0]

# # TODO#6 - Managing Outputs
# # Create the output directory if it doesn't exist
os.makedirs("output_path", exist_ok=True)
# # global variable to store the last generated audio path and text
last_generated_audio = None
# last_generated_text = ""

# TODO#7 - Implementing the Trim Function.
def trim_text(text, max_length=30):
    """
    Trim the text to a maximum length and add ellipsis if it exceeds the limit.
    """
    return text[:max_length] + "..." if len(text) > max_length else text

def generate_speech_from_description(description_text: str, output_path: str, speaker: str, language: str):
    """
    Converts text to speech and saves the audio file.

    Parameters:
        description_text (str): The generated description text.
        output_path (str): Path to save the generated audio file (e.g., MP3 or WAV).
        speaker (str): Selected speaker for TTS.
        language (str): Selected language for TTS.

    Returns:
        dict: Contains audio information and status.
    """
    if not description_text:
        return {"error": "No description text provided."}

    try:
        # Generate speech
        start_time = time.time()
        tts.tts_to_file(
            description_text,
            speaker=speaker,
            language="en" if language == "US English" else "es",
            file_path=output_path,
        )
        end_time = time.time()

        # Calculate duration
        duration = round(end_time - start_time, 2)

        # Read the generated audio file
        samplerate, data = wavfile.read(output_path)
        speech_length = len(data) / samplerate

        # Update global variable
        global last_generated_audio
        last_generated_audio = output_path

        return {
            "audio_path": output_path,
            "speaker": speaker,
            "language": language,
            "speech_length": round(speech_length, 2),
            "generation_duration": duration,
            "status": "Speech generation successful.",
        }

    except Exception as e:
        return {"error": f"Failed to generate speech: {e}"}


def generate_speech(description_text: str, speaker: str, language: str):
    """
    Generates speech from text and returns metadata.

    Parameters:
        description_text (str): The text to generate speech from.
        speaker (str): Selected speaker for TTS.
        language (str): Selected language for TTS.

    Returns:
        tuple: Contains the audio path, data information, and status message.
    """
    if not description_text:
        return None,None, "Please enter some text to generate speech.", "Missing description text"

    # Generate a unique output path
    output_path = f"output_path/generated_speech_{uuid.uuid4()}.wav"

    # Call the generate_speech_from_description function
    result = generate_speech_from_description(
        description_text=description_text,
        output_path=output_path,
        speaker=speaker,
        language=language,
    )

    # Check for errors
    if "error" in result:
        return None,None, result["error"], "Error occurred during speech generation"

    # Extract information
    audio_path = result["audio_path"]
    speech_length = result["speech_length"]
    duration = result["generation_duration"]
    speaker_name = result["speaker"]
    lang = result["language"]

    # Format the text box content
    word_count = len(description_text.split())
    data_info = (
        f"Word Count: {word_count}\n"
        f"Voice: {speaker_name}\n"
        f"Localization: {lang}\n"
        f"Length of Speech: {speech_length} seconds\n"
        f"Generation Duration: {duration} seconds"
    )

    return audio_path, data_info, "Speech generation successful!", None


def get_image_description(image_path: str, mode: str = "summary") -> str:
    """
    Generates a description for the image based on the specified mode and generates speech for it.

    Parameters:
        image_path (str): The path to the image file.
        mode (str): The mode for description; could be 'summary' or 'detailed'.

    Returns:
        str: The generated description.
    """
    try:
        # Load the image and preprocess it for the model
        image = Image.open(image_path)
        inputs = feature_extractor(images=image, return_tensors="pt").to(device)
        
        # Generate caption using the model
        outputs = model.generate(**inputs, max_length=50 if mode == "summary" else 100)
        
        # Decode the generated caption
        description = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # # Generate speech from the description and save it
        # generate_speech_from_description(description, output_path="output_path", speaker=selected_speaker,language=selected_language)

        return description

    except UnidentifiedImageError:
        error_message = "Invalid image format. Please provide a valid image file."
        print(error_message)
        return error_message
    except Exception as e:
        error_message = "An error occurred during image processing."
        print(f"{error_message}: {e}")
        return error_message

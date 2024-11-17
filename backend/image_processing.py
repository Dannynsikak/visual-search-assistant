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

# available_speakers = [
#     "Daisy Studious", "Sofia Hellen", "Asya Anara",
#     "Eugenio Mataracı","Viktor Menelaos", "Damien Black"
# ]

# available_languages = ["US English", "Spanish (LatAm)"]

# # Defining Variables to Hold Selected Voice and Localization
# selected_speaker = available_speakers[0]
# selected_language = available_languages[0]

# # TODO#6 - Managing Outputs
# # Create the output directory if it doesn't exist
# os.makedirs("output_path", exist_ok=True)
# # global variable to store the last generated audio path and text
# last_generated_audio = None
# last_generated_text = ""

# TODO#7 - Implementing the Trim Function.
def trim_text(text, max_length=30):
    """
    Trim the text to a maximum length and add ellipsis if it exceeds the limit.
    """
    return text[:max_length] + "..." if len(text) > max_length else text

def generate_speech_from_description(description_text: str, output_path: str,speaker: str, language: str):
    """
    Converts text to speech and saves the audio file.

    Parameters:
        description_text (str): The generated description text.
        output_path (str): Path to save the generated audio file (e.g., MP3 or WAV).
        speaker (str): Selected speaker for TTS.
        language (str): Selected language for TTS.
    """
    if not description_text:
        return {"error": "No description text provided."}
    
    
    output_path = f"temp/generated_speech_{uuid.uuid4()}.wav"
    start_time = time.time()
    # Generate speech from the description text
    tts.tts_to_file(description_text,speaker=speaker,language="en" if language == "US English" else "es",
    file_path=output_path)

    # TODO#9 - Managing Duration and Tracking Variables
    end_time = time.time()
    duration = round(end_time - start_time, 2)

    # TODO#10 - Extracting Audio Information
    # calculate the length of the generated speech
    samplerate, data = wavfile.read(output_path)
    speech_length = len(data) / samplerate

    # TODO#11 - Return Audio Information
    return {
            "audio_path": output_path,
            "speaker": speaker,
            "language": language,
            "speech_length": round(speech_length, 2),
            "generation_duration": duration,
            "status": "Speech generation successful."
        }
        

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

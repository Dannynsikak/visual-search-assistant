import uuid
from transformers import VisionEncoderDecoderModel, AutoTokenizer, ViTImageProcessor
import torch
from PIL import Image, UnidentifiedImageError
from TTS.api import TTS
import os
import time
from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
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

#  Create the output directory if it doesn't exist
os.makedirs("output_path", exist_ok=True)
os.makedirs("output", exist_ok=True)
# global variable to store the last generated audio path and text
last_generated_audio = None
last_generated_text = ""


# Implementing the Trim Function.
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

        # Update global variable
        global last_generated_audio,last_generated_text
        last_generated_audio = output_path
        last_generated_text =  description_text

          # Read the generated audio file
        samplerate, data = wavfile.read(output_path)
        speech_length = len(data) / samplerate

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

# Waveform Function
def generate_waveform():
    # Initialize Global Variables and Input Validation
    global last_generated_audio, last_generated_text

    # Check if a valid audio file exists
    if not last_generated_audio or not os.path.exists(last_generated_audio):
        return None, "No valid audio file found to generate waveform."

    # Read Audio File and Create Time Axis
    samplerate, data = wavfile.read(last_generated_audio)
    time_axis = np.linspace(0, len(data) / samplerate, num=len(data))

    # Plot the Waveform with Custom Styling
    fig, ax = plt.subplots(figsize=(8, 4), facecolor='#1E1E1E')  # Dark background

    # Plot the Waveform with Custom Styling
    ax.plot(time_axis, data, color='cyan', alpha=0.8, linewidth=1.2)

    # Styling grid and axes for a modern look
    ax.set_facecolor('#2E2E2E')  # Set darker plot background
    ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.5)  # Add grid lines
    ax.spines['bottom'].set_color('white')  # Set bottom spine color to white
    ax.spines['left'].set_color('white')  # Set left spine color to white
    ax.tick_params(axis='x', colors='white')  # Set x-axis tick color
    ax.tick_params(axis='y', colors='white')  # Set y-axis tick color
    ax.set_xlabel("Time (seconds)", color='white')  # Label x-axis
    ax.set_ylabel("Amplitude", color='white')  # Label y-axis

    # Add a Title to the Plot
    # Trim long text for display in title
    trimmed_text = trim_text(last_generated_text)
    ax.set_title(f"Waveform for text input: '{trimmed_text}'", color='white', fontsize=14)

    # Save the waveform image
    waveform_image_path = "output/waveform.png"
    plt.savefig(waveform_image_path, transparent=True)
    plt.close()

    return waveform_image_path, "Waveform generated successfully!"

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
        
        return description

    except UnidentifiedImageError:
        error_message = "Invalid image format. Please provide a valid image file."
        print(error_message)
        return error_message
    except Exception as e:
        error_message = "An error occurred during image processing."
        print(f"{error_message}: {e}")
        return error_message

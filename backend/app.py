import os
from pathlib import Path
import uuid
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from image_processing import generate_speech_from_description, get_image_description
from chromadb_config import add_to_database, query_database
from typing import List


app = FastAPI()

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# Serve static files from the "temp" directory
app.mount("/temp", StaticFiles(directory="temp"), name="temp")

available_speakers = [
    "Daisy Studious", "Sofia Hellen", "Asya Anara",
    "Eugenio Mataracı","Viktor Menelaos", "Damien Black"
]

available_languages = ["US English", "Spanish (LatAm)"]

# Defining Variables to Hold Selected Voice and Localization
selected_speaker = available_speakers[0]
selected_language = available_languages[0]

# Create temp directory if not exists
if not os.path.exists("temp"):
    os.makedirs("temp")

# TODO#6 - Managing Outputs
# Create the output directory if it doesn't exist
os.makedirs("output_path", exist_ok=True)
# global variable to store the last generated audio path and text
last_generated_audio = None
last_generated_text = ""

@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...), lang: str = "en", description_mode: str = "summary"):
    try:
        # Validate file type
        if not file.content_type.startswith("image/"):
            return JSONResponse(content={"error": "Invalid file type. Please upload an image file."}, status_code=400)
        
        # Save the uploaded file temporarily
        temp_file_path = f"temp/{uuid.uuid4()}_{file.filename}"
        with open(temp_file_path, "wb") as buffer:
            buffer.write(file.file.read())
        upload_response = {"status": "File uploaded successfully.", "file_path": temp_file_path}
        
        # Process image to get description
        description = get_image_description(temp_file_path, mode=description_mode)
        if "error" in description:
            return JSONResponse(content={"error": description}, status_code=500)
        process_response = {"status": "Image processed successfully.", "description": description}
        
        # Add description to the database
        item_id = os.path.splitext(file.filename)[0]
        add_to_database(item_id, description)
        
        # Generate audio from description
        audio_paths = generate_speech_from_description(description,speaker=selected_speaker,language=selected_language)
        print(f"audio_paths{audio_paths}")
        return {
            "upload_response": upload_response,
            "process_response": process_response,
            "database_response": {"status": "Description added to database.", "item_id": item_id},
            "audio_response": {"status": "Audio generated successfully.", "audio_paths": audio_paths},
        }

    except Exception as e:
        return JSONResponse(content={"error": f"An error occurred: {str(e)}"}, status_code=500)

@app.get("/audio-control/{action}")
async def audio_control(action: str, audio_path: str):
    """
    Control audio playback.
    Actions: 'play', 'pause', 'stop'.
    """
    try:
        if action == "play":
            os.system(f"start {audio_path}" if os.name == "nt" else f"xdg-open {audio_path}")
        elif action == "pause":
            # Pause functionality would depend on the playback library
            pass
        elif action == "stop":
            # Stop functionality would depend on the playback library
            pass
        else:
            return JSONResponse(content={"error": f"Invalid action: {action}"}, status_code=400)
        
        return {"status": f"Audio {action} action performed on {audio_path}"}
    
    except Exception as e:
        return JSONResponse(content={"error": f"An error occurred: {str(e)}"}, status_code=500)


@app.get("/latest-recordings", response_model=List[str])
def get_latest_recordings():
    try:
        # List all .wav files in the "output_path" directory
        recordings = list(Path("output_path").glob("*.wav"))
        
        # Sort files by modified time, most recent first
        recordings.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        # Get the first recordings and construct URLs
        latest_recordings = [f"/output_path/{file.name}" for file in recordings[:1]]
        
        return latest_recordings
    
    except Exception as e:
        return JSONResponse(content={"error": f"An error occurred: {str(e)}"}, status_code=500)

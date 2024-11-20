import os
from pathlib import Path
import uuid
from fastapi import FastAPI, File, Form, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from image_processing import  generate_speech, get_image_description
from chromadb_config import add_to_database
from typing import List
import traceback

app = FastAPI()

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

class CustomStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):
        response = await super().get_response(path, scope)
        # Check if the file is a .wav and set the MIME type
        if path.endswith(".wav"):
            response.headers["Content-Type"] = "audio/wav"
        return response
    
# Serve static files from the "temp" directory
app.mount("/temp", StaticFiles(directory="temp"), name="temp")
app.mount("/output_path", CustomStaticFiles(directory="output_path"), name="output_path")

available_speakers = [
    "Daisy Studious", "Sofia Hellen", "Asya Anara",
    "Eugenio Mataracı","Viktor Menelaos", "Damien Black"
]
available_languages = ["US English", "Spanish (LatAm)"]

# Defining Variables to Hold Selected Voice and Localization
selected_speaker = available_speakers[0]
selected_language = available_languages[0]

# Create temp directory if not exists
os.makedirs("temp", exist_ok=True)

# Create the output directory if it doesn't exist
os.makedirs("output_path", exist_ok=True)
# global variable to store the last generated audio path and text


@app.post("/upload-image")
async def upload_image(
    request: Request,
    file: UploadFile = File(...),
    lang: str = "en",
    description_mode: str = "summary",
    speaker: str = Form(...),
    language: str = Form(...),
):
    try:
        # Validate file type
        if not file.content_type.startswith("image/"):
            return JSONResponse(
                content={"error": "Invalid file type. Please upload an image file."},
                status_code=400
            )
        
        # Validate speaker and language inputs
        if speaker not in available_speakers:
            return JSONResponse(
                content={"error": f"Invalid speaker. Choose from {available_speakers}."},
                status_code=400
            )
        
        if language not in available_languages:
            return JSONResponse(
                content={"error": f"Invalid language. Choose from {available_languages}."},
                status_code=400
            )
        
        temp_file_path = f"temp/{uuid.uuid4()}_{file.filename}"
        with open(temp_file_path, "wb") as buffer:
            buffer.write(await file.read())

        description = get_image_description(temp_file_path, mode=description_mode)
        if not description:
            return JSONResponse(content={"error": "Failed to generate description."}, status_code=500)

        item_id = os.path.splitext(file.filename)[0]
        add_to_database(item_id, description)

        # Generate speech from description
        audio_path, data_info, message, error = generate_speech(
            description,
            speaker,
            language
        )

        if error:
            return JSONResponse(content={"error": message}, status_code=500)
        
        return {
            "status": "Success",
            "description": description,
            "audio_info": data_info,
            "audio_path": f"{request.base_url}{audio_path}"
        }

    except Exception as e:
        error_message = f"An error occurred: {str(e)}\n{traceback.format_exc()}"
        print(error_message)
        return JSONResponse(content={"error": error_message}, status_code=500)

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
def get_latest_recordings(request: Request,):
    try:
        # List all .wav files in the "output_path" directory
        recordings = list(Path("output_path").glob("*.wav"))
        
        # Sort files by modified time, most recent first
        recordings.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        # Get the first recordings and construct URLs
        latest_recordings = [f"{request.base_url}output_path/{file.name}" for file in recordings[:6]]
        
        return latest_recordings
    
    except Exception as e:
        return JSONResponse(content={"error": f"An error occurred: {str(e)}"}, status_code=500)

import os
<<<<<<< HEAD
=======
from pathlib import Path
>>>>>>> 221de2e8fc6779426901f2f3eb86618b73e0c2c2
import uuid
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from image_processing import get_image_description
<<<<<<< HEAD
from chromadb_config import add_to_database
from utils.speech_synthesis import text_to_speech
=======
from chromadb_config import add_to_database, query_database
from utils.speech_synthesis import text_to_speech
from typing import List

>>>>>>> 221de2e8fc6779426901f2f3eb86618b73e0c2c2

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
<<<<<<< HEAD
=======
app.mount("/static", StaticFiles(directory="static"), name="static")
>>>>>>> 221de2e8fc6779426901f2f3eb86618b73e0c2c2

# Create temp directory if not exists
if not os.path.exists("temp"):
    os.makedirs("temp")

<<<<<<< HEAD
=======
# Create static directory if not exists
if not os.path.exists("static"):
    os.makedirs("static")
>>>>>>> 221de2e8fc6779426901f2f3eb86618b73e0c2c2

@app.post("/upload-image/")
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
        audio_paths = text_to_speech(description, temp_file_path, lang=lang)
        
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
<<<<<<< HEAD
=======


@app.get("/latest-recordings", response_model=List[str])
def get_latest_recordings():
    try:
        # List all .mp3 files in the "temp" directory
        recordings = list(Path("temp").glob("*.mp3"))
        
        # Sort files by modified time, most recent first
        recordings.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        # Get the latest six recordings and construct URLs
        latest_recordings = [f"/temp/{file.name}" for file in recordings[:6]]
        
        return latest_recordings
    
    except Exception as e:
        return JSONResponse(content={"error": f"An error occurred: {str(e)}"}, status_code=500)
>>>>>>> 221de2e8fc6779426901f2f3eb86618b73e0c2c2

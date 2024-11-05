import os
import uuid
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from image_processing import get_image_description
from chromadb_config import add_to_database, query_database
from utils.speech_synthesis import text_to_speech

app = FastAPI()

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Adjust this URL to match your frontend's address
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# Serve static files from the "temp" directory
app.mount("/temp", StaticFiles(directory="temp"), name="temp")

# Ensure the "temp" directory exists
if not os.path.exists("temp"):
    os.makedirs("temp")

@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...), lang: str = "en", description_mode: str = "summary"):
    try:
        # Validate file type
        if not file.content_type.startswith("image/"):
            return {"error": "Invalid file type. Please upload an image file."}, 400
        
        # Step 1: Save the uploaded file temporarily
        temp_file_path = f"temp/{uuid.uuid4()}_{file.filename}"
        with open(temp_file_path, "wb") as buffer:
            buffer.write(file.file.read())
        upload_response = {"status": "File uploaded successfully.", "file_path": temp_file_path}
        
        # Step 2: Process image to get description
        description = get_image_description(temp_file_path, mode=description_mode)
        if "error" in description:
            return {"error": description}, 500
        process_response = {"status": "Image processed successfully.", "description": description}
        
        # Step 3: Add description to the database
        item_id = os.path.splitext(file.filename)[0]
        add_to_database(item_id, description)
        
        # Step 4: Generate audio from the description
        audio_paths = text_to_speech(description, temp_file_path, lang=lang)
        
        # Clean up the temporary file after processing
        os.remove(temp_file_path)
        
        return {
            "upload_response": upload_response,
            "process_response": {"status": "Image processed successfully.", "description": description},
            "database_response": {"status": "Description added to database.", "item_id": item_id},
            "audio_response": {"status": "Audio generated successfully.", "audio_paths": audio_paths},
        }

    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}, 500

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
            return {"error": f"Invalid action: {action}"}, 400
        
        return {"status": f"Audio {action} action performed on {audio_path}"}
    
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}, 500

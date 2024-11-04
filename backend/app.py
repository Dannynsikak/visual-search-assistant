import os
import uuid
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from image_processing import get_image_description
from chromadb_config import add_to_database, query_database
from utils.speech_synthesis import text_to_speech
from fastapi.staticfiles import StaticFiles


app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Adjust this URL to match your frontend's address
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.mount("/temp", StaticFiles(directory="temp"), name="temp")

# Ensure the temp directory exists
if not os.path.exists("temp"):
    os.makedirs("temp")

@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    try:
        if not file.content_type.startswith("image/"):
            return {"error": "Invalid file type"}, 400
        
        # Generate a unique filename to prevent overwriting
        temp_file_path = f"temp/{uuid.uuid4()}_{file.filename}"

        # Write the uploaded file to the unique path
        with open(temp_file_path, "wb") as buffer:
            buffer.write(file.file.read())

        # Process as before
        description = get_image_description(temp_file_path)
        item_id = os.path.splitext(file.filename)[0]
        add_to_database(item_id, description)
        audio_path = text_to_speech(description, temp_file_path)
        print(f"Generated audio path: {audio_path}")  # Debugging line


        os.remove(temp_file_path)  # Clean up after processing
        return {"description": description, "audio_path": audio_path}
    except Exception as e:
        return {"error": str(e)}, 500

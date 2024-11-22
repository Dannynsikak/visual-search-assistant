import asyncio
import os
from pathlib import Path
import uuid
from fastapi import FastAPI, File, Form, HTTPException, UploadFile, Request,Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from image_processing import  generate_speech, generate_waveform, get_image_description
from chromadb_config import add_to_database
from typing import List
import traceback

app = FastAPI()
lock = asyncio.Lock()
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
app.mount("/output", StaticFiles(directory="output"), name="output")

# Create temp directory if not exists
os.makedirs("temp", exist_ok=True)

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

@app.get("/latest-recordings", response_model=List[str])
def get_latest_recordings(request: Request,):
    try:
        # List all .wav files in the "output_path" directory
        recordings = list(Path("output_path").glob("*.wav"))
        
        # Sort files by modified time, most recent first
        recordings.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        # Get the first recordings and construct URLs
        latest_recordings = [f"{request.base_url}output_path/{file.name}" for file in recordings[:3]]
        
        return latest_recordings
    
    except Exception as e:
        return JSONResponse(content={"error": f"An error occurred: {str(e)}"}, status_code=500)

@app.get("/get-waveform")
async def get_waveform():
    async with lock: 
        waveform_image_path, message = generate_waveform()
    
    # Check if the waveform image exists
    if not os.path.exists(waveform_image_path):
        raise HTTPException(status_code=404, detail=message)

    # Serve the waveform image file
    return FileResponse(waveform_image_path, media_type="image/png")
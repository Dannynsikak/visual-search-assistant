## Visual Search Assistant

The Visual Search Assistant is a powerful tool that allows users to upload images for description and audio generation, making it accessible and useful for visually impaired users or anyone needing audio feedback on visual content. It leverages deep learning for image captioning and generates descriptions in either summary or detailed modes, providing flexible output options. Audio files of the descriptions are also created, allowing users to listen to generated descriptions.

## Table of Contents

Features
Technologies Used
Setup Instructions
Usage
Project Structure
API Endpoints
Future Improvements
Features
Image Upload and Processing
File Upload: Users can upload image files in various formats (JPEG, PNG).
File Validation: Ensures that only valid image files are uploaded.
Progress Feedback: Shows a progress bar while uploading the image.

## Image Description Generation

Dynamic Description Modes: Supports two modes for description:
Summary Mode: A brief overview of the image.
Detailed Mode: A more comprehensive description of the image content.
Description Text Output: Displays the generated text description for user reference.
Audio Generation
Audio Conversion: Generates audio files (MP3/WAV) from the image description.
Audio Playback: Provides a built-in audio player to play the generated description audio.
File Links: Dynamic path linking to server-stored audio files.

## Error Handling

Invalid File Handling: Detects non-image files and prompts users to upload valid formats.
Playback Error Handling: Catches errors that occur during audio playback and provides feedback.
Storage and Database Interaction
Database Logging: Stores generated descriptions in the database for future retrieval.
Unique File Paths: Organizes uploaded files and audio files with unique identifiers for easy management.

## Responsive and Accessible UI

Frontend Framework: Built with React and Tailwind CSS, providing a responsive and visually appealing UI.
Accessibility: Designed to be user-friendly for all users, with a focus on accessible elements for audio playback.

## Technologies Used

# Frontend:

React: JavaScript framework for building the UI.
Tailwind CSS: Utility-first CSS framework for fast, responsive design.
Axios: Used for handling HTTP requests to the backend server.

# Backend:

Python with FastAPI: High-performance web framework for building API endpoints.
Transformers Library: Used for the image-to-text model, specifically the VisionEncoderDecoderModel.
Pillow: Image processing library for loading and validating images.
Torch: PyTorch for running deep learning models.

# Machine Learning:

VisionEncoderDecoderModel: A pre-trained model that converts images into descriptive text.
ViTFeatureExtractor and AutoTokenizer: Tools for pre-processing images and tokenizing text to make them compatible with the model.

## Other:

FFmpeg: Converts text to audio in various formats (MP3, WAV).
MongoDB or SQL Database: Stores metadata of generated descriptions.

## Setup Instructions

Prerequisites
Node.js (for the frontend)
Python 3.7+ (for the backend)
FFmpeg (for audio conversion)
MongoDB or SQL Database (for data storage)
Steps
Clone the repository:

git clone https://github.com:Dannynsikak/visual-search-assistant.git
cd visual-search-assistant

## Backend Setup:

Set up a virtual environment and install Python dependencies:

cd backend
python -m venv env
source env/bin/activate # On Windows, use `env\Scripts\activate`
pip install -r requirements.txt
Ensure FFmpeg is installed and available in your PATH.

## Frontend Setup:

Install dependencies:

cd frontend
npm install
Environment Variables:

Create a .env file in both frontend and backend directories, specifying necessary variables (e.g., API endpoints, database URLs).

## Run the Application:

Start the backend server:

cd backend
uvicorn main:app --reload
Start the frontend development server:

cd frontend
npm start
Usage
Upload Image: Go to the upload section and select an image file.
Choose Description Mode: Select either “Summary” or “Detailed” for the description type.
Submit for Processing: Click “Upload and Describe” to send the image to the backend.
View Results:
Text Output: View the generated description.
Audio Output: Use the audio player to listen to the description.
Project Structure
graphql

visual-search-assistant/
├── backend/
│ ├── main.py # Main FastAPI server file
│ ├── routes/
│ │ └── image_processing.py # Handles image upload and description generation
│ ├── models/ # Machine learning models for image-to-text
│ └── utils/
│ └── audio_conversion.py # Text-to-audio conversion utilities
├── frontend/
│ ├── public/
│ ├── src/
│ │ ├── components/
│ │ │ ├── SearchComponent.tsx # Main upload component with UI
│ │ └── services/
│ │ └── api.js # API service for HTTP requests
│ └── App.js
└── README.md

## API Endpoints

POST /upload-image/: Accepts an image file, processes it, and returns a description and audio file paths.
Parameters:
file: Image file (required)
description_mode: summary or detailed
Response:
description: Generated description text
audio_paths: URLs to generated audio files (MP3 and WAV)
Future Improvements
Image Caching: Add caching for previously processed images to improve performance.
Additional Modes: Include additional modes, such as “creative” or “contextual.”
Multilingual Support: Generate descriptions in different languages.
Extended Error Logging: Implement more robust logging for better debugging.
License
This project is licensed under the MIT License. See the LICENSE file for more information.

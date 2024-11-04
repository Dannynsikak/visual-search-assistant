// frontend/src/components/SearchComponent.tsx
import type React from "react";
import { useState } from "react";
import axios from "axios";

const SearchComponent: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [description, setDescription] = useState("");
  const [audioPath, setAudioPath] = useState("");
  const [error, setError] = useState("");

  const handleUpload = async () => {
    setError(""); // Clear previous errors
    const formData = new FormData();

    if (file) {
      formData.append("file", file);

      try {
        const response = await axios.post(
          "http://localhost:8000/upload-image/",
          formData,
          {
            headers: { "Content-Type": "multipart/form-data" },
          }
        );
        console.log("Response data:", response.data);

        if (response.data) {
          setDescription(
            response.data.description || "No description available."
          );
          setAudioPath(response.data.audio_path || "");
        } else {
          setError("Unexpected response structure.");
        }
      } catch (err) {
        setError("An error occurred while uploading. Please try again.");
        console.error("Upload error:", err);
        if (axios.isAxiosError(err)) {
          console.error("Error response:", err.response);
        }
      }
    } else {
      setError("Please select a file before uploading.");
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="flex flex-col max-w-md w-full p-6 bg-white shadow-lg rounded-lg">
        <label
          htmlFor="file-upload"
          className="block text-lg font-semibold text-gray-800 mb-4"
        >
          Upload an image:
        </label>
        <input
          id="file-upload"
          name="file"
          type="file"
          accept="image/*"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
          className="text-red-600 font-bold mb-4 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 p-2"
        />
        <button
          type="button"
          onClick={handleUpload}
          className="w-full inline-flex items-center justify-center px-4 py-2 bg-blue-600 text-white text-lg font-semibold rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
        >
          Upload and Describe
        </button>
        {error && <p className="mt-3 text-red-500 text-sm">{error}</p>}
        {description && (
          <p className="mt-2 text-gray-700 text-md">{description}</p>
        )}
        {audioPath && (
          <div className="mt-4">
            <audio
              controls
              src={`http://localhost:8000/${audioPath}`}
              className="w-full"
              onError={(e) => {
                console.error("Audio playback error:", e);
                const target = e.target as HTMLAudioElement;
                console.error("Error details:", target.error);
              }}
            >
              <track
                src={"http://localhost:8000/captions.vtt"} // Adjust path as necessary
                kind="captions"
                srcLang="en"
                label="English"
                default
              />
            </audio>
          </div>
        )}
      </div>
    </div>
  );
};

export default SearchComponent;

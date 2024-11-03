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
      }
    } else {
      setError("Please select a file before uploading.");
    }
  };

  return (
    <div>
      <input
        name="file"
        type="file"
        accept="image/*"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
      />
      <button type="button" onClick={handleUpload}>
        Upload and Describe
      </button>

      {error && <p style={{ color: "red" }}>{error}</p>}
      {description && <p>{description}</p>}
      {audioPath && (
        <audio controls src={`http://localhost:8000/${audioPath}`}>
          <track
            src={"http://localhost:8000/captions.vtt"} // Adjust path as necessary
            kind="captions"
            srcLang="en"
            label="English"
            default
          />
        </audio>
      )}
    </div>
  );
};

export default SearchComponent;

import type React from "react";
import { useDispatch, useSelector } from "react-redux";
import axios from "axios";
import {
  setDescriptionMode,
  setDescription,
  setAudioPath,
  setError,
  setLoading,
  setUploadProgress,
} from "../slice/searchSlice";
import type { AppDispatch, RootState } from "../store";
import { useState } from "react";
import { ToggleButton } from "./ToggleBtn";

const SearchComponent: React.FC = () => {
  const dispatch: AppDispatch = useDispatch();

  const [file, setFile] = useState<File | null>(null);
  const descriptionMode = useSelector(
    (state: RootState) => state.search.descriptionMode
  );
  const loading = useSelector((state: RootState) => state.search.loading);
  const uploadProgress = useSelector(
    (state: RootState) => state.search.uploadProgress
  );
  const error = useSelector((state: RootState) => state.search.error);
  const description = useSelector(
    (state: RootState) => state.search.description
  );
  const audioPath = useSelector((state: RootState) => state.search.audioPath);

  const handleUpload = async () => {
    dispatch(setError(""));
    dispatch(setLoading(true));
    dispatch(setUploadProgress(0));

    const formData = new FormData();
    if (file) {
      formData.append("file", file);
      formData.append("description_mode", descriptionMode);

      try {
        const response = await axios.post(
          "http://localhost:8000/upload-image/",
          formData,
          {
            headers: { "Content-Type": "multipart/form-data" },
            onUploadProgress: (progressEvent) => {
              if (progressEvent.total) {
                const percent = Math.round(
                  (progressEvent.loaded * 100) / progressEvent.total
                );
                dispatch(setUploadProgress(percent));
              }
            },
          }
        );

        console.log("Response data:", response.data);

        if (response.data) {
          dispatch(
            setDescription(
              response.data.process_response?.description ||
                "No description available."
            )
          );
          dispatch(
            setAudioPath(response.data.audio_response?.audio_paths?.mp3 || "")
          );
        } else {
          dispatch(setError("Unexpected response structure."));
        }
      } catch (err) {
        dispatch(
          setError("An error occurred while uploading. Please try again.")
        );
        console.error("Upload error:", err);
      } finally {
        dispatch(setLoading(false));
      }
    } else {
      dispatch(setError("Please select a file before uploading."));
      dispatch(setLoading(false));
    }
  };

  return (
    <div className="p-2">
      <ToggleButton />
      <div className="flex items-center justify-center min-h-screen">
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
          <label
            htmlFor="description-mode"
            className="block text-md font-semibold text-gray-800 mb-2"
          >
            Description Mode:
          </label>
          <select
            id="description-mode"
            value={descriptionMode}
            onChange={(e) => dispatch(setDescriptionMode(e.target.value))}
            className="mb-4 border border-gray-300 bg-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 p-2"
          >
            <option value="summary">Summary</option>
            <option value="detailed">Detailed</option>
          </select>
          <button
            type="button"
            onClick={handleUpload}
            className="w-full inline-flex items-center justify-center px-4 py-2 bg-blue-600 text-white text-lg font-semibold rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            disabled={loading}
          >
            {loading ? "Uploading..." : "Upload and Describe"}
          </button>
          {loading && (
            <div className="mt-2 text-gray-500 text-sm">
              {uploadProgress}% uploaded...
            </div>
          )}
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
                  src={"http://localhost:8000/captions.vtt"}
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
    </div>
  );
};

export default SearchComponent;

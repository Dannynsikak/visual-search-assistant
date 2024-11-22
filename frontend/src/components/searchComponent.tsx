import type React from "react";
import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import axios from "axios";
import {
  setDescriptionMode,
  setDescription,
  setError,
  setLoading,
  setUploadProgress,
  setAudioPath,
} from "../slice/searchSlice";
import type { AppDispatch, RootState } from "../store";
import { ToggleButton } from "./ToggleBtn";
import ToggleModal from "./ToggleModel";
import { fetchWaveform } from "../slice/waveFormSlice";

const availableSpeakers = [
  "Daisy Studious",
  "Sofia Hellen",
  "Asya Anara",
  "Eugenio Mataracı",
  "Viktor Menelaos",
  "Damien Black",
];

const availableLanguages = ["US English", "Spanish (LatAm)"];

const SearchComponent: React.FC = () => {
  const dispatch: AppDispatch = useDispatch();

  const [file, setFile] = useState<File | null>(null);
  const [selectedSpeaker, setSelectedSpeaker] = useState(availableSpeakers[0]);
  const [selectedLanguage, setSelectedLanguage] = useState(
    availableLanguages[0]
  );

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
  const audioPath = useSelector((state: RootState) => state.search.audio_paths);
  const waveform = useSelector((state: RootState) => state.waveform.waveform);
  const waveformLoading = useSelector(
    (state: RootState) => state.waveform.loading
  );
  const waveformError = useSelector((state: RootState) => state.waveform.error);

  const handleUpload = async () => {
    dispatch(setError(""));
    dispatch(setLoading(true));
    dispatch(setUploadProgress(0));

    const formData = new FormData();
    if (file) {
      formData.append("file", file);
      formData.append("description_mode", descriptionMode);
      formData.append("speaker", selectedSpeaker);
      formData.append("language", selectedLanguage);

      try {
        const response = await axios.post(
          "http://localhost:8000/upload-image",
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
        if (response.data) {
          dispatch(
            setDescription(
              response.data.description || "No description available."
            )
          );
          dispatch(setAudioPath(response.data.audio_path));
          dispatch(fetchWaveform());
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
      <ToggleModal />
      {/* Project Name */}
      <h1 className="text-3xl font-bold text-center text-gray-800">
        Visual Search Assistant
      </h1>
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
            className="mb-4 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 p-2"
          >
            <option value="summary">Summary</option>
            <option value="detailed">Detailed</option>
          </select>

          <label
            htmlFor="speaker"
            className="block text-md font-semibold text-gray-800 mb-2"
          >
            Speaker:
          </label>
          <select
            id="speaker"
            value={selectedSpeaker}
            onChange={(e) => setSelectedSpeaker(e.target.value)}
            className="mb-4 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 p-2"
          >
            {availableSpeakers.map((speaker) => (
              <option key={speaker} value={speaker}>
                {speaker}
              </option>
            ))}
          </select>

          <label
            htmlFor="language"
            className="block text-md font-semibold text-gray-800 mb-2"
          >
            Language:
          </label>
          <select
            id="language"
            value={selectedLanguage}
            onChange={(e) => setSelectedLanguage(e.target.value)}
            className="mb-4 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 p-2"
          >
            {availableLanguages.map((language) => (
              <option key={language} value={language}>
                {language}
              </option>
            ))}
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
            <div className="mt-2 text-gray-500 text-sm text-center">
              {uploadProgress}% uploaded...
            </div>
          )}
          {error && <p className="mt-3 text-red-500 text-sm">{error}</p>}
          {description && (
            <p className="mt-2 text-gray-700 text-md">{description}</p>
          )}
          {audioPath ? (
            <div className="mt-4">
              <audio controls src={audioPath} className="w-full" autoPlay>
                <track
                  src="http://localhost:8000/captions.vtt"
                  kind="captions"
                  srcLang="en"
                  label="English"
                  default
                />
              </audio>
            </div>
          ) : (
            <p className="text-gray-500 text-center font-medium">
              Upload an Image to Generate Speech
            </p>
          )}
          {/* Display waveform after fetching */}
          {waveformLoading ? (
            <p className="mt-2 text-gray-500 text-sm">Loading waveform...</p>
          ) : waveform ? (
            <div className="mt-4">
              <img
                src={waveform}
                alt="generated waveform"
                className="w-full max-w-[100%] inline-block"
              />
            </div>
          ) : waveformError ? (
            <p className="mt-2 text-red-500 text-sm">{waveformError}</p>
          ) : null}
        </div>
      </div>
    </div>
  );
};

export default SearchComponent;

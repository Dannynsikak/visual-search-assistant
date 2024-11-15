import type React from "react";
import { useEffect, useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import type { RootState } from "../store";
import type { AppDispatch } from "../store";

const LatestRecordings: React.FC = () => {
  const dispatch: AppDispatch = useDispatch();
  const [localStorageRecordings, setLocalStorageRecordings] = useState<
    string[]
  >([]);

  // Select the necessary state from Redux store
  const { recordings, loading, error } = useSelector(
    (state: RootState) => state.recordings // Fetch from the recordings slice
  );

  const handleError = (
    event: React.SyntheticEvent<HTMLAudioElement, Event>
  ) => {
    console.error("Audio failed to load or play", event);
    // You can also set the state to show an error message to the user
  };

  useEffect(() => {
    // Retrieve saved audio from localStorage
    const savedAudio = localStorage.getItem("audioPath");
    if (savedAudio) {
      setLocalStorageRecordings([savedAudio]);
    }
  }, [dispatch]);

  // Log state for debugging
  console.log("Recordings:", recordings);
  console.log("Loading status:", loading);
  console.log("Error (if any):", error);

  return (
    <div className="recordings-list h-full p-6 bg-white shadow-lg overflow-y-auto w-full max-w-md">
      <h2 className="text-2xl font-semibold mb-4 text-gray-800 border-b pb-2">
        Recent Recordings
      </h2>

      {loading && <p className="text-gray-500 text-center mt-4">Loading...</p>}

      {error && <p className="text-red-500 text-center mt-4">{error}</p>}

      {/* Display recordings from Redux or localStorage */}
      {localStorageRecordings.length > 0 ? (
        <ul className="space-y-4">
          {/* Render localStorage audio if available */}
          {localStorageRecordings.map((audioUrl, index) => (
            <li key={index} className="bg-gray-100 rounded p-4 shadow-md">
              <audio
                controls
                className="w-full mt-2"
                onPlay={() => console.log("Audio started playing")}
                onPause={() => console.log("Audio paused")}
                onError={handleError}
              >
                <source src={audioUrl} type="audio/mp3" />
                Your browser does not support the audio element.
                {/* Optional: Add captions if you have a captions file */}
                <track
                  src="http://localhost:8000/captions.vtt"
                  kind="captions"
                  srcLang="en"
                  label="English"
                  default
                />
              </audio>
            </li>
          ))}
        </ul>
      ) : (
        !loading && (
          <p className="text-gray-500 text-center mt-4">
            No recent recordings available.
          </p>
        )
      )}
    </div>
  );
};

export default LatestRecordings;

import type React from "react";
import { useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { fetchLatestRecordings } from "../slice/latestRecordings"; // Import the async thunk
import type { RootState } from "../store";
import type { AppDispatch } from "../store";

const LatestRecordings: React.FC = () => {
  const dispatch: AppDispatch = useDispatch();

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
    // Dispatch fetchLatestRecordings when the component mounts
    console.log("Dispatching fetchLatestRecordings...");
    dispatch(fetchLatestRecordings());
  }, [dispatch]);

  // Log state for debugging
  console.log("Recordings:", recordings);
  console.log("Loading status:", loading);
  console.log("Error (if any):", error);

  return (
    <div className="recordings-list h-full p-6 bg-white shadow-lg overflow-y-auto  w-full max-w-md">
      <h2 className="text-2xl font-semibold mb-4 text-gray-800 border-b pb-2">
        Recent Recordings
      </h2>

      {loading && <p className="text-gray-500 text-center mt-4">Loading...</p>}

      {error && <p className="text-red-500 text-center mt-4">{error}</p>}

      {recordings.length > 0 ? (
        <ul className="space-y-4">
          {recordings.map((recording) => (
            <li
              key={recording.id}
              className="bg-gray-100 rounded p-4 shadow-md"
            >
              <audio
                controls
                className="w-full mt-2"
                onPlay={() => console.log("Audio started playing")}
                onPause={() => console.log("Audio paused")}
                onError={handleError}
              >
                <source src={recording.url} type="audio/mp3" />
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

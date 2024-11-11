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
    <div className="recordings-list">
      <h2>Latest Recordings</h2>
      {loading && <p>Loading...</p>}
      {error && <p>{error}</p>}
      {recordings.length > 0 ? (
        <ul>
          {recordings.map((recording) => (
            <li key={recording.id}>
              <audio
                controls
                onPlay={() => console.log("Audio started playing")}
                onPause={() => console.log("Audio paused")}
                onError={handleError}
              >
                <source src={recording.url} type="audio/mp3" />
                Your browser does not support the audio element.
                {/* Optional: Add captions if you have a captions file */}
                <track
                  src={"http://localhost:8000/captions.vtt"}
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
        !loading && <p>No recent recordings available.</p>
      )}
    </div>
  );
};

export default LatestRecordings;

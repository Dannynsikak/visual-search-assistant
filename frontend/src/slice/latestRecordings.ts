import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";

// Define the structure of a Recording
export interface Recording {
  id: string; // Unique identifier for the recording
  url: string; // The URL of the audio file for playback
}

// Define the structure of the Recordings state
export interface RecordingsState {
  recordings: Recording[]; // List of recordings
  loading: boolean; // Loading state
  error: string | null; // Error message, if any
}

const initialState: RecordingsState = {
  recordings: [],
  loading: false,
  error: null,
};

// Fetch MP3 recordings from the server (assuming the response contains URLs of MP3 files)
export const fetchLatestRecordings = createAsyncThunk(
  "recordings/fetchLatestRecordings",
  async () => {
    const response = await fetch("http://localhost:8000/first-six-recordings");

    // Handle non-OK responses
    if (!response.ok) {
      throw new Error(`Failed to fetch recordings: ${response.statusText}`);
    }

    // Assuming the response contains an array of URLs for the MP3 files
    const recordingsArray = await response.json();

    // Map through each recording URL and generate an object with id and URL
    const recordings = recordingsArray.map(
      (recordingUrl: string, index: number) => {
        return {
          id: String(index), // Generate a unique ID based on the index
          url: recordingUrl, // Use the URL directly (no need for Blob conversion)
        };
      }
    );

    return recordings; // Return the list of recordings
  }
);

const recordingSlice = createSlice({
  name: "recordings",
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchLatestRecordings.pending, (state) => {
        // Set loading state to true when fetching starts
        state.loading = true;
        state.error = null; // Clear previous error
      })
      .addCase(fetchLatestRecordings.fulfilled, (state, action) => {
        // On successful fetch, update state with the recordings
        state.loading = false;
        state.recordings = action.payload;
      })
      .addCase(fetchLatestRecordings.rejected, (state, action) => {
        // On failure, set loading to false and store the error message
        state.loading = false;
        state.error = action.error.message || "Failed to fetch recordings";
      });
  },
});

export default recordingSlice.reducer;

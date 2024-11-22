// src/slice/waveformSlice.ts
import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import axios from "axios";

// Define the initial state for the waveform
interface WaveformState {
  waveform: string | null;
  loading: boolean;
  error: string | null;
}

// Initial state
const initialState: WaveformState = {
  waveform: null,
  loading: false,
  error: null,
};
type FetchError = {
  message: string;
};
// Create an async thunk for fetching the waveform image
export const fetchWaveform = createAsyncThunk(
  "waveform/fetchWaveform",
  async (_, { rejectWithValue }) => {
    try {
      // Make the GET request to fetch the waveform
      const response = await axios.get("http://localhost:8000/get-waveform", {
        responseType: "blob",
      });

      // Create a URL for the image blob
      const imageURL = URL.createObjectURL(response.data);
      return imageURL;
    } catch (error) {
      const err = error as FetchError;
      return rejectWithValue(err.message || "Failed to fetch audio.");
    }
  }
);
const waveformSlice = createSlice({
  name: "waveform",
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchWaveform.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchWaveform.fulfilled, (state, action) => {
        state.loading = false;
        state.waveform = action.payload;
      })
      .addCase(fetchWaveform.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      });
  },
});
export default waveformSlice.reducer;

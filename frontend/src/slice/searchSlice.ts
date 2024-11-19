import {
  createSlice,
  createAsyncThunk,
  type PayloadAction,
} from "@reduxjs/toolkit";

interface SearchState {
  descriptionMode: string;
  description: string;
  audio_paths: string;
  error: string;
  loading: boolean;
  uploadProgress: number;
}

const initialState: SearchState = {
  descriptionMode: "summary",
  description: "",
  audio_paths: "",
  error: "",
  loading: false,
  uploadProgress: 0,
};

type FetchError = {
  message: string;
};

// Async thunk to fetch audio path
export const fetchAudioPath = createAsyncThunk(
  "search/fetchAudioPath",
  async (_, { rejectWithValue }) => {
    try {
      const response = await fetch("http://localhost:8000/output_path");
      if (!response.ok) {
        throw new Error(`Failed to fetch audio: ${response.statusText}`);
      }
      const data = await response.json();
      return data.audio_path; // Assuming backend returns { audio_path: string }
    } catch (error) {
      const err = error as FetchError;
      return rejectWithValue(err.message || "Failed to fetch audio.");
    }
  }
);

const searchSlice = createSlice({
  name: "search",
  initialState,
  reducers: {
    setDescriptionMode(state, action: PayloadAction<string>) {
      state.descriptionMode = action.payload;
    },
    setDescription(state, action: PayloadAction<string>) {
      state.description = action.payload;
    },
    setAudioPath(state, action: PayloadAction<string>) {
      state.audio_paths = action.payload;
    },
    setError(state, action: PayloadAction<string>) {
      state.error = action.payload;
    },
    setLoading(state, action: PayloadAction<boolean>) {
      state.loading = action.payload;
    },
    setUploadProgress(state, action: PayloadAction<number>) {
      state.uploadProgress = action.payload;
    },
    resetState() {
      return initialState;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchAudioPath.pending, (state) => {
        state.loading = true;
        state.error = "";
      })
      .addCase(fetchAudioPath.fulfilled, (state, action) => {
        state.loading = false;
        state.audio_paths = action.payload;
      })
      .addCase(fetchAudioPath.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      });
  },
});

export const {
  setDescriptionMode,
  setDescription,
  setAudioPath,
  setError,
  setLoading,
  setUploadProgress,
  resetState,
} = searchSlice.actions;

export default searchSlice.reducer;

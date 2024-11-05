import { createSlice, type PayloadAction } from "@reduxjs/toolkit";

interface SearchState {
  descriptionMode: string;
  description: string;
  audioPath: string;
  error: string;
  loading: boolean;
  uploadProgress: number;
}

const initialState: SearchState = {
  descriptionMode: "summary",
  description: "",
  audioPath: "",
  error: "",
  loading: false,
  uploadProgress: 0,
};

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
      state.audioPath = action.payload;
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

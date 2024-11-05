import { useDispatch, useSelector } from "react-redux";
import { switchMode } from "../store";
import { useEffect } from "react";
import type { RootState } from "../store";
import { FaSun, FaMoon } from "react-icons/fa";

export const ToggleButton = () => {
  const dispatch = useDispatch();
  const currentMode = useSelector((state: RootState) => state.mode.mode); // Get the current mode from the Redux store

  useEffect(() => {
    document.body.classList.remove("light-theme", "dark-theme");
    document.body.classList.add(`${currentMode}-theme`);
  }, [currentMode]);

  // Function to toggle mode
  const toggleMode = () => {
    dispatch(switchMode());
  };

  return (
    <button
      type="button"
      onClick={toggleMode}
      className={`px-4 py-2 rounded-md transition-colors duration-300 float-right   ${
        currentMode === "light"
          ? "bg-gray-800 text-white hover:bg-gray-900"
          : "bg-white text-gray-600 hover:bg-gray-700"
      }`}
    >
      {currentMode === "light" ? <FaSun /> : <FaMoon />}
    </button>
  );
};

import type React from "react";
import { useState } from "react";
import { FiEye } from "react-icons/fi"; // Import the icon you want to use
import LatestRecordings from "./LatestRecordings"; // Adjust the path as needed

const ToggleModal: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleModal = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div>
      <FiEye
        onClick={toggleModal}
        className="text-blue-500 text-3xl cursor-pointer hover:text-blue-700"
      />

      {isOpen && (
        <div className="fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-75 z-50">
          <div className="bg-white p-6 rounded shadow-lg max-w-lg w-full relative">
            <button
              type="button"
              onClick={toggleModal}
              className="absolute top-2 right-2 text-gray-500 hover:text-gray-700"
            >
              &times;
            </button>
            {/* Render the RecordingComponent inside the modal */}
            <LatestRecordings />
          </div>
        </div>
      )}
    </div>
  );
};

export default ToggleModal;

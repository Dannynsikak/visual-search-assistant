import type React from "react";
import { useState } from "react";
import { TbHistoryToggle } from "react-icons/tb";
import LatestRecordings from "./LatestRecordings"; // Adjust the path as needed

const ToggleModal: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleModal = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div>
      <TbHistoryToggle
        onClick={toggleModal}
        className="text-3xl cursor-pointer hover:text-gray-500"
      />

      {isOpen && (
        <div className="fixed inset-y-0 left-0 flex items-start bg-gray-800 bg-opacity-75 z-50">
          <div className="bg-white p-6  rounded-br-lg shadow-lg h-full w-full max-w-md relative">
            <button
              type="button"
              onClick={toggleModal}
              className="absolute top-2 right-2 text-gray-500 hover:text-gray-700 text-[2.5rem]"
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

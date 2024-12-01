"use client"

import React from 'react';

function App() {
  // Sample JSON data
  const jsonData1 = {
    names: ["John", "Alice", "Bob", "Emma", "Michael", "Sarah", "David", "Lisa"]
  };

  const jsonData2 = {
    names: ["James", "Sophie", "Daniel", "Olivia", "William", "Emily", "Alex", "Mia"]
  };

  const [currentJson, setCurrentJson] = React.useState(1);
  const [selectedNames, setSelectedNames] = React.useState([]);
  const [currentData, setCurrentData] = React.useState(jsonData1);

  const handleNameSelect = (name) => {
    if (selectedNames.includes(name)) {
      setSelectedNames(selectedNames.filter(n => n !== name));
    } else if (selectedNames.length < 4) {
      setSelectedNames([...selectedNames, name]);
    }
  };

  const handleNext = () => {
    if (currentJson === 1) {
      setCurrentJson(2);
      setCurrentData(jsonData2);
    }
  };

  const isNameSelected = (name) => selectedNames.includes(name);

  return (
    <div className="p-6 max-w-2xl mx-auto">
      <div className="mb-6">
        <h2 className="text-xl font-bold mb-4">
          Selected Names ({selectedNames.length}/4)
        </h2>
        <div className="flex flex-wrap gap-2 mb-4">
          {selectedNames.map((name, index) => (
            <div 
              key={index}
              className="bg-blue-100 px-3 py-1 rounded-full"
            >
              {name}
            </div>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4 mb-6">
        {currentData.names.map((name, index) => (
          <button
            key={index}
            onClick={() => handleNameSelect(name)}
            className={`p-2 rounded ${
              isNameSelected(name)
                ? 'bg-blue-500 text-white'
                : 'bg-gray-100 hover:bg-gray-200'
            } ${
              selectedNames.length >= 4 && !isNameSelected(name)
                ? 'opacity-50 cursor-not-allowed'
                : ''
            }`}
            disabled={selectedNames.length >= 4 && !isNameSelected(name)}
          >
            {name}
          </button>
        ))}
      </div>

      {selectedNames.length >= 4 ? (
        <button
          onClick={() => console.log('Saving:', selectedNames)}
          className="w-full bg-green-500 text-white py-2 rounded hover:bg-green-600"
        >
          Save
        </button>
      ) : (
        currentJson === 1 && (
          <button
            onClick={handleNext}
            className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600"
          >
            Next
          </button>
        )
      )}
    </div>
  );
}

export default App;
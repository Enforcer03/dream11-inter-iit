"use client";

import React, { useState } from "react";

function AudioComponent() {
  const [clicked, setClicked] = useState(false);

  const handleClick = () => {
    setClicked((prevState) => !prevState);
  };

  return (
    <button
      className={`audioComp ${clicked ? "audioCompClicked" : ""}`}
      onClick={handleClick}
    >
    </button>
  );
}

export default AudioComponent;

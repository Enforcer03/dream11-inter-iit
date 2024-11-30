"use client";

import { useEffect, useState } from "react";

export default function MatchSelector({ setMatch, allMatches }: { setMatch: (match: any) => void; allMatches: any[] }) {
  const [selectedIndex, setSelectedIndex] = useState(0);

  const handlePrevious = () => {
    const newIndex = (selectedIndex - 1 + allMatches.length) % allMatches.length;
    setSelectedIndex(newIndex);
    setMatch(allMatches[newIndex]);
  };

  const handleNext = () => {
    const newIndex = (selectedIndex + 1) % allMatches.length;
    setSelectedIndex(newIndex);
    setMatch(allMatches[newIndex]);
  };

  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === "ArrowLeft") {
        handlePrevious();
      } else if (event.key === "ArrowRight") {
        handleNext();
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  return (
    <div className="flex flex-col items-center justify-center mt-8">
      <h1 className="text-3xl font-bold mb-16 text-[#FFD700]">SELECT MATCH</h1>
      <div className="w-full px-4 relative">
        <div className="flex justify-center items-center mb-8">
          {allMatches?.map((match, index) => {
            const distance = Math.abs(selectedIndex - index);
            const isVisible = distance <= 2;
            return (
              <div
                key={index}
                className={`absolute transition-all duration-300 ${
                  isVisible ? "opacity-100" : "opacity-0 pointer-events-none"
                }`}
                style={{
                  transform: `translateX(${(index - selectedIndex) * 120}px) scale(${1 - distance * 0.2})`,
                  zIndex: allMatches.length - distance,
                }}
              >
                <button
                  className={`w-48 h-20 relative rounded-lg overflow-hidden border-2 transition-all duration-300 focus:outline-none ${
                    selectedIndex === index ? "border-white" : "border-transparent hover:border-white/50"
                  }`}
                  onClick={() => setSelectedIndex(index)}
                >
                  <div className="flex">
                    <div>
                      {match.split("_")[0]}
                      <img src={match.logo} />
                    </div>
                    <div>{match.split("_")[3]}</div>
                    <div>
                      {match.split("_")[2]}
                      <img src={match.logo} />
                    </div>
                  </div>
                </button>
              </div>
            );
          })}
        </div>
        <button
          onClick={handlePrevious}
          className="leftArrowBtn absolute left-0 top-1/2 transform -translate-y-1/2 p-2"
          aria-label="Previous team"
        />
        <button
          onClick={handleNext}
          className="rightArrowBtn absolute right-0 top-1/2 transform -translate-y-1/2 p-2"
          aria-label="Next team"
        />
      </div>
    </div>
  );
}

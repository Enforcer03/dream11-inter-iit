"use client";

import { useEffect, useState } from "react";
import { SquadApiResponse } from "../types/squadApiResponse";

export default function LeagueSelector({
  setLeague,
  allLeagues,
  setAllMatches,
  allData,
}: {
  setLeague: (league: string) => void;
  allLeagues: string[];
  setAllMatches: (matches: string[]) => void;
  allData: SquadApiResponse | null;
}) {
  const [selectedIndex, setSelectedIndex] = useState(0);

  const handlePrevious = () => {
    if (!allData) return;

    const newIndex = (selectedIndex - 1 + allLeagues.length) % allLeagues.length;
    setSelectedIndex(newIndex);
    setLeague(allLeagues[newIndex]);
    setAllMatches(Object.keys(allData[allLeagues[newIndex]]));
  };

  const handleNext = () => {
    if (!allData) return;

    const newIndex = (selectedIndex + 1) % allLeagues.length;
    setSelectedIndex(newIndex);
    setLeague(allLeagues[newIndex]);
    setAllMatches(Object.keys(allData[allLeagues[newIndex]]));
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
      <h1 className="text-3xl font-bold mb-16 text-[#FFD700]">SELECT LEAGUE</h1>
      <div className="w-full px-4 relative">
        <div className="flex justify-center items-center mb-8">
          {allLeagues ? (
            allLeagues.map((league, index) => {
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
                    zIndex: league.length - distance,
                  }}
                >
                  <button
                    className={`w-32 h-16 relative rounded-lg overflow-hidden border-2 transition-all duration-300 focus:outline-none ${
                      selectedIndex === index ? "border-white" : "border-transparent hover:border-white/50"
                    }`}
                    onClick={() => setSelectedIndex(index)}
                  >
                    <span>{league}</span>
                    <img src={league.logo} alt={league.name} className="object-cover" />
                  </button>
                </div>
              );
            })
          ) : (
            <div>Please select date first</div>
          )}
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

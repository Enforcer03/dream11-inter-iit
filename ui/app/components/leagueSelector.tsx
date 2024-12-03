"use client";

import { useEffect, useState } from "react";
import { SquadApiResponse } from "../types/squadApiResponse";

export default function LeagueSelector({
  setLeague,
  allLeagues,
  setAllMatches,
  allData,
  dateLength,
}: {
  setLeague: (league: string) => void;
  allLeagues: string[];
  setAllMatches: (matches: string[]) => void;
  allData: SquadApiResponse | null;
  dateLength: number;
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

  function handleDirectClick(index: number) {
    if (!allData) return;

    setSelectedIndex(index);
    setLeague(allLeagues[index]);
    setAllMatches(Object.keys(allData[allLeagues[index]]));
  }

  const shortenWord = (word) => {
    if (word.length > 15) {
      return word.slice(0, 14) + "...";
    }
    return word;
  };

  const shortenLeague = (league) => {
    const words = league.split(" ");
    const shortenedWords = words.map(shortenWord);

    let shortenedLeague = shortenedWords.join(" ");
    if (shortenedLeague.length > 35) {
      shortenedLeague = shortenedLeague.slice(0, 35) + "...";
    }

    return shortenedLeague;
  };

  return (
    <div className="flex flex-col items-center justify-center mt-14">
      <h1 className="text-3xl font-bold mb-16 text-[#FFD700]">SELECT LEAGUE</h1>
      <div className="w-full relative">
        <div className="flex justify-center items-center mb-8">
          {allLeagues.length && dateLength == 10 ? (
            allLeagues.map((league, index) => {
              const distance = Math.abs(selectedIndex - index);
              const isVisible = distance <= 2;
              return (
                <div
                  key={index}
                  className={`flex justify-center items-center mb-8 mt-8 absolute transition-all duration-300 ${
                    isVisible ? "opacity-100" : "opacity-0 pointer-events-none"
                  }`}
                  style={{
                    transform: `translateX(${(index - selectedIndex) * 200}px) scale(${1 - distance * 0.14})`,
                    zIndex: league.length - distance,
                  }}
                >
                  <button
                    className={`w-40 h-20 filledLeague relative overflow-hidden transition-all duration-300 ${
                      selectedIndex === index ? "" : "border-2 border-transparent hover:border-white/50"
                    }`}
                    onClick={() => handleDirectClick(index)}
                  >
                    <span className="text-yellow-100 relative z-10 text-white uppercase p-1">
                      {shortenLeague(league)}
                    </span>
                  </button>
                </div>
              );
            })
          ) : (
            <div>
              {dateLength === 10 ? (
                <div className="emptyText">NO LEAGUES FOUND</div>
              ) : (
                <div className="flex justify-center items-center mb-8">
                  {Array(3)
                    .fill()
                    .map((_, index) => {
                      const distance = Math.abs(selectedIndex + index);
                      const isVisible = distance <= 2;
                      return (
                        <div
                          key={index}
                          className={`absolute`}
                          style={{
                            transform: `translateX(${index * -200}px) scale(${1 - distance * 0.14})`,
                          }}
                        >
                          <div className={`w-40 h-20 emptyLeague`} />
                        </div>
                      );
                    })}
                  {Array(3)
                    .fill()
                    .map((_, index) => {
                      const distance = Math.abs(selectedIndex + index);
                      const isVisible = distance <= 2;
                      return (
                        <div
                          key={index}
                          className={`absolute`}
                          style={{
                            transform: `translateX(${index * 200}px) scale(${1 - distance * 0.14})`,
                          }}
                        >
                          <div className={`w-40 h-20 emptyLeague`} />
                        </div>
                      );
                    })}
                </div>
              )}
            </div>
          )}
        </div>
        <button
          onClick={handlePrevious}
          className={`leftArrowBtn -mt-4 -ml-24 absolute left-0 top-1/2 transform -translate-y-1/2 p-2 ${
            allLeagues.length != 0 && dateLength == 10 ? "" : "hidden"
          }`}
          aria-label="Previous team"
        />
        <button
          onClick={handleNext}
          className={`rightArrowBtn -mt-4 -mr-24 absolute right-0 top-1/2 transform -translate-y-1/2 p-2 ${
            allLeagues.length != 0 && dateLength == 10 ? "" : "hidden"
          }`}
          aria-label="Next team"
        />
      </div>
    </div>
  );
}

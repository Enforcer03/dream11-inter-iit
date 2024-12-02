"use client";

import { useState } from "react";
import { MatchDetails, SquadApiResponse } from "../types/squadApiResponse";

type MatchSelectorProps = {
  setMatchData: (matchData: MatchDetails) => void;
  allMatches: string[];
  allData: SquadApiResponse | null;
  league: string;
  date: string;
};

export default function MatchSelector({ setMatchData, allMatches, allData, league, date }: MatchSelectorProps) {
  const [selectedIndex, setSelectedIndex] = useState(0);

  function handlePrevious() {
    if (!allData) return;
    const newIndex = (selectedIndex - 1 + allMatches.length) % allMatches.length;
    setSelectedIndex(newIndex);
    setMatchData(allData[league][allMatches[newIndex]]);
  }

  function handleNext() {
    if (!allData) return;
    const newIndex = (selectedIndex + 1) % allMatches.length;
    setSelectedIndex(newIndex);
    setMatchData(allData[league][allMatches[newIndex]]);
  }

  function handleDirectClick(index: number) {
    if (!allData) return;

    setSelectedIndex(index);
    setMatchData(allData[league][allMatches[index]]);
  }

  const formatText = (word: String) => {
    const maxLength = 15;
    const chunkSize = 5;
    let chunks = [];

    for (let i = 0; i < word.length; i += chunkSize) {
      chunks.push(word.slice(i, i + chunkSize));
    }

    const result = chunks.join('');
    if (result.length > maxLength) {
      return formatText(result.slice(0, 13)) + '...';
    }

    return chunks.join(' ');
  };

  const formatLocation = (word: String) => {
    const maxLength = 22;
    if (word.length > maxLength) {
      return (word.slice(0, 22)) + '..';
    }

    return word;
  };

  const convertToDay = (dateString: string) => {
    const [day, month, year] = dateString.split("/");
    const date = new Date(year, month - 1, day);
    const daysOfWeek = [
      "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"
    ];
    const dayName = daysOfWeek[date.getDay()];

    return dayName;
  };

  return (
    <div className="flex flex-col items-center justify-center">
      <h1
        className={`text-3xl font-bold mb-16 text-[#FFD700] ${
          allMatches.length != 0 && date.length == 10 ? "mt-8" : ""
        }`}
      >
        SELECT MATCH
      </h1>
      <div className="w-full relative">
        <div className="flex justify-center items-center">
          {allMatches.length && date.length == 10 ? (
            allMatches?.map((match, index) => {
              const distance = Math.abs(selectedIndex - index);
              const isVisible = distance <= 2;

              const matchParts = match.split("_");
              const team1 = matchParts[0];
              const team2 = matchParts[2];
              const location = matchParts.slice(3).join(" ");
              return (
                <div
                  key={index}
                  className={`flex justify-center items-center mb-8 mt-8 absolute transition-all duration-300 ${
                    isVisible ? "opacity-100" : "opacity-0 pointer-events-none"
                  }`}
                  style={{
                    transform: `translateX(${(index - selectedIndex) * 325}px) scale(${1 - distance * 0.14})`,
                    zIndex: league.length - distance,
                  }}
                >
                  <button
                    className={`w-80 h-20 filledMatch relative overflow-hidden transition-all duration-300 ${
                      selectedIndex === index ? "" : "border-2 border-transparent hover:border-white/50"
                    }`}
                    onClick={() => handleDirectClick(index)}
                  >
                    <div className="flex text-yellow-100 relative z-10 text-white uppercase text-sm">
                      <span className="w-[3.6rem] m-0.5 flex justify-center items-center">{formatText(team1)}</span>
                      <div className="">
                        <span className="w-48 h-8 text-2xl font-bold m-0.5">{convertToDay(date)}</span>
                        <span className="w-48 h-9 m-0.5 flex flex-col justify-end">{formatLocation(location)}</span>
                      </div>
                      <span className="w-[3.6rem] m-0.5 flex justify-center items-center">{formatText(team2)}</span>
                    </div>
                  </button>
                </div>
              );
            })
          ) : (
            <div>
              {date.length === 10 ? (
                <div className="emptyText">NO MATCHES FOUND</div>
              ) : (
                <div className="flex justify-center items-center mb-8">
                  {Array(2)
                    .fill()
                    .map((_, index) => {
                      const distance = Math.abs(selectedIndex + index);
                      const isVisible = distance <= 1;
                      return (
                        <div
                          key={index}
                          className={`absolute`}
                          style={{
                            transform: `translateX(${index * -325}px) scale(${1 - distance * 0.14})`,
                          }}
                        >
                          <div className={`w-80 h-20 emptyMatch`} />
                        </div>
                      );
                    })}
                  {Array(2)
                    .fill()
                    .map((_, index) => {
                      const distance = Math.abs(selectedIndex + index);
                      const isVisible = distance <= 1;
                      return (
                        <div
                          key={index}
                          className={`absolute`}
                          style={{
                            transform: `translateX(${index * 325}px) scale(${1 - distance * 0.14})`,
                          }}
                        >
                          <div className={`w-80 h-20 emptyMatch`} />
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
          className={`leftArrowBtn -ml-24 top-1/2 transform -translate-y-1/2 p-2 ${
            allMatches.length != 0 && date.length == 10 ? "" : "hidden"
          }`}
          aria-label="Previous team"
        />
        <button
          onClick={handleNext}
          className={`rightArrowBtn -mr-24 top-1/2 transform -translate-y-1/2 p-2 ${
            allMatches.length != 0 && date.length == 10 ? "" : "hidden"
          }`}
          aria-label="Next team"
        />
      </div>
    </div>
  );
}

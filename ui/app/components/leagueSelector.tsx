"use client";

import { useState, useEffect } from "react";

export default function LeagueSelector({ setLeague }: { setLeague: (league: any) => void }) {
  const [selectedIndex, setSelectedIndex] = useState(3);

  const teams = [
    {
      name: "Kolkata Knight Riders",
      logo: "/placeholder.svg?height=200&width=200",
    },
    {
      name: "Sunrisers Hyderabad",
      logo: "/placeholder.svg?height=200&width=200",
    },
    {
      name: "Mumbai Indians",
      logo: "/placeholder.svg?height=200&width=200",
    },
    {
      name: "Chennai Super Kings",
      logo: "/placeholder.svg?height=200&width=200",
    },
    {
      name: "Mumbai Indians",
      logo: "/placeholder.svg?height=200&width=200",
    },
    {
      name: "Sunrisers Hyderabad",
      logo: "/placeholder.svg?height=200&width=200",
    },
    {
      name: "Kolkata Knight Riders",
      logo: "/placeholder.svg?height=200&width=200",
    },
  ];

  const handlePrevious = () => {
    const newIndex = (selectedIndex - 1 + teams.length) % teams.length;
    setSelectedIndex(newIndex);
    setLeague(teams[newIndex]);
  };

  const handleNext = () => {
    const newIndex = (selectedIndex + 1) % teams.length;
    setSelectedIndex(newIndex);
    setLeague(teams[newIndex]);
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
          {teams.map((team, index) => {
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
                  zIndex: teams.length - distance,
                }}
              >
                <button
                  className={`w-32 h-16 relative rounded-lg overflow-hidden border-2 transition-all duration-300 focus:outline-none ${
                    selectedIndex === index ? "border-white" : "border-transparent hover:border-white/50"
                  }`}
                  onClick={() => setSelectedIndex(index)}
                >
                  <img src={team.logo} alt={team.name} className="object-cover" />
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

"use client";

import React, { useEffect, useState } from "react";
import ButtonComponent from "../components/selectedPlayer";
import playersData from "../../public/players.json";

interface Instruction {
    id: number;
    text: string;
  }

const PeopleDisplay = () => {
    const [selectedPlayers, setSelectedPlayers] = useState(playersData.players.slice(0, 11));
    const [instructions, setInstructions] = useState<Instruction[]>([]);

    useEffect(() => {
        const fetchInstructions = async () => {
          try {
            const response = await fetch("/instructions.txt");
            if (!response.ok) {
              throw new Error("Failed to load instructions");
            }

            const text = await response.text();
            const instructionsList = text.split("\n").map((line, index) => ({
              id: index + 1,
              text: line.trim(),
            }));

            setInstructions(instructionsList);
          } catch (error) {
            console.error("There was an error fetching the instructions.");
          }
        };

        fetchInstructions();
      }, []);

  return (
    <div>
        <div className="-mb-6 ml-11">
            <h1 className="text-xl font-bold text-[#FFD700] ">PLAYERS' INFORMATION REPORT</h1>
        </div>
        <div className="flex m-16">
        {selectedPlayers.map((player) => (
            <div
                key={player.id}
                className="m-4"
            >
                <ButtonComponent
                  child1={<img src={player.image} alt="Player Image" className="" />}
                  child2={player.name.split(" ").map(word => word.charAt(0).toUpperCase()).join("")}
                />
            </div>
         ))}
        </div>
        <div className="instructions-container">
      <ul>
        {instructions.map((instruction) => (
          <li key={instruction.id}>{instruction.text}</li>
        ))}
      </ul>
    </div>
    </div>
  );
};

export default PeopleDisplay;

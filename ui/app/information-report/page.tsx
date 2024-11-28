"use client";

import React, { useEffect, useState } from "react";
import SelectedPlayer from "../components/selectedPlayer";
import playersData from "../../public/players.json";
import PageTemplate from "../components/pageTemplate"
import Button from "../components/buttonComp"

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
      <PageTemplate title="playing 11">
      <div className="-mb-6 ml-11">
        <h1 className="text-2xl text-[#FFD700] ">PLAYERS' INFORMATION REPORT</h1>
      </div>
      <div className="flex m-12">
        {selectedPlayers.map((player) => {
          let fullName = player.name.split(" ");
          let modifiedName = fullName.map((part) => {
            return part.length > 7 ? part[0] + "." : part;
          }).join(" ");

          return (
            <div key={player.id} className="m-2">
              <SelectedPlayer
                child1={<img src={player.image} alt="Player Image" className="player-image" />}
                child2={modifiedName}
              />
            </div>
          );
        })}
      </div>
      <div className="information-report-container">
        <ul>
          {instructions.map((instruction) => (
            <li key={instruction.id}>{instruction.text}</li>
          ))}
        </ul>
      </div>
      </PageTemplate>
      <div className="buttonCompDiv">
        <Button>BACK</Button>
        <Button>NEXT</Button>
      </div>
    </div>
  );
};

export default PeopleDisplay;

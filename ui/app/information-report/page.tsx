"use client";

import React, { useEffect, useState } from "react";
import InfoReportPlayer from "../components/infoReportPlayer";
import PageTemplate from "../components/pageTemplate";
import Button from "../components/buttonComp";
import { useMatchData } from "../contexts/matchDataContext";

interface Instruction {
  id: number;
  text: string;
}

  interface PlayerData {
    id: number;
    name: string;
    image: string;
  }

  function getPlayerImagePath(
    playerName: string,
    selectedPlayersTeamA: PlayerData[],
    selectedPlayersTeamB: PlayerData[]
  ): string {
    const nameParts = playerName.split(" ");
    const lastName = nameParts[nameParts.length - 1];
    const firstInitial = nameParts[0][0];
    const allPlayers = [...selectedPlayersTeamA, ...selectedPlayersTeamB];

    let matchingPlayer = allPlayers.find((player) => {
      const playerNameParts = player.name.split(" ");
      const playerLastName = playerNameParts[playerNameParts.length - 1];
      const playerFirstInitial = player.name[0];

      return playerLastName === lastName && playerFirstInitial === firstInitial;
    });

    if (!matchingPlayer) {
      matchingPlayer = allPlayers.find((player) => {
        const playerNameParts = player.name.split(" ");
        const playerLastName = playerNameParts[playerNameParts.length - 1];
        return playerLastName === lastName;
      });
    }

    return matchingPlayer ? matchingPlayer.image : "default_player_image_url";
  }

const PeopleDisplay = () => {
    const {
      predictedTeam,
      setPredictedTeam,
      selectedPlayersTeamA,
      selectedPlayersTeamB,
    } = useMatchData();

    console.log(predictedTeam);

  const [selectedPlayers, setSelectedPlayers] = useState(predictedTeam.slice(0, 11));
  const [instructions, setInstructions] = useState<Instruction[]>([]);

  const prevPage = "/playing11";

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
        <div className=" ml-2 -mt-20">
          <h1 className="text-3xl text-[#FFD700] font-bold tracking-wider">PLAYERS' INFORMATION REPORT</h1>
        </div>
        <div className="flex m-4">
          {selectedPlayers.map((player, index) => {
            let fullName = player.split(" ");
            let modifiedName = fullName
              .map((part) => {
                return part.length > 7 ? part[0] + "." : part;
              })
              .join(" ");

            return (
              <div key={index} className="m-3">
                <InfoReportPlayer
                  child1={
                    <img
                      src={getPlayerImagePath(player, selectedPlayersTeamA, selectedPlayersTeamB)}
                      alt="Player Image"
                      className="player-image"
                    />
                  }
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
        <Button nextPage={prevPage}>BACK</Button>
        <Button downloadScreenshot={true}>SAVE</Button>
      </div>
    </div>
  );
};

export default PeopleDisplay;

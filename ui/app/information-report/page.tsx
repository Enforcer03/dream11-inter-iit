"use client";

import Image from "next/image";
import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import { handleLLMTeam } from "../api/llmApi";
import Button from "../components/buttonComp";
import InfoReportPlayer from "../components/infoReportPlayer";
import PageTemplate from "../components/pageTemplate";
import { useMatchData } from "../contexts/matchDataContext";
import { areStringArraysEqualIgnoreOrder } from "../utils/TeamCompare";

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
  const { predictedTeam, selectedPlayersTeamA, selectedPlayersTeamB, instructionLLM, playerStats, setInstructionLLM } =
    useMatchData();

  const [isLoading, setIsLoading] = useState(false);
  const prevPage = "/playing11";

  useEffect(() => {
    async function checkLoading() {
      if (areStringArraysEqualIgnoreOrder(predictedTeam, instructionLLM.team)) {
        if (instructionLLM.instruction === "") setIsLoading(true);
        else setIsLoading(false);
      } else {
        setIsLoading(true);
        const response = await handleLLMTeam(predictedTeam, JSON.stringify(playerStats), "T20");

        setInstructionLLM({ team: predictedTeam, instruction: response["team analysis"] });
        setIsLoading(false);
      }
    }

    checkLoading();
  }, [instructionLLM, predictedTeam, playerStats, setInstructionLLM]);

  return (
    <div>
      <PageTemplate title="playing 11">
        <div className=" ml-2 -mt-20">
          <h1 className="text-3xl text-[#FFD700] font-bold tracking-wider">PLAYERS&apos; INFORMATION REPORT</h1>
        </div>
        <div className="flex m-4">
          {predictedTeam.map((player, index) => {
            const fullName = player.split(" ");
            const modifiedName = fullName
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
        <div className="information-report-container overflow-y-scroll h-[25rem]">
          {isLoading ? (
            <div className="loader-container">
              <Image src="/loading.gif" alt="Loading..." width={100} height={100} priority />
            </div>
          ) : (
            <ReactMarkdown>{instructionLLM.instruction}</ReactMarkdown>
          )}
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

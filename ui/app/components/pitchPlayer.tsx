"use client";

import Image from "next/image";
import { RevaluateTeamApiResponse } from "../types/modelApiResponse";
import { MatchDetails } from "../types/squadApiResponse";
import PlayerOptions from "./playerOptions";

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

type PitchComponentProps = {
  selectedPlayer: number | null;
  setSelectedPlayer: (selectedPlayer: number | null) => void;
  predictedTeam: string[];
  setPredictedTeam: (predictedTeam: string[] | ((prev: string[]) => string[])) => void;
  matchData: MatchDetails | null;
  selectedPlayersTeamA: string[];
  selectedPlayersTeamB: string[];
  handleTeamRevaluation: (newPredictedTeam: string[], flag: boolean) => void;
  setNewTeamStats: (response: RevaluateTeamApiResponse) => void;
  setHoverPlayer: (hoverPlayer: string | null) => void;
};

type PlayerComponentProps = {
  player: string;
  selectedPlayer: number | null;
  setSelectedPlayer: (selectedPlayer: number) => void;
  index: number;
  selectedPlayersTeamA: PlayerData[];
  selectedPlayersTeamB: PlayerData[];
};

function PlayerComponent({
  player,
  selectedPlayer,
  setSelectedPlayer,
  index,
  selectedPlayersTeamA,
  selectedPlayersTeamB,
}: PlayerComponentProps) {
  return (
    <div className={`m-2 w-32 p-3 ${selectedPlayer === index ? "selected" : null}`}>
      <div
        onClick={() => setSelectedPlayer(index)}
        className={`flex w-full h-16 mb-24 flex-col items-center text-white`}
      >
        <Image
          src={getPlayerImagePath(player, selectedPlayersTeamA, selectedPlayersTeamB)}
          alt="player"
          width={200}
          height={200}
        />
        <p className="pitchPlayerText">
          <span className="bg-green-950 p-1.5">{index + 1}</span>
          <span className="bg-green-300 p-1.5 text-green-950 font-bold">{player.slice(0, 13)}</span>
        </p>
      </div>
    </div>
  );
}

export default function PitchComponent({
  selectedPlayer,
  setSelectedPlayer,
  predictedTeam,
  setPredictedTeam,
  selectedPlayersTeamA,
  selectedPlayersTeamB,
  handleTeamRevaluation,
  setNewTeamStats,
  setHoverPlayer,
}: PitchComponentProps) {

  
  return (
    <div className="w-[53rem] flex flex-col ml-[27rem] mb-12">
      <div className="w-full h-[35rem] pitch">
        <div className="flex flex-row justify-center">
          {predictedTeam.map((player, index) => {
            if (index < 5) {
              return (
                <PlayerComponent
                  key={index}
                  index={index}
                  player={player}
                  selectedPlayersTeamA={selectedPlayersTeamA}
                  selectedPlayersTeamB={selectedPlayersTeamB}
                  selectedPlayer={selectedPlayer}
                  setSelectedPlayer={setSelectedPlayer}
                />
              );
            }
          })}
        </div>
        <div className="flex flex-row justify-center">
          {predictedTeam.map((player, index) => {
            if (index >= 5 && index < 9) {
              return (
                <PlayerComponent
                  key={index}
                  index={index}
                  player={player}
                  selectedPlayersTeamA={selectedPlayersTeamA}
                  selectedPlayersTeamB={selectedPlayersTeamB}
                  selectedPlayer={selectedPlayer}
                  setSelectedPlayer={setSelectedPlayer}
                />
              );
            }
          })}
        </div>
        <div className="flex flex-row justify-center">
          {predictedTeam.map((player, index) => {
            if (index >= 9) {
              return (
                <PlayerComponent
                  key={index}
                  index={index}
                  player={player}
                  selectedPlayersTeamA={selectedPlayersTeamA}
                  selectedPlayersTeamB={selectedPlayersTeamB}
                  selectedPlayer={selectedPlayer}
                  setSelectedPlayer={setSelectedPlayer}
                />
              );
            }
          })}
        </div>
      </div>
      <PlayerOptions
        selectedPlayer={selectedPlayer}
        predictedTeam={predictedTeam}
        setPredictedTeam={setPredictedTeam}
        selectedPlayersTeamA={selectedPlayersTeamA}
        selectedPlayersTeamB={selectedPlayersTeamB}
        handleTeamRevaluation={handleTeamRevaluation}
        setNewTeamStats={setNewTeamStats}
        setHoverPlayer={setHoverPlayer}
      />
    </div>
  );
}

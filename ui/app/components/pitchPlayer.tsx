"use client";

import Image from "next/image";
import profilePhoto from "../../public/photo.png";
import { RevaluateTeamApiResponse } from "../types/modelApiResponse";
import { MatchDetails } from "../types/squadApiResponse";
import PlayerOptions from "./playerOptions";

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
};

type PlayerComponentProps = {
  player: string;
  selectedPlayer: number | null;
  setSelectedPlayer: (selectedPlayer: number) => void;
  index: number;
};

function PlayerComponent({ player, selectedPlayer, setSelectedPlayer, index }: PlayerComponentProps) {
  return (
    <div className={`m-2 w-40 p-3 ${selectedPlayer === index ? "selected" : null}`}>
      <div onClick={() => setSelectedPlayer(index)} className={`flex w-full flex-col items-center text-white `}>
        <Image src={profilePhoto} alt="player" width={200} height={200} />
        <p className="anonymousPlayerText">
          <span className="bg-green-950 p-2">{index + 1}</span>
          <span className="bg-green-300 p-2 text-green-950 font-bold">{player}</span>
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
}: PitchComponentProps) {
  return (
    <div className="w-[55.5rem] flex flex-col ml-[26rem] mb-12">
      <div className="w-full h-[35rem] pitch">
        <div className="flex flex-row">
          {predictedTeam.map((player, index) => {
            if (index < 5) {
              return (
                <PlayerComponent
                  key={index}
                  index={index}
                  player={player}
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
                  selectedPlayer={selectedPlayer}
                  setSelectedPlayer={setSelectedPlayer}
                />
              );
            }
          })}
        </div>
      </div>
      <PlayerOptions
        setHoveredPlayer={setHoveredPlayer}
        selectedPlayer={selectedPlayer}
        predictedTeam={predictedTeam}
        setPredictedTeam={setPredictedTeam}
        selectedPlayersTeamA={selectedPlayersTeamA}
        selectedPlayersTeamB={selectedPlayersTeamB}
        handleTeamRevaluation={handleTeamRevaluation}
        setNewTeamStats={setNewTeamStats}
      />
    </div>
  );
}

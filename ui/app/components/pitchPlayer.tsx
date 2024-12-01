"use client";

import Image from "next/image";
import profilePhoto from "../../public/photo.png";
import PlayerOptions from "./playerOptions";
import { MatchDetails } from "../types/squadApiResponse";

type PitchComponentProps = {
  selectedPlayer: number | null;
  setSelectedPlayer: (selectedPlayer: number | null) => void;
  setHoveredPlayer: (hoveredPlayer: number | null) => void;
  predictedTeam: string[];
  setPredictedTeam: (predictedTeam: string[] | ((prev: string[]) => string[])) => void;
  matchData: MatchDetails | null;
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
        {/* <img src={player.image} alt="player" /> */}
        <Image src={profilePhoto} alt="player" width={200} height={200} />
        <p>
          <span className="bg-green-950 p-2">{"010"}</span>
          <span className="bg-green-300 p-2 text-green-950 font-bold">{player}</span>
        </p>
      </div>
    </div>
  );
}

export default function PitchComponent({
  selectedPlayer,
  setSelectedPlayer,
  setHoveredPlayer,
  predictedTeam,
  setPredictedTeam,
  matchData,
}: PitchComponentProps) {
  return (
    <div className="w-[55.5rem] flex flex-col ml-[26rem] mb-12">
      <div className="w-full h-[35rem] pitch">
        {predictedTeam.map((player, index) => (
          <PlayerComponent
            key={index}
            index={index}
            player={player}
            selectedPlayer={selectedPlayer}
            setSelectedPlayer={setSelectedPlayer}
          />
        ))}
      </div>
      <PlayerOptions
        setHoveredPlayer={setHoveredPlayer}
        selectedPlayer={selectedPlayer}
        predictedTeam={predictedTeam}
        setPredictedTeam={setPredictedTeam}
        matchData={matchData}
      />
    </div>
  );
}

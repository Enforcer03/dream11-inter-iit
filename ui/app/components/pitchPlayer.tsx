"use client";

import Image from "next/image";
import profilePhoto from "../../public/photo.png";
import playerJsonTest from "../../public/playerJsonTest.json";
import PlayerOptions from "./playerOptions";

function PlayerComponent({ player, selectedPlayer, setSelectedPlayer }) {
  return (
    <div className={`m-2 w-40 p-3 ${selectedPlayer.playNumber === player.playNumber ? "selected" : null}`}>
      <div onClick={() => setSelectedPlayer(player)} className={`flex w-full flex-col items-center text-white `}>
        {/* <img src={player.image} alt="player" /> */}
        <Image src={profilePhoto} alt="player" width={200} height={200} />
        <p>
          <span className="bg-green-950 p-2">{player.playNumber}</span>
          <span className="bg-green-300 p-2 text-green-950 font-bold">{player.name}</span>
        </p>
      </div>
    </div>
  );
}

export default function PitchComponent({
  finalPlayers,
  setFinalPlayers,
  selectedPlayer,
  setSelectedPlayer,
  setHoveredPlayer,
}: {
  finalPlayers: number[];
  setFinalPlayers: (finalPlayers: number[]) => void;
  setSelectedPlayer: (selectedPlayer: number) => void;
  setHoveredPlayer: (hoveredPlayer: number) => void;
}) {
  return (
    <div className="w-[55.5rem] flex flex-col ml-[26rem] mb-12">
      <div className="w-full h-[35rem] pitch">
        <PlayerComponent
          player={playerJsonTest[finalPlayers[0]]}
          selectedPlayer={selectedPlayer}
          setSelectedPlayer={setSelectedPlayer}
        />

      </div>
      <PlayerOptions
        setFinalPlayers={setFinalPlayers}
        setHoveredPlayer={setHoveredPlayer}
        selectedPlayer={selectedPlayer}
        finalPlayers={finalPlayers}
      />
    </div>
  );
}

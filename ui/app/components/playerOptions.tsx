import Image from "next/image";
import profilePhoto from "../../public/photo.png";
import { MatchDetails } from "../types/squadApiResponse";

type PlayerOptionsProps = {
  setHoveredPlayer: (player: number | null) => void;
  selectedPlayer: number | null;
  predictedTeam: string[];
  setPredictedTeam: (predictedTeam: string[] | ((prev: string[]) => string[])) => void;
  matchData: MatchDetails;
};

type PlayerCardProps = {
  player: string;
  selectedPlayer: number | null;
  setPredictedTeam: (predictedTeam: string[] | ((prev: string[]) => string[])) => void;
  setHoveredPlayer: (player: number | null) => void;
  index: number;
};

function PlayerCard({ player, setHoveredPlayer, selectedPlayer, setPredictedTeam, index }: PlayerCardProps) {
  function handleSwapPlayer() {
    if (selectedPlayer === null) return;
    setPredictedTeam((prev: string[]) => {
      const newTeam = [...prev];
      newTeam[selectedPlayer] = player;
      return newTeam;
    });
  }

  return (
    <div
      onMouseEnter={() => setHoveredPlayer(index)}
      onMouseLeave={() => setHoveredPlayer(null)}
      onClick={handleSwapPlayer}
    >
      <div className="playerCardSwap flex mr-1 overflow-hidden">
        <div className="mt-4">
          <Image src={profilePhoto} alt="player" width={100} height={100} />
        </div>
      </div>
      <p className="anonymousPlayerText ml-1">
        {player
          .split(" ")
          .map((word) => word.charAt(0).toUpperCase())
          .join("")}
      </p>
    </div>
  );
}

export default function PlayerOptions({
  setHoveredPlayer,
  selectedPlayer,
  predictedTeam,
  setPredictedTeam,
  matchData,
}: PlayerOptionsProps) {
  const leftOutPlayers: string[] = [];
  // const leftOutPlayers = // players not in predicted team but in the player selection done by the user.
  return (
    <div className="playerOptionsDiv">
      <div className="players-list">
        {leftOutPlayers.map((player, index) => {
          if (index < 10) return null;
          return (
            <PlayerCard
              key={index}
              setHoveredPlayer={setHoveredPlayer}
              player={player}
              selectedPlayer={selectedPlayer}
              index={index}
              setPredictedTeam={setPredictedTeam}
            />
          );
        })}
      </div>
    </div>
  );
}

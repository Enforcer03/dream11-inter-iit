import Image from "next/image";
import { RevaluateTeamApiResponse } from "../types/modelApiResponse";

type PlayerOptionsProps = {
  setHoveredPlayer: (player: number | null) => void;
  selectedPlayer: number | null;
  predictedTeam: string[];
  setPredictedTeam: (predictedTeam: string[] | ((prev: string[]) => string[])) => void;
  selectedPlayersTeamA: string[];
  selectedPlayersTeamB: string[];
  handleTeamRevaluation: (newPredictedTeam: string[], flag: boolean) => void;
  setNewTeamStats: (response: RevaluateTeamApiResponse) => void;
};

type PlayerCardProps = {
  player: string;
  selectedPlayer: number | null;
  setPredictedTeam: (predictedTeam: string[] | ((prev: string[]) => string[])) => void;
  predictedTeam: string[];
  handleTeamRevaluation: (newPredictedTeam: string[], flag: boolean) => void;
  setNewTeamStats: (response: RevaluateTeamApiResponse) => void;
};

function PlayerCard({
  player,
  selectedPlayer,
  setPredictedTeam,
  predictedTeam,
  handleTeamRevaluation,
  setNewTeamStats,
}: PlayerCardProps) {
  function handleEnterHoverPlayer() {
    const newPredictedTeam = [...predictedTeam];
    newPredictedTeam[selectedPlayer] = player.name;

    handleTeamRevaluation(newPredictedTeam, false);
  }

  function handleExitHoverPlayer() {
    setNewTeamStats(null);
  }

  function handleSwapPlayer() {
    if (selectedPlayer === null) return;
    const newPredictedTeam = [...predictedTeam];
    newPredictedTeam[selectedPlayer] = player.name;

    setPredictedTeam(newPredictedTeam);

    handleTeamRevaluation(newPredictedTeam, true);
  }

  return (
    <div
      onMouseEnter={() => handleEnterHoverPlayer()}
      onMouseLeave={() => handleExitHoverPlayer()}
      onClick={handleSwapPlayer}
    >
      <div className="playerCardSwap flex mr-1 overflow-hidden">
        <div className="mt-4">
          <Image src={player.image} alt="player" width={100} height={100} />
        </div>
      </div>
      <p className="anonymousPlayerText ml-1">{player.name}</p>
    </div>
  );
}

export default function PlayerOptions({
  selectedPlayer,
  predictedTeam,
  setPredictedTeam,
  selectedPlayersTeamA,
  selectedPlayersTeamB,
  handleTeamRevaluation,
  setNewTeamStats,
}: PlayerOptionsProps) {
  const leftOutPlayers: string[] = [...selectedPlayersTeamA, ...selectedPlayersTeamB].filter(
    (player) => !predictedTeam.includes(player.name)
  );

  // const leftOutPlayers = // players not in predicted team but in the player selection done by the user.
  return (
    <div className="playerOptionsDiv">
      <div className="players-list">
        {leftOutPlayers.map((player, index) => {
          return (
            <PlayerCard
              key={index}
              player={player}
              selectedPlayer={selectedPlayer}
              predictedTeam={predictedTeam}
              setPredictedTeam={setPredictedTeam}
              handleTeamRevaluation={handleTeamRevaluation}
              setNewTeamStats={setNewTeamStats}
            />
          );
        })}
      </div>
    </div>
  );
}

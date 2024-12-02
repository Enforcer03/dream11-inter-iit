import Image from "next/image";
import { RevaluateTeamApiResponse } from "../types/modelApiResponse";

type PlayerOptionsProps = {
  selectedPlayer: number | null;
  predictedTeam: string[];
  setPredictedTeam: (predictedTeam: string[] | ((prev: string[]) => string[])) => void;
  selectedPlayersTeamA: string[];
  selectedPlayersTeamB: string[];
  handleTeamRevaluation: (newPredictedTeam: string[], flag: boolean) => void;
  setNewTeamStats: (response: RevaluateTeamApiResponse) => void;
  setHoverPlayer: (hoverPlayer: string | null) => void;
};

type PlayerCardProps = {
  player: string;
  selectedPlayer: number | null;
  setPredictedTeam: (predictedTeam: string[] | ((prev: string[]) => string[])) => void;
  predictedTeam: string[];
  handleTeamRevaluation: (newPredictedTeam: string[], flag: boolean) => void;
  setNewTeamStats: (response: RevaluateTeamApiResponse) => void;
  setHoverPlayer: (hoverPlayer: string | null) => void;
};

function PlayerCard({
  player,
  selectedPlayer,
  setPredictedTeam,
  predictedTeam,
  handleTeamRevaluation,
  setNewTeamStats,
  setHoverPlayer,
}: PlayerCardProps) {
  function handleEnterHoverPlayer() {
    setHoverPlayer(player.name);
    const newPredictedTeam = [...predictedTeam];
    newPredictedTeam[selectedPlayer] = player.name;
    handleTeamRevaluation(newPredictedTeam, false);
  }

  function handleExitHoverPlayer() {
    setHoverPlayer(null);
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
      <div className="playerCardSwap flex mr-1 mb-1 overflow-hidden">
        <div>
          <Image src={player.image} alt="player" width={100} height={100} />
        </div>
      </div>
      <p className="optionalPlayerText w-[4.8rem] flex text-center justify-center">{`${player.name.split(" ").slice(1).join(" ").slice(0, 7)}`}</p>
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
  setHoverPlayer,
}: PlayerOptionsProps) {
  const leftOutPlayers: string[] = [...selectedPlayersTeamA, ...selectedPlayersTeamB].filter(
    (player) => !predictedTeam.includes(player.name)
  );

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
              setHoverPlayer={setHoverPlayer}
            />
          );
        })}
      </div>
    </div>
  );
}

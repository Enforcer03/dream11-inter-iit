import Image from "next/image";
import profilePhoto from "../../public/photo.png";

type PlayerOptionsProps = {
  setHoveredPlayer: (player: number | null) => void;
  selectedPlayer: number | null;
  predictedTeam: string[];
  setPredictedTeam: (predictedTeam: string[] | ((prev: string[]) => string[])) => void;
  selectedPlayersTeamA: string[];
  selectedPlayersTeamB: string[];
};

type PlayerCardProps = {
  player: string;
  selectedPlayer: number | null;
  setPredictedTeam: (predictedTeam: string[] | ((prev: string[]) => string[])) => void;
  setHoveredPlayer: (player: number | null) => void;
  index: number;
};

function PlayerCard({
  player,
  setHoveredPlayer,
  selectedPlayer,
  setPredictedTeam,
  index,
  handleTeamRevaluation,
}: PlayerCardProps) {
  function handleSwapPlayer() {
    if (selectedPlayer === null) return;
    setPredictedTeam((prev: string[]) => {
      const newTeam = [...prev];
      newTeam[selectedPlayer] = player.name;
      return newTeam;
    });
    handleTeamRevaluation();
  }

  return (
    <div
      onMouseEnter={() => setHoveredPlayer(index)}
      onMouseLeave={() => setHoveredPlayer(null)}
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
  setHoveredPlayer,
  selectedPlayer,
  predictedTeam,
  setPredictedTeam,
  selectedPlayersTeamA,
  selectedPlayersTeamB,
  handleTeamRevaluation,
}: PlayerOptionsProps) {
  console.log("PlayerOptions", predictedTeam);
  const leftOutPlayers: string[] = [...selectedPlayersTeamA, ...selectedPlayersTeamB].filter(
    (player) => !predictedTeam.includes(player.name)
  );

  console.log("leftOutPlayers", leftOutPlayers);
  // const leftOutPlayers = // players not in predicted team but in the player selection done by the user.
  return (
    <div className="playerOptionsDiv">
      <div className="players-list">
        {leftOutPlayers.map((player, index) => {
          return (
            <PlayerCard
              key={index}
              setHoveredPlayer={setHoveredPlayer}
              player={player}
              selectedPlayer={selectedPlayer}
              index={index}
              setPredictedTeam={setPredictedTeam}
              handleTeamRevaluation={handleTeamRevaluation}
            />
          );
        })}
      </div>
    </div>
  );
}

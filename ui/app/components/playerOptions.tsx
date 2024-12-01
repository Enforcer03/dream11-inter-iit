import playerJsonTest from "../../public/playerJsonTest.json";
import profilePhoto from "../../public/photo.png";
import Image from "next/image";

function PlayerCard({ player, setHoveredPlayer, setFinalPlayers, selectedPlayer, finalPlayers }) {
  function handleSwapPlayer() {
    if (selectedPlayer.playNumber === player.playNumber) return;

    const indexSelected = playerJsonTest.findIndex((p) => p.playNumber === player.playNumber);

    const indexFinal = finalPlayers.findIndex((p) => playerJsonTest[p].playNumber === selectedPlayer.playNumber);

    const newFinalPlayers = [...finalPlayers];

    newFinalPlayers[indexFinal] = indexSelected;

    setFinalPlayers(newFinalPlayers);
  }

  return (
    <div
      onMouseEnter={() => setHoveredPlayer(player)}
      onMouseLeave={() => setHoveredPlayer(null)}
      onClick={handleSwapPlayer}
    >
      <div className="playerCardSwap flex mr-1 overflow-hidden">
        <div className="mt-4">
          <Image src={profilePhoto} alt="player" width={100} height={100} />
        </div>
      </div>
      <p className="anonymousPlayerText ml-1">{player.name
                    .split(" ")
                    .map((word) => word.charAt(0).toUpperCase())
                    .join("")}
      </p>
    </div>
  );
}

export default function PlayerOptions({ setFinalPlayers, setHoveredPlayer, selectedPlayer, finalPlayers }) {
  return (
    <div className="playerOptionsDiv">
        <div className="players-list">
          {playerJsonTest.map((player, index) => {
          if (index < 10) return null;
          return (
            <PlayerCard
              setHoveredPlayer={setHoveredPlayer}
              key={index}
              player={player}
              setFinalPlayers={setFinalPlayers}
              selectedPlayer={selectedPlayer}
              finalPlayers={finalPlayers}
            />
          );
          })}
        </div>
    </div>
  );
}

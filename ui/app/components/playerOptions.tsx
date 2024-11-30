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
      className="w-36 mx-2"
      onMouseEnter={() => setHoveredPlayer(player)}
      onMouseLeave={() => setHoveredPlayer(null)}
      onClick={handleSwapPlayer}
    >
      <div className="playerCardSwap flex">
        <div className="flex flex-col h-24 text-black">
          <div className="font-bold text-lg">{player.playNumber}</div>
          <div className="text-sm">{"ST"}</div>
          <div>{player.flag}</div>
          <div>{player.flag}</div>
        </div>
        <div className="mt-8">
          <Image src={profilePhoto} alt="player" width={200} height={200} />
        </div>
      </div>
      <p className="font-bold text-[#FFECB2] text-center backdrop-blur-md">{player.name}</p>
    </div>
  );
}

export default function PlayerOptions({ setFinalPlayers, setHoveredPlayer, selectedPlayer, finalPlayers }) {
  return (
    <div className="player-swap-area w-full text-white">
      <div className="flex w-full">
        {playerJsonTest.map((player, index) => {
          if (index > 10) return null;
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
      <div className="flex w-full">
        {playerJsonTest.map((player, index) => {
          if (index < 11) return null;
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

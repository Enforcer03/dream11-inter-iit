"use client";

import { useRouter } from "next/navigation";
import playersImages from "../../public/playerImages.json";
import { PlayerStats } from "../contexts/matchDataContext";

function PlayerList({
  predictedTeam,
  playerStats,
  selectedPlayersTeamA,
  selectedPlayersTeamB,
}: {
  predictedTeam: string[];
  playerStats: PlayerStats[];
  selectedPlayersTeamA: string[];
  selectedPlayersTeamB: string[];
}) {
  const router = useRouter();

  const playerStatsLookup = playerStats.reduce(
    (map, playerStat) => {
      map[playerStat.player] = playerStat;
      return map;
    },
    {} as Record<string, PlayerStats>
  );

  function handlePlayerClick(id: number, image: string) {
    router.push(`/player-information?id=${id}&image=${encodeURIComponent(image)}`);
  }

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

    return matchingPlayer ? matchingPlayer.image : "https://cdn.sportmonks.com/images/cricket/placeholder.png";
  }

  return (
    <div className="players-list">
      {predictedTeam.map((player, index) => (
        <div
          key={index}
          className="badge-bg cursor-pointer"
          onClick={() =>
            handlePlayerClick(player, getPlayerImagePath(player, selectedPlayersTeamA, selectedPlayersTeamB))
          }
        >
          <div className="player-image-container">
            <div className="image-container">
              <img
                src={getPlayerImagePath(player, selectedPlayersTeamA, selectedPlayersTeamB)}
                alt="Player Image"
                className="player-image"
              />
            </div>
          </div>
          <div className="player-bio-container">
            <h4 className="player-name">
              {player.split(" ")[0].charAt(0)}. {player.split(" ").slice(1).join(" ").slice(0, 10)}
            </h4>
            <hr className="player-hr" />
            <div className="player-bio">
              <div className="flex flex-col">
                <p className="w-full ">🏏: {playerStatsLookup[player].batting_points.toFixed(1)}</p>
                <p className="w-full">W: {playerStatsLookup[player].fielding_points.toFixed(1)}</p>
              </div>
              <hr className="badge-hr" />
              <div className="flex flex-col">
                <p className="w-full">⚾️: {playerStatsLookup[player].bowling_points.toFixed(1)}</p>
                <p className="w-full">Av: {playerStatsLookup[player].mean_points.toFixed(1)}</p>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

export default PlayerList;

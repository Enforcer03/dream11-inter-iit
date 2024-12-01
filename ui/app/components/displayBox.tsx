"use client";

import { useRouter } from "next/navigation";
import countryImages from "../../public/countryImages.json";
import playersImages from "../../public/playerImages.json";
import { PlayerStats } from "../contexts/matchDataContext";

function PlayerList({ predictedTeam, playerStats }: { predictedTeam: string[]; playerStats: PlayerStats[] }) {
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

  function getPlayerImagePath(playerName: string) {
    const matchingPlayer = playersImages.data.find((imageData) => {
      const isMatch = imageData.fullname === playerName;
      if (isMatch) {
      imageData.image_path;
      }
      return isMatch;
    });

    if (!matchingPlayer) {
      playersImages.data[4].image_path;
    }

    return matchingPlayer ? matchingPlayer.image_path : playersImages.data[4].image_path;
  }

  return (
    <div className="players-list">
      {predictedTeam.map((player, index) => (
        <div key={index} className="badge-bg" onClick={() => handlePlayerClick(index, getPlayerImagePath(player))}>
          <div className="player-image-container">
            <div className="flag-container">
              <img src={countryImages.data[0].image_path} alt="Flag" className="flag" />
              <hr className="flag-hr" />
              <img src={countryImages.data[0].image_path} alt="Flag" className="flag" />
              <hr className="flag-hr" />
              <img src={countryImages.data[0].image_path} alt="Flag" className="flag" />
            </div>
            <div className="image-container">
              <img src={getPlayerImagePath(player)} alt="Player Image" className="player-image" />
            </div>
          </div>
          <div className="player-bio-container">
            <h4 className="player-name">
              {player.split(" ")[0].charAt(0)}. {player.split(" ").slice(1).join(" ")}
            </h4>
            <hr className="player-hr" />
            <div className="player-bio">
              <div className="flex flex-col">
                <p className="w-full ">🏏: {playerStats[index].batting_points}</p>
                <p className="w-full">WIC: {playerStats[index].fielding_points}</p>
              </div>
              <hr className="badge-hr" />
              <div className="flex flex-col">
                <p className="w-full">⚾️: {playerStatsLookup[player].bowling_points}</p>
                <p className="w-full">AVG: {playerStats[index].mean_points}</p>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

export default PlayerList;

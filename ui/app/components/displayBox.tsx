"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import playersData from "../../public/players.json";
import playersData2 from "../../public/players2.json";
import playersImages from "../../public/playerImages.json";
import countryImages from "../../public/countryImages.json";

interface Player {
  id: number;
  name: string;
  image: string;
  countryFlag: string;
  bio: string;
}

const PlayerList = () => {
  const [players, setPlayers] = useState<Player[]>([]);
  const router = useRouter();

  useEffect(() => {
    fetch("/players.json")
      .then((response) => response.json())
      .then((data) => setPlayers(data.players.slice(0, 11)));
  }, []);

  const handlePlayerClick = (id: number, image: string) => {
    router.push(`/player-information?id=${id}&image=${encodeURIComponent(image)}`);
  };

  const getPlayerImagePath = (playerName: string) => {
    const matchingPlayer = playersImages.data.find((imageData) => {
      console.log("Comparing with:", imageData.fullname);
      const isMatch = imageData.fullname === playerName;
      if (isMatch) {
        console.log("Match found! Image path:", imageData.image_path);
      }
      return isMatch;
    });

    if (!matchingPlayer) {
      console.log("No match found, using default image:", playersImages.data[4].image_path);
    }

    return matchingPlayer ? matchingPlayer.image_path : playersImages.data[4].image_path;
  };

  return (
    <div className="players-list">
      {players.map((player) => (
        <div
          key={player.id}
          className="badge-bg"
          onClick={() => handlePlayerClick(player.id, getPlayerImagePath(player.name))}
        >
          {" "}
          <div className="player-image-container">
            <div className="flag-container">
              <img src={countryImages.data[0].image_path} alt="Flag" className="flag" />
              <hr className="flag-hr" />
              <img src={countryImages.data[0].image_path} alt="Flag" className="flag" />
              <hr className="flag-hr" />
              <img src={countryImages.data[0].image_path} alt="Flag" className="flag" />
            </div>
            <div className="image-container">
              <img src={getPlayerImagePath(player.name)} alt="Player Image" className="player-image" />
            </div>
          </div>
          <div className="player-bio-container">
            <h4 className="player-name">
              {player.name.split(" ")[0].charAt(0)}. {player.name.split(" ").slice(1).join(" ")}
            </h4>
            <hr className="player-hr" />
            <div className="player-bio">
              <div className="flex flex-col">
                <p className="w-full ">🏏: {12}</p>
                <p className="w-full">WIC: {311}</p>
              </div>
              <hr className="badge-hr" />
              <div className="flex flex-col">
                <p className="w-full">⚾️: {2}</p>
                <p className="w-full">AVG: {101}</p>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default PlayerList;

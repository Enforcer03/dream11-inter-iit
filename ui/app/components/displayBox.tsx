"use client";

import { useEffect, useState } from "react";
import { useRouter } from 'next/navigation';

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

  const handlePlayerClick = (id: number) => {
    router.push(`/swap-player?id=${id}`);
  };

  return (
    <div className="players-list">
      {players.map((player) => (
        <div
          key={player.id}
          className="badge-bg"
          onClick={() => handlePlayerClick(player.id)}
        >
          <div className="player-image-container">
            <div className="flag-container">
              <img src={player.countryFlag} alt="Flag" className="flag" />
              <hr className="flag-hr" />
              <img src={player.countryFlag} alt="Flag" className="flag" />
              <hr className="flag-hr" />
              <img src={player.countryFlag} alt="Flag" className="flag" />
            </div>
            <div className="image-container">
              <img src={player.image} alt="Player Image" className="player-image" />
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

"use client";

import { useEffect, useState } from "react";

interface Player {
  id: number;
  name: string;
  image: string;
  countryFlag: string;
  bio: string;
}

const PlayerList = () => {
  const [players, setPlayers] = useState<Player[]>([]);

  useEffect(() => {
    fetch("/players.json")
      .then((response) => response.json())
      .then((data) => setPlayers(data.players));
  }, []);

  return (
    <div className="players-list w-5/6">
      {players.map((player) => (

        <div key={player.id} className="badge-bg">
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
            <p className="player-bio">
              {player.bio.split(" ").slice(0, 5).join(" ")}
              {player.bio.split(" ").length > 7 ? "..." : ""}
            </p>
          </div>
        </div>
      ))}
    </div>
  );
};

export default PlayerList;

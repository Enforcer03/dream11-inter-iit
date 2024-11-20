"use client";

import { useState } from "react";
import AnonymousPlayer from "./anonymousPlayer";
import playersData from "../../public/players.json";

const PeopleDisplay = () => {
  const [selectedPlayers, setSelectedPlayers] = useState(
    playersData.players.slice(0, 11)
  );
  const [filledDivs, setFilledDivs] = useState<
    (null | (typeof playersData.players)[0])[]
  >(Array(11).fill(null));

  const handleOptionClick = (player: (typeof playersData.players)[0]) => {
    if (filledDivs.some((filledPlayer) => filledPlayer?.id === player.id)) {
      return;
    }

    setFilledDivs((prev) => {
      const emptyIndex = prev.findIndex((p) => p === null);
      if (emptyIndex !== -1) {
        const newFilledDivs = [...prev];
        newFilledDivs[emptyIndex] = player;
        return newFilledDivs;
      }
      return prev;
    });
  };

  const handleEmptyDivClick = (index: number) => {
    setFilledDivs((prev) => {
      const newFilledDivs = [...prev];
      newFilledDivs[index] = null;
      return newFilledDivs;
    });
  };

  return (
    <div>
      <div className="selectionListDiv">
        <div className="players-list">
          {selectedPlayers.map((player) => (
            <div
              key={player.id}
              onClick={() => handleOptionClick(player)}
              className={`text-center cursor-pointer badge-bg-small ${
                filledDivs.some(
                  (filledPlayer) => filledPlayer?.id === player.id
                )
                  ? "cursor-not-allowed"
                  : ""
              }`}
              style={{ minHeight: "150px" }}
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
                  <img
                    src={player.image}
                    alt="Player Image"
                    className="player-image"
                  />
                </div>
              </div>
              {/* <div className="player-bio-container">
                <h3 className="player-name">
                  {player.name.split(" ")[0].charAt(0)}.{" "}
                  {player.name.split(" ").slice(1).join(" ")}
                </h3>
                <hr className="player-hr" />
                <p className="player-bio">
                  {player.bio.split(" ").slice(0, 7).join(" ")}
                  {player.bio.split(" ").length > 10 ? "..." : ""}
                </p>
              </div> */}
            </div>
          ))}
        </div>
      </div>

      <div className="selectListDiv">
        <div className="players-list">
          {filledDivs.map((player, index) => (
            <div
              key={index}
              onClick={() => handleEmptyDivClick(index)}
              className={`text-center ${
                player ? "bgSelectedPlayer cursor-pointer" : ""
              }`}
              style={{ minHeight: "150px" }}
            >
              {player ? (
                <div className="flex flex-col items-center">
                  <div className="player-image-container">
                    <div className="flag-container">
                      <img
                        src={player.countryFlag}
                        alt="Flag"
                        className="flag"
                      />
                      <hr className="flag-hr" />
                      <img
                        src={player.countryFlag}
                        alt="Flag"
                        className="flag"
                      />
                      <hr className="flag-hr" />
                      <img
                        src={player.countryFlag}
                        alt="Flag"
                        className="flag"
                      />
                    </div>
                    <div className="image-container">
                      <img
                        src={player.image}
                        alt="Player Image"
                        className="player-image"
                      />
                    </div>
                  </div>
                </div>
              ) : (
                <AnonymousPlayer children={"PLAYER"} />
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default PeopleDisplay;

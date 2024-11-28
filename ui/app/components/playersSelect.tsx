"use client";

import { useState } from "react";
import AnonymousPlayer from "./anonymousPlayer";
import SelectedPlayer from "./selectedPlayer";
import playersData from "../../public/players.json";
import PlayerInformation from "./playerInformation";

const PeopleDisplay = () => {
  const [selectedPlayers, setSelectedPlayers] = useState(playersData.players.slice(0, 11));
  const [filledDivs, setFilledDivs] = useState<(null | (typeof playersData.players)[0])[]>(Array(11).fill(null));
  const [details, setDetails] = useState(playersData.players[0]);

  const handleSelection = () => {
    setFilledDivs(playersData.players.slice(0, 11));
  };

  const handleDetails = (player: (typeof playersData.players)[0]) => {
    setDetails(player);
  };

  const handleOptionClick = (player: (typeof playersData.players)[0]) => {
    handleDetails(player);
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
      <div className="playerShortDetails">
        <PlayerInformation
          title={"PLAYER SELECTION"}
          child2={details.name}
          child3={details.image}
          child4={details.countryFlag}
        />
      </div>

      <div className="selectionListDiv">
        <div className="players-list w-[59rem]">
          {selectedPlayers.map((player) => (
            <div
              key={player.id}
              onClick={() => handleOptionClick(player)}
              className={`text-center cursor-pointer badge-bg ${
                filledDivs.some((filledPlayer) => filledPlayer?.id === player.id) ? "cursor-not-allowed" : ""
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
                  <img src={player.image} alt="Player Image" className="player-image" />
                </div>
              </div>
              <div className="player-bio-container">
                <h3 className="player-name">
                  {player.name.split(" ")[0].charAt(0)}. {player.name.split(" ").slice(1).join(" ")}
                </h3>
                <hr className="player-hr" />
                <p className="player-bio">
                  {player.bio.split(" ").slice(0, 5).join(" ")}
                  {player.bio.split(" ").length > 7 ? "..." : ""}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="selectListDiv">
        <div className="-mb-10 ml-11">
          <h1 className="text-xl font-bold text-[#FFD700] inline">SELECTED PLAYERS</h1>
          <button className="autoSelectBtn" onClick={handleSelection}>
            AUTO SELECT
          </button>
        </div>
        <div className="flex justify-center">
          <div className="players-list">
            {filledDivs.map((player, index) => (
              <div
                key={index}
                onClick={() => handleEmptyDivClick(index)}
                className={`text-center ${player ? "cursor-pointer" : ""} flex flex-col items-center justify-center`}
                style={{ minHeight: "150px" }}
              >
                {player ? (
                  <SelectedPlayer
                    child1={
                      <img src={player.image} alt="Player Image" className="select-player-image no-repeat center" />
                    }
                    child2={player.name
                      .split(" ")
                      .map((word) => word.charAt(0).toUpperCase())
                      .join("")}
                  />
                ) : (
                  <AnonymousPlayer>PLAYER</AnonymousPlayer>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default PeopleDisplay;

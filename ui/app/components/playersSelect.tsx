"use client";

import { useState } from "react";
import AnonymousPlayer from "./anonymousPlayer";
import SelectedPlayer from "./selectedPlayer";
import Button from "./buttonComp";
import playersData from "../../public/players.json";
import playersData2 from "../../public/players.json";
import playersImages from "../../public/playerImages.json";
import countryImages from "../../public/countryImages.json";
import PlayerInformation from "./playerInformation";
import { useMatchData } from "../contexts/matchDataContext";

type SimplifiedPlayer = {
  id: number;
  name: string;
  image: string;
};

function PeopleDisplay() {
  const { aggregateStats, matchData } = useMatchData();

  if (!aggregateStats) return null;
  const stats = aggregateStats;

  console.log(Object.keys(stats));
  const playerNames = Object.keys(aggregateStats);
  const format = matchData?.Format;

  console.log("Player Names:", playerNames);
  console.log("Format:", format);

  const [currentDataset, setCurrentDataset] = useState(1);
  const [selectedPlayers, setSelectedPlayers] = useState(playersData.players);
  const [selectedData, setSelectedData] = useState([]);
  const [filledDivs, setFilledDivs] = useState<(null | SimplifiedPlayer)[]>(Array(11).fill(null));
  const [details, setDetails] = useState(playersData.players[0]);

  const handleSelection = () => {
    const simplifiedPlayers = selectedPlayers.slice(0, 11).map((player) => ({
      id: player.id,
      name: player.name,
      image: getPlayerImagePath(player.name),
    }));
    setFilledDivs(simplifiedPlayers);
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
        // Create simplified player object
        const simplifiedPlayer: SimplifiedPlayer = {
          id: player.id,
          name: player.name,
          image: getPlayerImagePath(player.name),
        };
        newFilledDivs[emptyIndex] = simplifiedPlayer;
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

  console.log(selectedData.length);

  const handleNext = () => {
    if (currentDataset === 1) {
      setCurrentDataset(2);
      setSelectedPlayers(playersData2.players);
      setDetails(playersData2.players[0]);
      setSelectedData(filledDivs.filter((player) => player !== null));
      setFilledDivs(Array(11).fill(null));
    }
  };

  const getPlayerImagePath = (playerName: string) => {
    const matchingPlayer = playersImages.data.find((imageData) => {
      const isMatch = imageData.fullname === playerName;
      if (isMatch) {
        console.log("Match found! Image path:", imageData.image_path);
        return isMatch;
      }
    });

    if (!matchingPlayer) {
      console.log("No match found, using default image:", playersImages.data[4].image_path);
    }

    return matchingPlayer ? matchingPlayer.image_path : playersImages.data[4].image_path;
  };

  const prevPage = "/select-match";
  const nextPage = "/playing11";

  // Calculate number of selected players
  const countTeam1 = selectedData.length;
  const countTeam2 = filledDivs.filter((player) => player !== null).length;

  // Determine if Next button should be active
  const isNextActive = currentDataset === 1 || countTeam1 + countTeam2 >= 11;

  return (
    <div>
      <div className="playerShortDetails">
        <PlayerInformation
          title={"PLAYER SELECTION"}
          child2={details.name}
          child3={getPlayerImagePath(details.name)}
          child4={countryImages.data[0].image_path}
        />
      </div>

      <div className="selectionListDiv">
        <div className="players-list ">
          {playerNames.map((playerName, index) => (
            <div
              key={index}
              onClick={() => handleOptionClick(playerName)}
              className={`text-center cursor-pointer badge-bg ${
                filledDivs.some((filledPlayer) => filledPlayer?.id === playerName.id) ? "cursor-not-allowed" : ""
              }`}
              style={{ minHeight: "150px" }}
            >
              <div className="player-image-container">
                <div className="flag-container">
                  <img src={countryImages.data[0].image_path} alt="Flag" className="flag" />
                  <hr className="flag-hr" />
                  <img src={countryImages.data[0].image_path} alt="Flag" className="flag" />
                  <hr className="flag-hr" />
                  <img src={countryImages.data[0].image_path} alt="Flag" className="flag" />
                </div>
                <div className="image-container">
                  <img src={getPlayerImagePath(playerName)} alt="Player Image" className="player-image" />
                </div>
              </div>
              <div className="player-bio-container">
                <h3 className="player-name">
                  {playerName.split(" ")[0].charAt(0)}. {playerName.split(" ").slice(1).join(" ")} {playerName}
                </h3>
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
      </div>

      <div className="selectListDiv">
        <div className="-mb-2 ml-5">
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
      <div className="buttonPlayerSelectionDiv">
        {currentDataset === 1 ? (
          <Button onClick={handleNext} disabled={!isNextActive}>
            NEXT
          </Button>
        ) : (
          <Button nextPage={nextPage} disabled={!isNextActive}>
            PREDICT 11
          </Button>
        )}
        <Button nextPage={prevPage}>BACK</Button>
      </div>
    </div>
  );
}

export default PeopleDisplay;

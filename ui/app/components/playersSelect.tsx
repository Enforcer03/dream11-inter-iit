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

  const [currentDataset, setCurrentDataset] = useState(1);
  const [selectedPlayers, setSelectedPlayers] = useState(playerNames);
  const [selectedData, setSelectedData] = useState([]);
  const [filledDivs, setFilledDivs] = useState<(null | SimplifiedPlayer)[]>(Array(11).fill(null));
  const [details, setDetails] = useState(playersData.players[0]);

  const handleSelection = () => {
    const simplifiedPlayers = selectedPlayers.slice(0, 11).map((player) => ({
      id: player.id,
      name: player.name,
      image: "",
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
    let nameParts = playerName.split(' ');
    let lastName = nameParts[nameParts.length - 1]
    const matchingPlayer = playersImages.data.find((imageData) => {
      const isMatch = imageData.lastname === lastName;
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

  const countTeam1 = selectedData.length;
  const countTeam2 = filledDivs.filter((player) => player !== null).length;

  const isNextActive = currentDataset === 1 || countTeam1 + countTeam2 >= 11;

  return (
    <div>
      <div className="playerShortDetails">
  {/* Ensure you have a format defined, e.g., 'ODI', 'T20', or 'Test' */}
  {format && ['ODI', 'T20', 'Test'].includes(format) && details.name && (
    <PlayerInformation
      title={"PLAYER SELECTION"}
      child2={details.name}
      child3={getPlayerImagePath(details.name)}
      child4={countryImages.data[0].image_path}
      child5={aggregateStats[details.name]?.[format]?.["Batting S/R"] || "No data"}
      child6={aggregateStats[details.name]?.[format]?.["Runs"] || "No data"}
      child7={aggregateStats[details.name]?.[format]?.["Batting Avg"] || "No data"}
      child8={aggregateStats[details.name]?.[format]?.["Wickets"] || "-"}
      child9={aggregateStats[details.name]?.[format]?.["Economy Rate"] || "No data"}
      child10={aggregateStats[details.name]?.[format]?.["Bowling S/R"] || "No data"}
    />
  )}
</div>


    <div className="selectionListDiv">
      <div className="players-list ">
        {playerNames.map((playerName, index) => {
          const playerStats = aggregateStats[playerName];
          const battingAvg = format && ['ODI', 'T20', 'Test'].includes(format)
            ? playerStats[format]["Batting Avg"]
            : "No data";

          const wickets = playerStats[format]?.["Wickets"] || "-";
          const bowling = playerStats[format]?.["Bowling S/R"] || "-";
          const battingSR = playerStats[format]["Batting S/R"] || "-";

          return (
            <div
              key={index}
              onClick={() => handleOptionClick({id:index, name:playerName})}
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
                  {playerName.split(" ")[0].charAt(0)}. {playerName.split(" ").slice(1).join(" ")}
                </h3>
                <hr className="player-hr" />
                <div className="player-bio">
                  <div className="flex flex-col">
                    <p className="w-full ">🏏: {battingSR}</p>
                    <p className="w-full">WIC: {wickets}</p>
                  </div>
                  <hr className="badge-hr" />
                  <div className="flex flex-col">
                    <p className="w-full">⚾️: {bowling}</p>
                    <p className="w-full">AVG: {battingAvg}</p>
                  </div>
                </div>
              </div>
            </div>
          );
        })}
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
                      <img src={getPlayerImagePath(player.name)} alt="Player Image" className="select-player-image no-repeat center" />
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

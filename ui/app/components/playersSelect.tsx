"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import AnonymousPlayer from "./anonymousPlayer";
import SelectedPlayer from "./selectedPlayer";
import Button from "./buttonComp";
import playersData from "../../public/players.json";
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
  const router = useRouter();

  if (!aggregateStats) return null;

  const playerNames = Object.keys(aggregateStats);
  const format = matchData?.Format;

  const [currentDataset, setCurrentDataset] = useState(1);
  const [selectedPlayers, setSelectedPlayers] = useState(matchData[Object.keys(matchData).filter(team => team !== "Format")[currentDataset - 1]]);
  const [selectedData, setSelectedData] = useState([]);
  const [filledDivs, setFilledDivs] = useState<(null | SimplifiedPlayer)[]>(Array(11).fill(null));
  const [details, setDetails] = useState({id: 0, name: matchData[Object.keys(matchData).filter(team => team !== "Format")[currentDataset - 1]][0]});

  const handleSelection = () => {playerNames
    const simplifiedPlayers = selectedPlayers.slice(0, 11).map((player, index) => ({
      id: index,
      name: player,
      image: getPlayerImagePath(player),
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

    setSelectedData((prevSelectedDivs) => {
      return [...prevSelectedDivs, player];
    });
  };

  const handleEmptyDivClick = (index: number) => {
    setFilledDivs((prev) => {
      const newFilledDivs = [...prev];
      newFilledDivs[index] = null;
      return newFilledDivs;
    });
  };

  const handleNext = () => {
    if (currentDataset === 1) {
      setCurrentDataset(2);
      setSelectedPlayers(matchData[Object.keys(matchData).filter(team => team !== "Format")[1]]);
      setDetails({id: 0, name: matchData[Object.keys(matchData).filter(team => team !== "Format")[1]][0]});
      setSelectedData(filledDivs.filter((player) => player !== null));
      setFilledDivs(Array(11).fill(null));
    }
  };

  const displaySelected = () => {
    setSelectedData((prevSelectedData) => {
      const updatedSelectedData = [
        ...prevSelectedData,
        ...filledDivs.filter((player) => player !== null)
      ];
      return updatedSelectedData;
    });

    setFilledDivs(Array(11).fill(null));

    router.push(nextPage);
  }

  const getPlayerImagePath = (playerName: string) => {
    let nameParts = playerName.split(" ");
    let lastName = nameParts[nameParts.length - 1];
    const matchingPlayer = playersImages.data.find((imageData) => {
      const isMatch = imageData.lastname === lastName;
      if (isMatch) {
        return isMatch;
      }
    });

    if (!matchingPlayer) {
      playersImages.data[4].image_path;
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
        {format && ['ODI', 'T20', 'Test'].includes(format) && details.name && (() => {

          let battingSR = aggregateStats[details.name]?.[format]?.["Batting S/R"];
          let runs = aggregateStats[details.name]?.[format]?.["Runs"];
          let battingAvg = aggregateStats[details.name]?.[format]?.["Batting Avg"];
          let wickets = aggregateStats[details.name]?.[format]?.["Wickets"];
          let economyRate = aggregateStats[details.name]?.[format]?.["Economy Rate"];
          let bowlingSR = aggregateStats[details.name]?.[format]?.["Bowling S/R"];

          if (battingSR == null || battingSR === Infinity || battingSR < 0) {
            battingSR = "-";
          }
          if (runs == null || runs === Infinity || runs < 0) {
            runs = "-";
          }
          if (battingAvg == null || battingAvg === Infinity || battingAvg < 0) {
            battingAvg = "-";
          }
          if (wickets == null || wickets === Infinity || wickets < 0) {
            wickets = "-";
          }
          if (economyRate == null || economyRate === Infinity || economyRate < 0) {
            economyRate = "-";
          }
          if (bowlingSR == null || bowlingSR === Infinity || bowlingSR < 0) {
            bowlingSR = "-";
          }

          return (
            <PlayerInformation
              title={"PLAYER SELECTION"}
              child2={details.name}
              child3={getPlayerImagePath(details.name)}
              child4={countryImages.data[0].image_path}
              child5={battingSR}
              child6={runs}
              child7={battingAvg}
              child8={wickets}
              child9={economyRate}
              child10={bowlingSR}
            />
          );
        })()}
      </div>

      <div className="selectionListDiv">
        <div className="players-list ">
          {(() => {
            const firstTeam = Object.keys(matchData).filter(team => team !== "Format")[currentDataset - 1];
            const teamPlayers = matchData[firstTeam];

            return teamPlayers.map((playerName, playerIndex) => {
              const playerStats = aggregateStats[playerName];
              let battingAvg = format && ['ODI', 'T20', 'Test'].includes(format)
                ? playerStats[format]["Batting Avg"]
                : "No data";

              let wickets = playerStats[format]?.["Wickets"];
              let bowling = playerStats[format]?.["Bowling S/R"];
              let battingSR = playerStats[format]["Batting S/R"];

              if (battingAvg == null || battingAvg === Infinity || battingAvg < 0) {
                battingAvg = "-";
              }
              if (wickets == null || wickets === Infinity || wickets < 0) {
                wickets = "-";
              }
              if (bowling == null || bowling === Infinity || bowling < 0) {
                bowling = "-";
              }
              if (battingSR == null || battingSR === Infinity || battingSR < 0) {
                battingSR = "-";
              }

              return (
                <div
                  key={`${firstTeam}-${playerIndex}`}
                  onClick={() => handleOptionClick({ id: playerIndex, name: playerName })}
                  className={`text-center cursor-pointer badge-bg ${
                    filledDivs.some((filledPlayer) => filledPlayer?.id === playerName.id)
                      ? "cursor-not-allowed"
                      : ""
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
            });
          })()}
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
                      <img
                        src={getPlayerImagePath(player.name)}
                        alt="Player Image"
                        className="select-player-image no-repeat center"
                      />
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
          <Button onClick={displaySelected} nextPage={nextPage} disabled={!isNextActive}>
            PREDICT 11
          </Button>
        )}
        <Button nextPage={prevPage}>BACK</Button>
      </div>
    </div>
  );
}

export default PeopleDisplay;

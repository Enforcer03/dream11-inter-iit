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
  // const { aggregateStats, matchData } = useMatchData();
const aggregateStats = {
  "BM Duckett": {
    "ODI": {
      "Batting": "Left hand",
      "Batting Avg": 32.9,
      "Batting S/R": 93.1,
      "Bowling": "Right arm off break",
      "Bowling S/R": -1.0,
      "Economy Rate": -1.0,
      "Runs": 1579,
      "Wickets": 0
    },
    "T20": {
      "Batting": "Left hand",
      "Batting Avg": 30.21,
      "Batting S/R": 137.6,
      "Bowling": "Right arm off break",
      "Bowling S/R": -1.0,
      "Economy Rate": -1.0,
      "Runs": 4471,
      "Wickets": 0
    },
    "Test": {
      "Batting": "Left hand",
      "Batting Avg": 30.21,
      "Batting S/R": 137.6,
      "Bowling": "Right arm off break",
      "Bowling S/R": -1.0,
      "Economy Rate": -1.0,
      "Runs": 4471,
      "Wickets": 0
    }
  },
  "JA Morkel": {
    "ODI": {
      "Batting": "Left hand",
      "Batting Avg": 20.38,
      "Batting S/R": 92.6,
      "Bowling": "Right arm pace",
      "Bowling S/R": 101.7,
      "Economy Rate": 6.5,
      "Runs": 163,
      "Wickets": 3
    },
    "T20": {
      "Batting": "Left hand",
      "Batting Avg": 23.05,
      "Batting S/R": 140.1,
      "Bowling": "Right arm pace",
      "Bowling S/R": 21.4,
      "Economy Rate": 7.7,
      "Runs": 1729,
      "Wickets": 110
    },
    "Test": {
      "Batting": "Left hand",
      "Batting Avg": 23.05,
      "Batting S/R": 140.1,
      "Bowling": "Right arm pace",
      "Bowling S/R": 21.4,
      "Economy Rate": 7.7,
      "Runs": 1729,
      "Wickets": 110
    }
  },
  "JJ Roy": {
    "ODI": {
      "Batting": "Right hand",
      "Batting Avg": 40.02,
      "Batting S/R": 105.2,
      "Bowling": -1,
      "Bowling S/R": -1.0,
      "Economy Rate": -1.0,
      "Runs": 5483,
      "Wickets": 0
    },
    "T20": {
      "Batting": "Right hand",
      "Batting Avg": 27.98,
      "Batting S/R": 142.6,
      "Bowling": -1,
      "Bowling S/R": Infinity,
      "Economy Rate": 16.0,
      "Runs": 8002,
      "Wickets": 0
    },
    "Test": {
      "Batting": "Right hand",
      "Batting Avg": 27.98,
      "Batting S/R": 142.6,
      "Bowling": -1,
      "Bowling S/R": Infinity,
      "Economy Rate": 16.0,
      "Runs": 8002,
      "Wickets": 0
    }
  },
  "JT Smuts": {
    "ODI": {
      "Batting": "Right hand",
      "Batting Avg": 45.0,
      "Batting S/R": 78.6,
      "Bowling": "Left arm orthodox",
      "Bowling S/R": 45.0,
      "Economy Rate": 5.5,
      "Runs": 180,
      "Wickets": 4
    },
    "T20": {
      "Batting": "Right hand",
      "Batting Avg": 26.01,
      "Batting S/R": 127.0,
      "Bowling": "Left arm orthodox",
      "Bowling S/R": 25.3,
      "Economy Rate": 6.8,
      "Runs": 3147,
      "Wickets": 81
    },
    "Test": {
      "Batting": "Right hand",
      "Batting Avg": 26.01,
      "Batting S/R": 127.0,
      "Bowling": "Left arm orthodox",
      "Bowling S/R": 25.3,
      "Economy Rate": 6.8,
      "Runs": 3147,
      "Wickets": 81
    }
  },
  "KA Maharaj": {
    "ODI": {
      "Batting": "Right hand",
      "Batting Avg": 13.22,
      "Batting S/R": 82.6,
      "Bowling": "Left arm orthodox",
      "Bowling S/R": 40.3,
      "Economy Rate": 4.6,
      "Runs": 238,
      "Wickets": 55
    },
    "T20": {
      "Batting": "Right hand",
      "Batting Avg": 14.63,
      "Batting S/R": 102.3,
      "Bowling": "Left arm orthodox",
      "Bowling S/R": 22.7,
      "Economy Rate": 6.8,
      "Runs": 439,
      "Wickets": 119
    },
    "Test": {
      "Batting": "Right hand",
      "Batting Avg": 14.63,
      "Batting S/R": 102.3,
      "Bowling": "Left arm orthodox",
      "Bowling S/R": 22.7,
      "Economy Rate": 6.8,
      "Runs": 439,
      "Wickets": 119
    }
  },
  "KJ Abbott": {
    "ODI": {
      "Batting": "Right hand",
      "Batting Avg": 11.06,
      "Batting S/R": 63.4,
      "Bowling": "Right arm pace",
      "Bowling S/R": 35.9,
      "Economy Rate": 5.2,
      "Runs": 199,
      "Wickets": 69
    },
    "T20": {
      "Batting": "Right hand",
      "Batting Avg": 13.5,
      "Batting S/R": 124.8,
      "Bowling": "Right arm pace",
      "Bowling S/R": 20.8,
      "Economy Rate": 8.4,
      "Runs": 297,
      "Wickets": 133
    },
    "Test": {
      "Batting": "Right hand",
      "Batting Avg": 13.5,
      "Batting S/R": 124.8,
      "Bowling": "Right arm pace",
      "Bowling S/R": 20.8,
      "Economy Rate": 8.4,
      "Runs": 297,
      "Wickets": 133
    }
  },
  "M de Lange": {
    "ODI": {
      "Batting": "Right hand",
      "Batting Avg": 19.0,
      "Batting S/R": 128.5,
      "Bowling": "Right arm pace",
      "Bowling S/R": 26.7,
      "Economy Rate": 6.5,
      "Runs": 266,
      "Wickets": 46
    },
    "T20": {
      "Batting": "Right hand",
      "Batting Avg": 11.23,
      "Batting S/R": 131.9,
      "Bowling": "Right arm pace",
      "Bowling S/R": 18.3,
      "Economy Rate": 8.7,
      "Runs": 393,
      "Wickets": 142
    },
    "Test": {
      "Batting": "Right hand",
      "Batting Avg": 11.23,
      "Batting S/R": 131.9,
      "Bowling": "Right arm pace",
      "Bowling S/R": 18.3,
      "Economy Rate": 8.7,
      "Runs": 393,
      "Wickets": 142
    }
  },
  "RS Second": {
    "ODI": null,
    "T20": {
      "Batting": "Right hand",
      "Batting Avg": 24.5,
      "Batting S/R": 111.2,
      "Bowling": "Right arm off break",
      "Bowling S/R": -1.0,
      "Economy Rate": -1.0,
      "Runs": 637,
      "Wickets": 0
    },
    "Test": {
      "Batting": "Right hand",
      "Batting Avg": 24.5,
      "Batting S/R": 111.2,
      "Bowling": "Right arm off break",
      "Bowling S/R": -1.0,
      "Economy Rate": -1.0,
      "Runs": 637,
      "Wickets": 0
    }
  },
  "Rashid Khan": {
    "ODI": {
      "Batting": "Right hand",
      "Batting Avg": 19.91,
      "Batting S/R": 107.6,
      "Bowling": -1,
      "Bowling S/R": 28.2,
      "Economy Rate": 4.2,
      "Runs": 1294,
      "Wickets": 184
    },
    "T20": {
      "Batting": "Right hand",
      "Batting Avg": 13.4,
      "Batting S/R": 144.8,
      "Bowling": -1,
      "Bowling S/R": 17.0,
      "Economy Rate": 6.5,
      "Runs": 2185,
      "Wickets": 578
    },
    "Test": {
      "Batting": "Right hand",
      "Batting Avg": 13.4,
      "Batting S/R": 144.8,
      "Bowling": -1,
      "Bowling S/R": 17.0,
      "Economy Rate": 6.5,
      "Runs": 2185,
      "Wickets": 578
    }
  },
  "SJ Erwee": {
    "ODI": null,
    "T20": {
      "Batting": "Left hand",
      "Batting Avg": 18.11,
      "Batting S/R": 124.4,
      "Bowling": "Right arm off break",
      "Bowling S/R": -1.0,
      "Economy Rate": -1.0,
      "Runs": 489,
      "Wickets": 0
    },
    "Test": {
      "Batting": "Left hand",
      "Batting Avg": 18.11,
      "Batting S/R": 124.4,
      "Bowling": "Right arm off break",
      "Bowling S/R": -1.0,
      "Economy Rate": -1.0,
      "Runs": 489,
      "Wickets": 0
    }
  },
  "VD Philander": {
    "ODI": {
      "Batting": "Right hand",
      "Batting Avg": 8.67,
      "Batting S/R": 60.0,
      "Bowling": "Right arm pace",
      "Bowling S/R": 28.7,
      "Economy Rate": 4.6,
      "Runs": 78,
      "Wickets": 35
    },
    "T20": {
      "Batting": "Right hand",
      "Batting Avg": 29.47,
      "Batting S/R": 156.0,
      "Bowling": "Right arm pace",
      "Bowling S/R": 28.5,
      "Economy Rate": 7.8,
      "Runs": 560,
      "Wickets": 33
    },
    "Test": {
      "Batting": "Right hand",
      "Batting Avg": 29.47,
      "Batting S/R": 156.0,
      "Bowling": "Right arm pace",
      "Bowling S/R": 28.5,
      "Economy Rate": 7.8,
      "Runs": 560,
      "Wickets": 33
    }
  }
}

const matchData = {
  "Durban Heat": [
      "SJ Erwee",
      "JA Morkel",
      "VD Philander",
      "KA Maharaj",
      "Rashid Khan",
      "KJ Abbott",
      "M de Lange"
  ],
  "Format": "T20",
  "Nelson Mandela Bay Giants": [
      "JT Smuts",
      "JJ Roy",
      "RS Second",
      "BM Duckett"
  ]
}

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

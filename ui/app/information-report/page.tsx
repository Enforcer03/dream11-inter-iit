"use client";

import React, { useEffect, useState } from "react";
import InfoReportPlayer from "../components/infoReportPlayer";
import PageTemplate from "../components/pageTemplate";
import Button from "../components/buttonComp";
import { useMatchData } from "../contexts/matchDataContext";
import { handleLLMTeam } from "../api/llmApi";
import ReactMarkdown from "react-markdown";

interface PlayerData {
  id: number;
  name: string;
  image: string;
}

function getPlayerImagePath(
  playerName: string,
  selectedPlayersTeamA: PlayerData[],
  selectedPlayersTeamB: PlayerData[]
): string {
  const nameParts = playerName.split(" ");
  const lastName = nameParts[nameParts.length - 1];
  const firstInitial = nameParts[0][0];
  const allPlayers = [...selectedPlayersTeamA, ...selectedPlayersTeamB];

  let matchingPlayer = allPlayers.find((player) => {
    const playerNameParts = player.name.split(" ");
    const playerLastName = playerNameParts[playerNameParts.length - 1];
    const playerFirstInitial = player.name[0];

    return playerLastName === lastName && playerFirstInitial === firstInitial;
  });

  if (!matchingPlayer) {
    matchingPlayer = allPlayers.find((player) => {
      const playerNameParts = player.name.split(" ");
      const playerLastName = playerNameParts[playerNameParts.length - 1];
      return playerLastName === lastName;
    });
  }

  return matchingPlayer ? matchingPlayer.image : "default_player_image_url";
}

const PeopleDisplay = () => {
  const { predictedTeam, selectedPlayersTeamA, selectedPlayersTeamB, playerStats } = useMatchData();

  const [loading, setLoading] = useState(false);
  const [instruction, setInstruction] = useState<string>("");
  const prevPage = "/playing11";

  useEffect(() => {
    const fetchInstructions = async () => {
      try {
        const response = await handleLLMTeam(predictedTeam, JSON.stringify(playerStats), "T20");
        setInstruction(response["team analysis"]);
        // setInstruction(
        //   "### Team Analysis: Optimal Combination of Players\n\n#### 1. Overall Team Balance and Composition\nThe team is well-balanced with a strong mix of batting and bowling skills. The average win percentage (38.73%) suggests a balanced approach to both offense and defense. The total combined experience of 1190 matches indicates a solid base of veteran players who can contribute effectively.\n\n#### 2. Batting Lineup Strength and Depth\n- **Batting Average**: The team has a good batting average, with players like SC Getkate (16.23) and GH Dockrell (22.52) providing a solid base.\n- **Strike Rate**: Players such as PR Stirling (141.7), KJ O'Brien (133.8), and SC Williams (126.3) offer high strike rates, which can be crucial in fantasy cricket.\n- **Consistency**: Players like MR Adair (24.9) and SC Getkate (19.9) have higher consistency scores, ensuring they perform reliably across different conditions.\n\n#### 3. Bowling Attack Variety and Effectiveness\n- **Bowling Types**: The team features a mix of right-arm pacers (KJ O'Brien, MR Adair, SC Getkate, GH Dockrell, SF Mire, KM Jarvis, TL Chatara, H Masakadza) and left-arm orthodox spinners (GH Dockrell, SC Williams).\n- **Economy Rate and Wickets**: Bowlers like GH Dockrell (7.4) and SC Williams (7.1) have low economy rates and decent wicket-taking abilities, contributing to a strong bowling attack.\n- **Wickets**: The combined total of 568 wickets from 1190 matches shows a high overall bowling quality.\n\n#### 4. Fielding Capabilities\n- **Catches**: The team boasts a robust fielding record with 252 catches (PR Stirling, KJ O'Brien, MR Adair, GH Dockrell, SC Williams, SF Mire, KM Jarvis, TL Chatara, H Masakadza) and 24 runouts, indicating strong defensive skills.\n- **Experience**: High experience levels (e.g., GH Dockrell with 167 games) contribute to better fielding coordination and positioning.\n\n#### 5. Experience and Win-Rate Contribution\n- **Experience**: The team has a combined experience of 1"
        // );
      } catch (error) {
        console.error(error);
        // console.error("There was an error fetching the instructions.");
      }
    };

    fetchInstructions();
  }, [playerStats, predictedTeam]);

  return (
    <div>
      <PageTemplate title="playing 11">
        <div className=" ml-2 -mt-20">
          <h1 className="text-3xl text-[#FFD700] font-bold tracking-wider">PLAYERS&apos; INFORMATION REPORT</h1>
        </div>
        <div className="flex m-4">
          {predictedTeam.map((player, index) => {
            const fullName = player.split(" ");
            const modifiedName = fullName
              .map((part) => {
                return part.length > 7 ? part[0] + "." : part;
              })
              .join(" ");

            return (
              <div key={index} className="m-3">
                <InfoReportPlayer
                  child1={
                    <img
                      src={getPlayerImagePath(player, selectedPlayersTeamA, selectedPlayersTeamB)}
                      alt="Player Image"
                      className="player-image"
                    />
                  }
                  child2={modifiedName}
                />
              </div>
            );
          })}
        </div>
        <div className="information-report-container overflow-y-scroll h-[25rem]">
          <ReactMarkdown>{instruction}</ReactMarkdown>
        </div>
      </PageTemplate>
      <div className="buttonCompDiv">
        <Button nextPage={prevPage}>BACK</Button>
        <Button downloadScreenshot={true}>SAVE</Button>
      </div>
    </div>
  );
};

export default PeopleDisplay;

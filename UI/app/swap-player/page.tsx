"use client";

import { useEffect, useState } from "react";
import { handleLLMTeam } from "../api/llmApi";
import { revaluateTeamSwap } from "../api/predictedSquad";
import ButtonComponent from "../components/buttonComp";
import PageTemplateWithoutTop from "../components/pageTemplateNoTop";
import PitchComponent from "../components/pitchPlayer";
import PlayerInformationSwap from "../components/playerInformationSwap";
import { useMatchData } from "../contexts/matchDataContext";
import { RevaluateTeamApiResponse } from "../types/modelApiResponse";
import { areStringArraysEqualIgnoreOrder } from "../utils/TeamCompare";
import BackButtonComponent from "../components/backButton";

// const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

export default function SwapPlayer() {
  const {
    predictedTeam,
    setPredictedTeam,
    playerStats,
    covMatrix,
    matchData,
    selectedPlayersTeamA,
    selectedPlayersTeamB,
    teamStats,
    setTeamStats,
    aggregateStats,
    instructionLLM,
    setInstructionLLM,
  } = useMatchData();

  const [selectedPlayer, setSelectedPlayer] = useState<number | null>(0);
  const [newTeamStats, setNewTeamStats] = useState<RevaluateTeamApiResponse | null>(null);
  const [hoverPlayer, setHoverPlayer] = useState<string | null>(null);

  const nextPage = "/final-playing11";

  async function handleTeamRevaluation(newPredictedTeam: string[], flag: boolean) {
    try {
      const response = await revaluateTeamSwap(covMatrix, JSON.stringify(playerStats), newPredictedTeam);
      if (flag) setTeamStats(response);
      else setNewTeamStats(response);
    } catch (error) {
      console.error(error);
    }
  }

  const hoverPlayerStats = hoverPlayer ? aggregateStats[hoverPlayer] : null;

  useEffect(() => {
    async function fetchInstructions() {
      try {
        if (predictedTeam.length === 0) return;

        if (areStringArraysEqualIgnoreOrder(predictedTeam, instructionLLM.team)) return;
        setInstructionLLM({ team: predictedTeam, instruction: "" });
        const response = await handleLLMTeam(predictedTeam, JSON.stringify(playerStats), "T20");
        // await delay(10000);

        setInstructionLLM({ team: predictedTeam, instruction: response["team analysis"] });
        // setInstructionLLM({
        //   team: predictedTeam,
        //   instruction:
        //     "### Team Analysis: Optimal Combination of Players\n\n#### 1. Overall Team Balance and Composition\nThe team is well-balanced with a strong mix of batting and bowling skills. The average win percentage (38.73%) suggests a balanced approach to both offense and defense. The total combined experience of 1190 matches indicates a solid base of veteran players who can contribute effectively.\n\n#### 2. Batting Lineup Strength and Depth\n- **Batting Average**: The team has a good batting average, with players like SC Getkate (16.23) and GH Dockrell (22.52) providing a solid base.\n- **Strike Rate**: Players such as PR Stirling (141.7), KJ O'Brien (133.8), and SC Williams (126.3) offer high strike rates, which can be crucial in fantasy cricket.\n- **Consistency**: Players like MR Adair (24.9) and SC Getkate (19.9) have higher consistency scores, ensuring they perform reliably across different conditions.\n\n#### 3. Bowling Attack Variety and Effectiveness\n- **Bowling Types**: The team features a mix of right-arm pacers (KJ O'Brien, MR Adair, SC Getkate, GH Dockrell, SF Mire, KM Jarvis, TL Chatara, H Masakadza) and left-arm orthodox spinners (GH Dockrell, SC Williams).\n- **Economy Rate and Wickets**: Bowlers like GH Dockrell (7.4) and SC Williams (7.1) have low economy rates and decent wicket-taking abilities, contributing to a strong bowling attack.\n- **Wickets**: The combined total of 568 wickets from 1190 matches shows a high overall bowling quality.\n\n#### 4. Fielding Capabilities\n- **Catches**: The team boasts a robust fielding record with 252 catches (PR Stirling, KJ O'Brien, MR Adair, GH Dockrell, SC Williams, SF Mire, KM Jarvis, TL Chatara, H Masakadza) and 24 runouts, indicating strong defensive skills.\n- **Experience**: High experience levels (e.g., GH Dockrell with 167 games) contribute to better fielding coordination and positioning.\n\n#### 5. Experience and Win-Rate Contribution\n- **Experience**: The team has a combined experience of 1",
        // });
      } catch (error) {
        console.error(error);
      }
    }

    fetchInstructions();
  }, [playerStats, predictedTeam, setInstructionLLM, instructionLLM]);
  return (
    <>
      <div>
        <PageTemplateWithoutTop>
          <div className="flex w-full">
            <div className="playerShortDetails -ml-16">
              <PlayerInformationSwap
                playerName={predictedTeam[selectedPlayer]}
                playerInfo={aggregateStats[predictedTeam[selectedPlayer]]}
                teamStats={teamStats}
                newTeamStats={newTeamStats}
                hoverPlayerStats={hoverPlayerStats}
                selectedPlayersTeamA={selectedPlayersTeamA}
                selectedPlayersTeamB={selectedPlayersTeamB}
                hoverPlayer={hoverPlayer}
              />
            </div>
            <PitchComponent
              selectedPlayer={selectedPlayer}
              setSelectedPlayer={setSelectedPlayer}
              predictedTeam={predictedTeam}
              setPredictedTeam={setPredictedTeam}
              matchData={matchData}
              selectedPlayersTeamA={selectedPlayersTeamA}
              selectedPlayersTeamB={selectedPlayersTeamB}
              handleTeamRevaluation={handleTeamRevaluation}
              setNewTeamStats={setNewTeamStats}
              setHoverPlayer={setHoverPlayer}
            />
          </div>
        </PageTemplateWithoutTop>
        <div className="buttonPlayerSelectionDiv">
          <ButtonComponent nextPage={nextPage}>Finalize</ButtonComponent>
          <BackButtonComponent>BACK</BackButtonComponent>
        </div>
      </div>
    </>
  );
}

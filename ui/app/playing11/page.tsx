"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { handleLLMTeam } from "../api/llmApi";
import { getPredicted11, revaluateTeamSwap } from "../api/predictedSquad";
import Button from "../components/buttonComp";
import DisplayBox from "../components/displayBox";
import LoadingScreen from "../components/loadingScreen";
import PageTemplate from "../components/pageTemplate";
import { PlayerStats, useMatchData } from "../contexts/matchDataContext";
import { PlayerInfo } from "../types/modelApiResponse";
import { areStringArraysEqualIgnoreOrder } from "../utils/TeamCompare";

// const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

function Playing11() {
  const {
    date,
    matchData,
    setCovMatrix,
    playerStats,
    setPlayerStats,
    predictedTeam,
    setPredictedTeam,
    selectedPlayersTeamA,
    selectedPlayersTeamB,
    setTeamStats,
    instructionLLM,
    setInstructionLLM,
    totalScore,
    setTotalScore,
  } = useMatchData();

  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();
  const prevPage = "/player-selection";
  const nextPage = "/swap-player";

  const handlePredictedScoreClick = () => {
    router.push("/information-report");
  };

  useEffect(() => {
    async function fetchInstructions() {
      try {
        if (predictedTeam.length === 0) return;

        if (areStringArraysEqualIgnoreOrder(predictedTeam, instructionLLM.team)) return;

        setInstructionLLM({
          team: predictedTeam,
          instruction: "",
        });
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

  useEffect(() => {
    async function handleFetchPredictedPlayers() {
      try {
        setIsLoading(true);
        const teams = Object.keys(matchData).filter((team) => team !== "Format" && !team.includes("Second_Squad"));
        const player_info: PlayerInfo = {
          [teams[0]]: selectedPlayersTeamA.map((player) => player.name),
          [teams[1]]: selectedPlayersTeamB.map((player) => player.name),
        };
        const response = await getPredicted11(date, matchData?.Format as "T20" | "Test" | "ODI", player_info);

        const player_stats: PlayerStats[] = JSON.parse(response.player_stats);

        let total_score = 0;

        for (let i = 0; i < player_stats.length; i++) {
          if (response.best_team.includes(player_stats[i].player)) {
            if (player_stats[i].mean_points > 0) total_score += player_stats[i].mean_points;
          }
        }

        setTotalScore(total_score);
        setPredictedTeam(response.best_team);
        setCovMatrix(response.cov_matrix);
        setPlayerStats(player_stats);

        const resp = await revaluateTeamSwap(response.cov_matrix, response.player_stats, response.best_team);
        setTeamStats(resp);
      } catch (error) {
        console.error(error);
      } finally {
        setIsLoading(false);
      }
    }
    handleFetchPredictedPlayers();
  }, [
    date,
    matchData,
    setCovMatrix,
    setPlayerStats,
    setPredictedTeam,
    selectedPlayersTeamA,
    selectedPlayersTeamB,
    setTeamStats,
    setTotalScore,
  ]);

  if (isLoading) {
    return <LoadingScreen />;
  }

  return (
    <div>
      <PageTemplate title="PLAYING 11" />
      <div className="displayBoxDivDiv">
        <button className="predictedScoreBtn" onClick={handlePredictedScoreClick}>
          PREDICTED TOTAL SCORE {totalScore.toFixed(2)}
        </button>
        <div className="displayBoxDiv">
          <DisplayBox
            predictedTeam={predictedTeam}
            playerStats={playerStats}
            selectedPlayersTeamA={selectedPlayersTeamA}
            selectedPlayersTeamB={selectedPlayersTeamB}
          />
        </div>
      </div>
      <div className="buttonCompDiv">
        <Button nextPage={prevPage}>BACK</Button>
        <Button nextPage={nextPage}>SWAP</Button>
      </div>
    </div>
  );
}

export default Playing11;

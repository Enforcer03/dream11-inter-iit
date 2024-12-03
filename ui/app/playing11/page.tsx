"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { getPredicted11, revaluateTeamSwap } from "../api/predictedSquad";
import Button from "../components/buttonComp";
import DisplayBox from "../components/displayBox";
import LoadingScreen from "../components/loadingScreen";
import PageTemplate from "../components/pageTemplate";
import { PlayerStats, useMatchData } from "../contexts/matchDataContext";
import { PlayerInfo } from "../types/modelApiResponse";

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
  } = useMatchData();

  const [totalScore, setTotalScore] = useState(0);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();
  const prevPage = "/player-selection";
  const nextPage = "/swap-player";

  const handlePredictedScoreClick = () => {
    router.push("/information-report");
  };

  useEffect(() => {
    async function handleFetchPredictedPlayers() {
      try {
        setIsLoading(true);
        const teams = Object.keys(matchData).filter((team) => team != "Format");
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

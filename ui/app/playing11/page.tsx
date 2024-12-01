"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { getPredicted11 } from "../api/predictedSquad";
import Button from "../components/buttonComp";
import DisplayBox from "../components/displayBox";
import PageTemplate from "../components/pageTemplate";
import { PlayerStats, useMatchData } from "../contexts/matchDataContext";

function Playing11() {
  const { date, matchData, setCovMatrix, playerStats, setPlayerStats, predictedTeam, setPredictedTeam } =
    useMatchData();

  const [totalScore, setTotalScore] = useState(0);
  const router = useRouter();
  const prevPage = "/player-selection";

  const handlePredictedScoreClick = () => {
    router.push("/information-report");
  };

  useEffect(() => {
    async function handleFetchPredictedPlayers() {
      try {
        const response = await getPredicted11(date, matchData?.Format as "T20" | "Test" | "ODI");
        const player_stats: PlayerStats[] = JSON.parse(response.player_stats);

        let total_score = 0;

        for (let i = 0; i < player_stats.length; i++) {
          if (player_stats[i].player in response.best_team) {
            total_score += player_stats[i].mean_points;
          }
        }

        setTotalScore(total_score);

        setPredictedTeam(response.best_team);
        setCovMatrix(response.cov_matrix);
        setPlayerStats(player_stats);
      } catch (error) {
        console.error(error);
      }
    }
    handleFetchPredictedPlayers();
  }, [date, matchData, setCovMatrix, setPlayerStats, setPredictedTeam]);

  return (
    <div>
      <PageTemplate title="PLAYING 11" />
      <div className="displayBoxDivDiv">
        <button className="predictedScoreBtn" onClick={handlePredictedScoreClick}>
          PREDICTED TOTAL SCORE {totalScore}
        </button>
        <div className="displayBoxDiv">
          <DisplayBox predictedTeam={predictedTeam} playerStats={playerStats} />
        </div>
      </div>
      <div className="buttonCompDiv">
        <Button nextPage={prevPage}>BACK</Button>
        <Button downloadScreenshot={true}>SAVE</Button>
      </div>
    </div>
  );
}

export default Playing11;

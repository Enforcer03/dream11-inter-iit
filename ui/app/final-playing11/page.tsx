"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import Button from "../components/buttonComp";
import DisplayBox from "../components/displayBox";
import PageTemplate from "../components/pageTemplate";
import { useMatchData } from "../contexts/matchDataContext";

function FinalPlaying11() {
  const { playerStats, predictedTeam, selectedPlayersTeamA, selectedPlayersTeamB } = useMatchData();

  const [totalScore, setTotalScore] = useState(0);
  const router = useRouter();
  const prevPage = "/player-selection";

  const handlePredictedScoreClick = () => {
    router.push("/information-report");
  };

  useEffect(() => {
    let total_score = 0;

    for (let i = 0; i < playerStats.length; i++) {
      if (predictedTeam.includes(playerStats[i].player)) {
        if (playerStats[i].mean_points > 0) total_score += playerStats[i].mean_points;
      }
    }
    setTotalScore(total_score);
  }, [playerStats, predictedTeam]);

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
        <Button downloadScreenshot={true}>SAVE</Button>
      </div>
    </div>
  );
}

export default FinalPlaying11;

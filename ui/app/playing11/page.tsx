"use client"

import { useRouter } from 'next/navigation';
import Button from "../components/buttonComp";
import DisplayBox from "../components/displayBox";
import PageTemplate from "../components/pageTemplate";

function Playing11() {
  const router = useRouter();
  const prevPage = "/player-selection";

  const handlePredictedScoreClick = () => {
    router.push('/information-report');
  };

  return (
    <div>
      <PageTemplate title="PLAYING 11" />
      <div className="displayBoxDivDiv">
        <button
          className="predictedScoreBtn"
          onClick={handlePredictedScoreClick}
        >
          PREDICTED TOTAL SCORE 195
        </button>
        <div className="displayBoxDiv">
          <DisplayBox />
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

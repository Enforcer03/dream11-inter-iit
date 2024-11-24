import AudioComp from "../components/audioSet";
import Button from "../components/buttonComp";
import InstructionSet from "../components/instructionSet";
import PageTemplate from "../components/pageTemplate";
import VideoComp from "../components/videoSet";

function InstructionsPage() {
  return (
    <div className="">
      <PageTemplate title="instructions" />
      <div className="instructionsDiv">
        <InstructionSet />
      </div>
      <div className="buttonCompDiv">
        <Button>BACK</Button>
        <Button>NEXT</Button>
      </div>
      <div className="videoCompDiv">
        <VideoComp>VIDEO DEMO</VideoComp>
      </div>
      <div className="audioCompDiv">
        <AudioComp />
      </div>
    </div>
  );
}

export default InstructionsPage;

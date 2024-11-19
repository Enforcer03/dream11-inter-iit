import PageTemplate from "../components/pageTemplate";
import Button from "../components/buttonComp";
import TopButton from "../components/topButtonComp";
import InstructionSet from "../components/instructionSet";
import VideoComp from "../components/videoSet";
import AudioComp from "../components/audioSet";

function InstructionsPage() {
  return (
    <div className="">
      <div className="topButtonCompDiv">
        <TopButton children={"INSTRUCTIONS"} />
      </div>
      <PageTemplate />
      <div className="instructionsDiv">
        <InstructionSet />
      </div>
      <div className="buttonCompDiv">
        <Button children={"BACK"} />
        <Button children={"NEXT"} />
      </div>
      <div className="videoCompDiv">
        <VideoComp children={"VIDEO DEMO"} />
      </div>
      <div className="audioCompDiv">
        <AudioComp />
      </div>
    </div>
  );
}

export default InstructionsPage;

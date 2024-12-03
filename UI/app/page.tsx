import AudioComp from "./components/audioSet";
import InstructionSet from "./components/instructionSet";
import Button from "./components/nextBtn";
import PageTemplate from "./components/pageTemplate";
import VideoComp from "./components/videoSet";

function InstructionsPage() {
  const nextPage = "/select-match";

  return (
    <div>
      <PageTemplate title="instructions">
        <InstructionSet />
      </PageTemplate>
      <div className="buttonCompDiv">
        <Button nextPage={nextPage}>NEXT</Button>
      </div>
      <div className="videoCompDiv">
        <VideoComp nextPage="/video-instructions">
          VIDEO <span className="text-white">DEMO</span>
        </VideoComp>
      </div>
      <div className="audioCompDiv">
        <AudioComp />
      </div>
    </div>
  );
}

export default InstructionsPage;

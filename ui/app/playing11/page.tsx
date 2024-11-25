import Button from "../components/buttonComp";
import DisplayBox from "../components/displayBox";
import PageTemplate from "../components/pageTemplate";

function Playing11() {
  return (
    <div>
      <PageTemplate title="PLAYING 11"/>
      <div className="displayBoxDiv">
        <DisplayBox />
      </div>
      <div className="buttonCompDiv">
        <Button>BACK</Button>
        <Button>NEXT</Button>
      </div>
    </div>
  );
}

export default Playing11;

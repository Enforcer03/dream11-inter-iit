import Button from "../components/buttonComp";
import DisplayBox from "../components/displayBox";
import PageTemplate from "../components/pageTemplate";
import TopButton from "../components/topButtonComp";

function Playing11() {
  return (
    <div className="">
      <div className="topButtonCompDiv">
        <TopButton>PLAYING 11</TopButton>
      </div>
      <PageTemplate />
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

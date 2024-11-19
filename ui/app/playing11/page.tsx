import PageTemplate from "../components/pageTemplate";
import Button from "../components/buttonComp";
import TopButton from "../components/topButtonComp";
import DisplayBox from "../components/displayBox";

function Playing11() {
  return (
    <div className="">
      <div className="topButtonCompDiv">
        <TopButton children={"PLAYING 11"} />
      </div>
      <PageTemplate />
      <div className="displayBoxDiv">
        <DisplayBox />
      </div>
      <div className="buttonCompDiv">
        <Button children={"BACK"} />
        <Button children={"NEXT"} />
      </div>
    </div>
  );
}

export default Playing11;

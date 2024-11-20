import PageTemplate from "../components/pageTemplate";
import Button from "../components/buttonComp";
import PlayersSelect from "../components/playersSelect";

function InstructionsPage() {
  return (
    <div className="">
      <PageTemplate />
      <PlayersSelect />
      <div className="buttonPlayerSelectionDiv">
        <Button children={"NEXT"} />
        <Button children={"BACK"} />
      </div>
    </div>
  );
}

export default InstructionsPage;

import Button from "../components/buttonComp";
import PageTemplate from "../components/pageTemplate";
import PlayersSelect from "../components/playersSelect";

function InstructionsPage() {
  return (
    <div className="">
      <PageTemplate />
      <PlayersSelect />
      <div className="buttonPlayerSelectionDiv">
        <Button>NEXT</Button>
        <Button>BACK</Button>
      </div>
    </div>
  );
}

export default InstructionsPage;

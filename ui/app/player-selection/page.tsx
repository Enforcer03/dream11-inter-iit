import Button from "../components/buttonComp";
import PageTemplateNoTop from "../components/pageTemplateNoTop";
import PlayersSelect from "../components/playersSelect";

function InstructionsPage() {
  return (
    <div className="">
      <PageTemplateNoTop />
      <PlayersSelect />
      <div className="buttonPlayerSelectionDiv">
        <Button>NEXT</Button>
        <Button>BACK</Button>
      </div>
    </div>
  );
}

export default InstructionsPage;

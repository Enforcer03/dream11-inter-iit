import Button from "../components/buttonComp";
import PageTemplateNoTop from "../components/pageTemplateNoTop";
import PlayersSelect from "../components/playersSelect";

function InstructionsPage() {
  const prevPage = "/select-match";
  const nextPage = "/playing11";

  return (
    <div className="">
      <PageTemplateNoTop />
      <PlayersSelect />
      <div className="buttonPlayerSelectionDiv">
        <Button nextPage={nextPage}>NEXT</Button>
        <Button nextPage={prevPage}>BACK</Button>
      </div>
    </div>
  );
}

export default InstructionsPage;

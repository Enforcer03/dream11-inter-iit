import PageTemplateWithoutTop from "../components/pageTemplateWithoutTop";
import PlayerInformation from "../components/playerInformation";

export default function SwapPlayer() {
  return (
    <PageTemplateWithoutTop>
      <div className="flex w-full">
        <div className="basis-1/4">
          <PlayerInformation title="swap player" />
        </div>
        <div className="flex flex-col w-16 basis-3/4">
          <div className="pitch w-full basis-4/6"></div>
          <div className="basis-2/6"></div>
        </div>
      </div>
    </PageTemplateWithoutTop>
  );
}

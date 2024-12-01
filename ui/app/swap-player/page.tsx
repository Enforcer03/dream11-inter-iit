"use client";

import { useEffect, useState } from "react";
import ButtonComponent from "../components/buttonComp";
import PageTemplateWithoutTop from "../components/pageTemplateNoTop";
import PitchComponent from "../components/pitchPlayer";
import PlayerInformation from "../components/playerInformation";
import playersData from "../../public/players.json";
import playerJsonTest from "../../public/playerJsonTest.json";

export default function SwapPlayer() {
  const [selectedPlayer, setSelectedPlayer] = useState(playerJsonTest[0]);
  const [hoveredPlayer, setHoveredPlayer] = useState(null);
  const [finalPlayers, setFinalPlayers] = useState([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);

  useEffect(() => {}, []);
  return (
    <>
      <div>
        <PageTemplateWithoutTop>
          <div className="flex w-full">
            <div className="playerShortDetails -ml-16">
              <PlayerInformation 
                title="Swap Player" 
                selectedPlayer={selectedPlayer} 
                hoveredPlayer={hoveredPlayer} />
            </div>
            <PitchComponent
              setFinalPlayers={setFinalPlayers}
              finalPlayers={finalPlayers}
              selectedPlayer={selectedPlayer}
              setSelectedPlayer={setSelectedPlayer}
              setHoveredPlayer={setHoveredPlayer}
            />
          </div>
        </PageTemplateWithoutTop>
        <div className="buttonPlayerSelectionDiv">
          <ButtonComponent>Finalize</ButtonComponent>
          <ButtonComponent>BACK</ButtonComponent>
        </div>
      </div>
    </>
  );
}

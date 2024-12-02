"use client";

import { useState } from "react";
import ButtonComponent from "../components/buttonComp";
import PageTemplateWithoutTop from "../components/pageTemplateNoTop";
import PitchComponent from "../components/pitchPlayer";
import PlayerInformation from "../components/playerInformation";
import { useMatchData } from "../contexts/matchDataContext";
import { revaluateTeamSwap } from "../api/predictedSquad";

export default function SwapPlayer() {
  const {
    predictedTeam,
    setPredictedTeam,
    playerStats,
    covMatrix,
    matchData,
    selectedPlayersTeamA,
    selectedPlayersTeamB,
  } = useMatchData();

  const [selectedPlayer, setSelectedPlayer] = useState<number | null>(0);
  const [hoveredPlayer, setHoveredPlayer] = useState<number | null>(null);

  async function handleTeamRevaluation() {
    try {
      const response = await revaluateTeamSwap(covMatrix, JSON.stringify(playerStats), predictedTeam);
    } catch (error) {
      console.error(error);
    }
  }
  console.log("SwapPlayer");
  console.log(predictedTeam);
  return (
    <>
      <div>
        <PageTemplateWithoutTop>
          <div className="flex w-full">
            <div className="playerShortDetails -ml-16">
              <PlayerInformation title="Swap Player" selectedPlayer={selectedPlayer} hoveredPlayer={hoveredPlayer} />
            </div>
            <PitchComponent
              selectedPlayer={selectedPlayer}
              setSelectedPlayer={setSelectedPlayer}
              setHoveredPlayer={setHoveredPlayer}
              predictedTeam={predictedTeam}
              setPredictedTeam={setPredictedTeam}
              matchData={matchData}
              selectedPlayersTeamA={selectedPlayersTeamA}
              selectedPlayersTeamB={selectedPlayersTeamB}
              handleTeamRevaluation={handleTeamRevaluation}
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

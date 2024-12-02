"use client";

import { useState } from "react";
import { revaluateTeamSwap } from "../api/predictedSquad";
import ButtonComponent from "../components/buttonComp";
import PageTemplateWithoutTop from "../components/pageTemplateNoTop";
import PitchComponent from "../components/pitchPlayer";
import PlayerInformationSwap from "../components/playerInformationSwap";
import { useMatchData } from "../contexts/matchDataContext";
import { RevaluateTeamApiResponse } from "../types/modelApiResponse";

export default function SwapPlayer() {
  const {
    predictedTeam,
    setPredictedTeam,
    playerStats,
    covMatrix,
    matchData,
    selectedPlayersTeamA,
    selectedPlayersTeamB,
    teamStats,
    setTeamStats,
    aggregateStats,
  } = useMatchData();

  const [selectedPlayer, setSelectedPlayer] = useState<number | null>(0);
  const [newTeamStats, setNewTeamStats] = useState<RevaluateTeamApiResponse | null>(null);
  const [hoverPlayer, setHoverPlayer] = useState<string | null>(null);

  const prevPage = "/playing11";
  const nextPage = "/final-playing11";

  async function handleTeamRevaluation(newPredictedTeam: string[], flag: boolean) {
    try {
      const response = await revaluateTeamSwap(covMatrix, JSON.stringify(playerStats), newPredictedTeam);
      if (flag) setTeamStats(response);
      else setNewTeamStats(response);
    } catch (error) {
      console.error(error);
    }
  }

  const hoverPlayerStats = hoverPlayer ? aggregateStats[hoverPlayer] : null;

  return (
    <>
      <div>
        <PageTemplateWithoutTop>
          <div className="flex w-full">
            <div className="playerShortDetails -ml-16">
              <PlayerInformationSwap
                playerName={predictedTeam[selectedPlayer]}
                playerInfo={aggregateStats[predictedTeam[selectedPlayer]]}
                teamStats={teamStats}
                newTeamStats={newTeamStats}
                hoverPlayerStats={hoverPlayerStats}
                selectedPlayersTeamA={selectedPlayersTeamA}
                selectedPlayersTeamB={selectedPlayersTeamB}
              />
            </div>
            <PitchComponent
              selectedPlayer={selectedPlayer}
              setSelectedPlayer={setSelectedPlayer}
              predictedTeam={predictedTeam}
              setPredictedTeam={setPredictedTeam}
              matchData={matchData}
              selectedPlayersTeamA={selectedPlayersTeamA}
              selectedPlayersTeamB={selectedPlayersTeamB}
              handleTeamRevaluation={handleTeamRevaluation}
              setNewTeamStats={setNewTeamStats}
              setHoverPlayer={setHoverPlayer}
            />
          </div>
        </PageTemplateWithoutTop>
        <div className="buttonPlayerSelectionDiv">
          <ButtonComponent nextPage={nextPage}>Finalize</ButtonComponent>
          <ButtonComponent nextPage={prevPage}>BACK</ButtonComponent>
        </div>
      </div>
    </>
  );
}

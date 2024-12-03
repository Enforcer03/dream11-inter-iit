"use client";

import Image from "next/image";
import React from "react";
import { AggregateStats } from "../types/aggregateApiResponse";
import { RevaluateTeamApiResponse } from "../types/modelApiResponse";
import { useMatchData } from "../contexts/matchDataContext";

interface PlayerInformationSwapProps {
  playerName: string;
  playerInfo?: AggregateStats;
  teamStats?: RevaluateTeamApiResponse;
  newTeamStats?: RevaluateTeamApiResponse | null;
  hoverPlayerStats: AggregateStats | null;
  selectedPlayersTeamA?: string[];
  selectedPlayersTeamB?: string[];
  hoverPlayer: string;
}

interface PlayerData {
  id: number;
  name: string;
  image: string;
}

function getPlayerImagePath(
  playerName: string,
  selectedPlayersTeamA: PlayerData[],
  selectedPlayersTeamB: PlayerData[]
): string {
  const nameParts = playerName.split(" ");
  const lastName = nameParts[nameParts.length - 1];
  const firstInitial = nameParts[0][0];
  const allPlayers = [...selectedPlayersTeamA, ...selectedPlayersTeamB];

  let matchingPlayer = allPlayers.find((player) => {
    const playerNameParts = player.name.split(" ");
    const playerLastName = playerNameParts[playerNameParts.length - 1];
    const playerFirstInitial = player.name[0];

    return playerLastName === lastName && playerFirstInitial === firstInitial;
  });

  if (!matchingPlayer) {
    matchingPlayer = allPlayers.find((player) => {
      const playerNameParts = player.name.split(" ");
      const playerLastName = playerNameParts[playerNameParts.length - 1];
      return playerLastName === lastName;
    });
  }

  return matchingPlayer ? matchingPlayer.image : "default_player_image_url";
}

function PlayerInformationSwap({
  playerName,
  playerInfo,
  teamStats,
  newTeamStats,
  hoverPlayerStats,
  selectedPlayersTeamA,
  selectedPlayersTeamB,
  hoverPlayer,
}: PlayerInformationSwapProps) {
  const { totalScore, setTotalScore, playerStats } = useMatchData();

  const formatName = (name: string) => {
    if (name.length > 13) {
      const words = name.split(" ");
      if (words.length > 1) {
        const initial = words[0][0] + ".";
        return initial + " " + words.slice(1).join(" ");
      }
    }
    return name;
  };

  let newConsistencyScorePercent = 0,
    newDiversityScorePercent = 0,
    newFormScorePercent = 0;

  if (newTeamStats && teamStats) {
    newConsistencyScorePercent =
      ((newTeamStats.team_consistency_score - teamStats.team_consistency_score) * 100) /
      teamStats?.team_consistency_score;

    newDiversityScorePercent =
      ((Math.pow(newTeamStats.team_diversity_score, 1) - Math.pow(teamStats.team_diversity_score, 1)) * 100) /
      Math.pow(teamStats?.team_diversity_score, 1);

    newFormScorePercent = ((newTeamStats.form_score - teamStats.form_score) * 100) / teamStats?.form_score;

    newConsistencyScorePercent = newConsistencyScorePercent.toFixed(2);
    newDiversityScorePercent = newDiversityScorePercent.toFixed(2);
    newFormScorePercent = newFormScorePercent.toFixed(2);
  }

  let runsDiff = 0,
    battingSRDiff = 0,
    bowlingSRDiff = 0,
    economyRateDiff = 0,
    totalScoreDiff = 0;

  if (hoverPlayerStats) {
    runsDiff = hoverPlayerStats.Runs - playerInfo?.Runs;
    battingSRDiff = hoverPlayerStats["Batting S/R"] - playerInfo?.["Batting S/R"];
    bowlingSRDiff = hoverPlayerStats["Bowling S/R"] - playerInfo?.["Bowling S/R"];
    economyRateDiff = hoverPlayerStats["Economy Rate"] - playerInfo?.["Economy Rate"];

    let totalScoreHoverPlayer = 0;
    let totalScoreSelectedPlayer = 0;

    for (let i = 0; i < playerStats.length; i++) {
      if (playerStats[i].player === hoverPlayer) {
        totalScoreHoverPlayer = playerStats[i].mean_points;
      }
      if (playerStats[i].player === playerName) {
        totalScoreSelectedPlayer = playerStats[i].mean_points;
      }
    }

    totalScoreDiff = totalScoreHoverPlayer - totalScoreSelectedPlayer;

    runsDiff = runsDiff.toFixed(0);
    battingSRDiff = battingSRDiff.toFixed(1);
    bowlingSRDiff = bowlingSRDiff.toFixed(1);
    economyRateDiff = economyRateDiff.toFixed(1);
    totalScoreDiff = totalScoreDiff.toFixed(2);
  }

  return (
    <div className="flex flex-col justify-center items-center uppercase w-[21rem] h-full">
      <h1 className="uppercase text-dream11FontColor font-bold text-3xl mb-4 ">Swap Player</h1>
      <div className="rounded-full border-2 profilePhoto w-44 h-44 mb-8 flex items-center justify-center">
        <Image
          src={getPlayerImagePath(playerName, selectedPlayersTeamA, selectedPlayersTeamB)}
          alt="player"
          height={180}
          width={180}
        />
      </div>
      <div className="flex align-center justify-center">
        <div className="text-left flex flex-col">
          <div className="flex flex-col w-[25rem] ml-24">
            <div className="flex text-dream11FontColor">
              <div className="font-bold w-2/6">Name:</div>
            </div>
            <div className="flex mb-2 text-white">
              <div className="w-2/6">{formatName(playerName)}</div>
            </div>
            <div className="flex text-dream11FontColor">
              <div className="font-bold w-2/6">Batting S/R:</div>
              <div className="font-bold w-4/6">Team Consistency Score:</div>
            </div>
            <div className="flex mb-2 text-white">
              <div className="w-2/6">
                <span>
                  {playerInfo?.["Batting S/R"] < 0 || playerInfo?.["Batting S/R"] === "Infinity"
                    ? "-"
                    : playerInfo?.["Batting S/R"]}
                </span>
                {playerInfo?.["Batting S/R"] < 0 || playerInfo?.["Batting S/R"] === "Infinity" ? null : (
                  <span className={`${battingSRDiff > 0 ? "text-green-500" : "text-red-500"} ml-4`}>
                    {hoverPlayerStats
                      ? battingSRDiff > 0
                        ? `${battingSRDiff} ${String.fromCharCode(8593)}`
                        : `${battingSRDiff * -1} ${String.fromCharCode(8595)}`
                      : null}
                  </span>
                )}
              </div>
              <div className="w-4/6">
                <span className={`${newConsistencyScorePercent < 0 ? "text-red-500" : "text-green-500"}`}>
                  {newTeamStats ? (
                    newConsistencyScorePercent < 0 ? (
                      `${newConsistencyScorePercent * -1}% ${String.fromCharCode(8595)}`
                    ) : (
                      `${newConsistencyScorePercent}% ${String.fromCharCode(8593)}`
                    )
                  ) : (
                    <span className="text-gray-500">HOVER TO VIEW</span>
                  )}
                </span>
              </div>
            </div>
            <div className="flex text-dream11FontColor">
              <div className="font-bold w-2/6">Bowling S/R:</div>
              <div className="font-bold w-4/6">Team Diversity Score:</div>
            </div>
            <div className="flex mb-2 text-white">
              <div className="w-2/6">
                <span>
                  {playerInfo?.["Bowling S/R"] < 0 || playerInfo?.["Bowling S/R"] === "Infinity"
                    ? "-"
                    : playerInfo?.["Bowling S/R"]}
                </span>
                {playerInfo?.["Bowling S/R"] < 0 || playerInfo?.["Bowling S/R"] === "Infinity" ? null : (
                  <span className={`${bowlingSRDiff > 0 ? "text-green-500" : "text-red-500"} ml-4`}>
                    {hoverPlayerStats
                      ? bowlingSRDiff > 0
                        ? `${bowlingSRDiff} ${String.fromCharCode(8593)}`
                        : `${bowlingSRDiff * -1} ${String.fromCharCode(8595)}`
                      : null}
                  </span>
                )}
              </div>
              <div className="w-4/6">
                <span className={`${newDiversityScorePercent < 0 ? "text-red-500" : "text-green-500"}`}>
                  {newTeamStats ? (
                    newDiversityScorePercent < 0 ? (
                      `${newDiversityScorePercent * -1}% ${String.fromCharCode(8595)}`
                    ) : (
                      `${newDiversityScorePercent}% ${String.fromCharCode(8593)}`
                    )
                  ) : (
                    <span className="text-gray-500">HOVER TO VIEW</span>
                  )}
                </span>
              </div>
            </div>
            <div className="flex text-dream11FontColor">
              <div className="font-bold w-2/6">Economy Rate:</div>
              <div className="font-bold w-4/6">Team Form Score:</div>
            </div>
            <div className="flex text-white">
              <div className="w-2/6">
                <span>
                  {playerInfo?.["Economy Rate"] < 0 || playerInfo?.["Economy Rate"] === "Infinity"
                    ? "-"
                    : playerInfo?.["Economy Rate"]}
                </span>
                {playerInfo?.["Economy Rate"] < 0 || playerInfo?.["Economy Rate"] === "Infinity" ? null : (
                  <span className={`${economyRateDiff > 0 ? "text-green-500" : "text-red-500"} ml-4`}>
                    {hoverPlayerStats
                      ? economyRateDiff > 0
                        ? `${economyRateDiff} ${String.fromCharCode(8593)}`
                        : `${economyRateDiff * -1} ${String.fromCharCode(8595)}`
                      : null}
                  </span>
                )}
              </div>
              <div className="w-4/6">
                <span className={`${newFormScorePercent < 0 ? "text-red-500" : "text-green-500"}`}>
                  {newTeamStats ? (
                    newFormScorePercent < 0 ? (
                      `${newFormScorePercent * -1}% ${String.fromCharCode(8595)}`
                    ) : (
                      `${newFormScorePercent}% ${String.fromCharCode(8593)}`
                    )
                  ) : (
                    <span className="text-gray-500">HOVER TO VIEW</span>
                  )}
                </span>
              </div>
            </div>
            <div className="flex text-dream11FontColor">
              <div className="font-bold w-2/6">Runs:</div>
              <div className="font-bold w-4/6">Team Team Score:</div>
            </div>
            <div className="flex text-white">
              <div className="w-2/6">
                <span>{playerInfo?.Runs < 0 || playerInfo?.Runs === "Infinity" ? "-" : playerInfo?.Runs}</span>
                {playerInfo?.Runs < 0 || playerInfo?.Runs === "Infinity" ? null : (
                  <span className={`${runsDiff > 0 ? "text-green-500" : "text-red-500"} ml-4`}>
                    {hoverPlayerStats
                      ? runsDiff > 0
                        ? `${runsDiff} ${String.fromCharCode(8593)}`
                        : `${runsDiff * -1} ${String.fromCharCode(8595)}`
                      : null}
                  </span>
                )}
              </div>
              <div className="w-4/6">
                <span>{totalScore.toFixed(2)}</span>
                <span className={`${totalScoreDiff > 0 ? "text-green-500" : "text-red-500"} ml-4`}>
                  {hoverPlayerStats
                    ? totalScoreDiff > 0
                      ? `${totalScoreDiff} ${String.fromCharCode(8593)}`
                      : `${totalScoreDiff * -1} ${String.fromCharCode(8595)}`
                    : null}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default PlayerInformationSwap;

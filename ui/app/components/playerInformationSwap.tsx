"use client";

import Image from "next/image";
import React from "react";
import { AggregateStats } from "../types/aggregateApiResponse";
import { RevaluateTeamApiResponse } from "../types/modelApiResponse";

interface PlayerInformationSwapProps {
  playerName: string;
  playerInfo?: AggregateStats;
  teamStats?: RevaluateTeamApiResponse;
  newTeamStats?: RevaluateTeamApiResponse | null;
  child3?: string;
  child4?: string;
}

function PlayerInformationSwap({
  playerName,
  playerInfo,
  teamStats,
  newTeamStats,
  child3,
  child4,
}: PlayerInformationSwapProps) {
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
      ((newTeamStats.team_diversity_score - teamStats.team_diversity_score) * 100) / teamStats?.team_diversity_score;
    newFormScorePercent = ((newTeamStats.form_score - teamStats.form_score) * 100) / teamStats?.form_score;
  }

  return (
    <div className="flex flex-col justify-center items-center uppercase w-[21rem] h-full">
      <h1 className="uppercase text-dream11FontColor font-bold text-3xl mb-4 ">Swap Player</h1>
      <div className="rounded-full border-2 profilePhoto w-44 h-44 mb-8 flex items-center justify-center">
        <Image src={child3} alt="player" height={180} width={180} />
      </div>
      <div className="flex align-center justify-center">
        <div className="text-left flex flex-col">
          <div className="flex justify-center mb-4">
            <Image src={child4} alt="player" width={60} height={50} />
          </div>
          <div className="flex flex-col w-[21rem] ml-24">
            <div className="flex text-dream11FontColor">
              <div className="font-bold w-1/2">Name:</div>
              <div className="font-bold">Runs</div>
            </div>
            <div className="flex mb-2 text-white">
              <div className="w-1/2">{formatName(playerName)}</div>
              <div className="w-1/2">
                {playerInfo?.Runs < 0 || playerInfo?.Runs === "Infinity" ? "-" : playerInfo?.Runs}
              </div>
            </div>
            <div className="flex text-dream11FontColor">
              <div className="font-bold w-1/2">Batting S/R:</div>
              <div className="font-bold w-1/2">Team Consistency Score:</div>
            </div>
            <div className="flex mb-2 text-white">
              <div className="w-1/2">
                {playerInfo?.["Batting S/R"] < 0 || playerInfo?.["Batting S/R"] === "Infinity"
                  ? "-"
                  : playerInfo?.["Batting S/R"]}
              </div>
              <div className="w-1/2">
                {newTeamStats
                  ? newConsistencyScorePercent < 0
                    ? `${(newConsistencyScorePercent * -1).toFixed(1)}% ${String.fromCharCode(8593)}`
                    : `${newConsistencyScorePercent.toFixed(1)}% ${String.fromCharCode(8595)}`
                  : null}
              </div>
            </div>
            <div className="flex text-dream11FontColor">
              <div className="font-bold w-1/2">Bowling S/R:</div>
              <div className="font-bold w-1/2">Team Diversity Score:</div>
            </div>
            <div className="flex mb-2 text-white">
              <div className="w-1/2">
                {playerInfo?.["Bowling S/R"] < 0 || playerInfo?.["Bowling S/R"] === "Infinity"
                  ? "-"
                  : playerInfo?.["Bowling S/R"]}
              </div>
              <div className="w-1/2">
                {newTeamStats
                  ? newDiversityScorePercent < 0
                    ? `${(newDiversityScorePercent * -1).toFixed(1)}% ${String.fromCharCode(8593)}`
                    : `${newDiversityScorePercent.toFixed(1)}% ${String.fromCharCode(8595)}`
                  : null}
              </div>
            </div>
            <div className="flex text-dream11FontColor">
              <div className="font-bold w-1/2">Economy Rate:</div>
              <div className="font-bold w-1/2">Team Form Score:</div>
            </div>
            <div className="flex text-white">
              <div className="w-1/2">
                {playerInfo?.["Economy Rate"] < 0 || playerInfo?.["Economy Rate"] === "Infinity"
                  ? "-"
                  : playerInfo?.["Economy Rate"]}
              </div>
              <div className="w-1/2">
                {newTeamStats
                  ? newFormScorePercent < 0
                    ? `${(newFormScorePercent * -1).toFixed(1)}% ${String.fromCharCode(8593)}`
                    : `${newFormScorePercent.toFixed(1)}% ${String.fromCharCode(8595)}`
                  : null}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default PlayerInformationSwap;

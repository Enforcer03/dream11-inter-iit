"use client";

import { useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import { handleLLMPlayer } from "../api/llmApi";
import ButtonComponent from "../components/buttonComp";
import PageTemplate from "../components/pageTemplate";
import PlayerInformation from "../components/playerInformation";
import { useMatchData } from "../contexts/matchDataContext";

export default function SwapPlayer() {
  const { aggregateStats, matchData } = useMatchData();
  const [playerLLMInfo, setPlayerLLMInfo] = useState<JSX.Element[]>([]);

  const { predictedTeam } = useMatchData();
  const searchParams = useSearchParams();
  const id = searchParams.get("id");
  const image = searchParams.get("image");

  const prevPage = "/playing11";
  const nextPage = "/swap-player";

  const format = matchData?.Format;
  console.log(aggregateStats[id]?.["Batting S/R"]);

  useEffect(() => {
    async function handleLLMForPlayers() {
      try {
        // const playerName = predictedTeam[id];
        const res = await handleLLMPlayer(format, id, predictedTeam);
        console.log("LLM Response: ", res);
        setPlayerLLMInfo(res.analysis);

        console.log("LLM Response: ", res);
      } catch (error) {
        console.error(error);
      }
    }

    handleLLMForPlayers();
  }, [format, id, predictedTeam]);
  return (
    <>
      <PageTemplate title="Playing 11">
        <div className="flex">
          <div className="playerShortDetails -ml-10 mt-12">
            {format &&
              ["ODI", "T20", "Test"].includes(format) &&
              id &&
              (() => {
                let battingSR = aggregateStats[id]?.["Batting S/R"];
                let runs = aggregateStats[id]?.["Runs"];
                let battingAvg = aggregateStats[id]?.["Batting Avg"];
                let wickets = aggregateStats[id]?.["Wickets"];
                let economyRate = aggregateStats[id]?.["Economy Rate"];
                let bowlingSR = aggregateStats[id]?.["Bowling S/R"];

                if (battingSR == null || battingSR === Infinity || battingSR < 0) {
                  battingSR = "-";
                }
                if (runs == null || runs === Infinity || runs < 0) {
                  runs = "-";
                }
                if (battingAvg == null || battingAvg === Infinity || battingAvg < 0) {
                  battingAvg = "-";
                }
                if (wickets == null || wickets === Infinity || wickets < 0) {
                  wickets = "-";
                }
                if (economyRate == null || economyRate === Infinity || economyRate < 0) {
                  economyRate = "-";
                }
                if (bowlingSR == null || bowlingSR === Infinity || bowlingSR < 0) {
                  bowlingSR = "-";
                }

                console.log("battingSR", battingSR);
                console.log(predictedTeam[id]);

                return (
                  <PlayerInformation
                    title={"Player Information"}
                    child2={predictedTeam[id]}
                    child3={image}
                    child4={""}
                    child5={battingSR}
                    child6={runs}
                    child7={battingAvg}
                    child8={wickets}
                    child9={economyRate}
                    child10={bowlingSR}
                  />
                );
              })()}
          </div>
          <div className="flex flex-col text-slate-300 w-[50rem] tracking-wider text-lg ml-[24rem] mb-[18rem] leading-relaxed overflow-scroll">
            {playerLLMInfo}
          </div>
        </div>
      </PageTemplate>
      <div className="buttonCompDiv">
        <ButtonComponent nextPage={prevPage}>BACK</ButtonComponent>
        <ButtonComponent nextPage={nextPage}>SWAP</ButtonComponent>
      </div>
    </>
  );
}

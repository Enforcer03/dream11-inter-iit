"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { getAggregateStats } from "../api/aggregateSquad";
import { getSquadsByDate } from "../api/squads";
import ButtonComponent from "../components/buttonComp";
import LeagueSelector from "../components/leagueSelector";
import MatchSelector from "../components/matchSelector";
import PageTemplate from "../components/pageTemplate";
import VideoComp from "../components/videoSet";
import { useMatchData } from "../contexts/matchDataContext";
import { MatchDetails, SquadApiResponse } from "../types/squadApiResponse";

type MatchDateInputProps = {
  date: string;
  setDate: (date: string) => void;
  setAllData: (data: SquadApiResponse) => void;
  setAllLeagues: (leagues: string[]) => void;
  setLeague: (league: string) => void;
  setAllMatches: (matches: string[]) => void;
  setMatchData: React.Dispatch<React.SetStateAction<MatchDetails | null>>;
};

function isValidDateFormat(dateString: string) {
  const datePattern = /^(0[1-9]|[12][0-9]|3[01])\/(0[1-9]|1[0-2])\/\d{4}$/;
  return datePattern.test(dateString);
}

function formatWithPlaceholder(value: string) {
  const parts = value.split("/");

  if (parts.length === 1) {
    return `${parts[0]}${"DD/MM/YYYY".slice(parts[0].length)}`;
  } else if (parts.length === 2) {
    return `${parts[0]}/${parts[1]}${"MM/YYYY".slice(parts[1].length)}`;
  } else if (parts.length === 3) {
    return `${parts[0]}/${parts[1]}/${parts[2]}${"YYYY".slice(parts[2].length)}`;
  }

  return value;
}

function MatchDateInput({
  date,
  setDate,
  setAllData,
  setAllLeagues,
  setLeague,
  setAllMatches,
  setMatchData,
}: MatchDateInputProps) {
  function handleInputChange(e: React.ChangeEvent<HTMLInputElement>) {
    let value = e.target.value.replace(/[^0-9]/g, "");
    if (value.length > 8) value = value.slice(0, 8);

    let formattedDate = value;
    if (value.length > 4) {
      formattedDate = `${value.slice(0, 2)}/${value.slice(2, 4)}/${value.slice(4)}`;
    } else if (value.length > 2) {
      formattedDate = `${value.slice(0, 2)}/${value.slice(2)}`;
    }

    setDate(formattedDate);
    if (isValidDateFormat(formattedDate)) {
      handleGetSquads(formattedDate);
    }
  }

  const displayValue = () => {
    const numericDate = date.replace(/[^0-9/]/g, "");
    return formatWithPlaceholder(numericDate);
  };

  async function handleGetSquads(date: string) {
    try {
      const [day, month, year] = date.split("/");
      const formattedDate = `${year}-${month}-${day}`;

      const data = await getSquadsByDate(formattedDate);

      const newAllLeagues = Object.keys(data);
      const newSelectedLeague = newAllLeagues[0];
      const newAllMatches = Object.keys(data[newSelectedLeague]);
      const newMatchData = data[newSelectedLeague][newAllMatches[0]];

      setAllData(data);
      setAllLeagues(newAllLeagues);
      setLeague(newSelectedLeague);
      setAllMatches(newAllMatches);
      setMatchData(newMatchData);
    } catch (error) {
      console.error(error);
    }
  }

  return (
    <div className="flex flex-col items-center justify-center mt-16">
      <h1 className="text-3xl font-bold mb-8 text-[#FFD700] uppercase">Date of Match</h1>
      <input
        className="dateInputMatch"
        type="text"
        value={displayValue()}
        onChange={handleInputChange}
        placeholder="DD/MM/YYYY"
      />
    </div>
  );
}

function SelectMatchScreen() {
  const { date, setDate, matchData, setMatchData, setAggregateStats } = useMatchData();
  const [league, setLeague] = useState<string>("");
  const [allData, setAllData] = useState<SquadApiResponse | null>(null);
  const [allLeagues, setAllLeagues] = useState<string[]>([]);
  const [allMatches, setAllMatches] = useState<string[]>([]);

  const router = useRouter();

  const nextPage = "/player-selection";
  const prevPage = "/instructions";

  async function handleNextButton() {
    try {
      if (matchData === null) return;

      const teams = Object.keys(matchData).filter((team) => team != "Format");

      const teamPlayers = teams.map((team) => ({
        team,
        players: matchData[team],
      }));

      // teamPlayers.forEach(({ team, players }) => {
      //   console.log(`Team: ${team}, Players:`, players);
      // });

      const combinePlayerList = teamPlayers.map((team) => team.players).flat();

      const response = await getAggregateStats(combinePlayerList);
      setAggregateStats(response);
      console.log(response);
      // router.push(nextPage);
    } catch (error) {
      console.error(error);
    }
  }

  return (
    <div>
      <PageTemplate title="INPUT DETAILS" />
      <div className="selectMatchDiv">
        <MatchDateInput
          date={date}
          setDate={setDate}
          setAllData={setAllData}
          setAllLeagues={setAllLeagues}
          setLeague={setLeague}
          setAllMatches={setAllMatches}
          setMatchData={setMatchData}
        />
        <LeagueSelector setLeague={setLeague} allLeagues={allLeagues} setAllMatches={setAllMatches} allData={allData} />
        <MatchSelector allMatches={allMatches} setMatchData={setMatchData} allData={allData} league={league} />
      </div>
      <div className="buttonCompDiv">
        <ButtonComponent nextPage={prevPage}>BACK</ButtonComponent>
        <ButtonComponent onClick={handleNextButton}>NEXT</ButtonComponent>
      </div>
      <div className="videoCompDiv">
        <VideoComp nextPage="/video-instructions">
          VIDEO <span className="text-white">DEMO</span>
        </VideoComp>
      </div>
    </div>
  );
}

export default SelectMatchScreen;

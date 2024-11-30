"use client";

import { useState } from "react";
import { getSquadsByDate } from "../api/squads";
import ButtonComponent from "../components/buttonComp";
import LeagueSelector from "../components/leagueSelector";
import MatchSelector from "../components/matchSelector";
import PageTemplate from "../components/pageTemplate";
import VideoComp from "../components/videoSet";

function isValidDateFormat(dateString: string) {
  const datePattern = /^(0[1-9]|[12][0-9]|3[01])\/(0[1-9]|1[0-2])\/\d{4}$/;
  return datePattern.test(dateString);
}

function MatchDateInput({ date, setDate, setAllData, setAllLeagues }) {
  const formatWithPlaceholder = (value: string) => {
    const parts = value.split("/");
    if (parts.length === 1) {
      return `${parts[0]}${"DD/MM/YYYY".slice(parts[0].length)}`;
    } else if (parts.length === 2) {
      return `${parts[0]}/${parts[1]}${"YYYY".slice(parts[1].length)}`;
    } else if (parts.length === 3) {
      return `${parts[0]}/${parts[1]}/${parts[2]}`;
    }
    return value;
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
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
  };

  const displayValue = () => {
    const numericDate = date.replace(/[^0-9/]/g, "");
    return formatWithPlaceholder(numericDate);
  };

  async function handleGetSquads(date: string) {
    try {
      const [day, month, year] = date.split("/");
      const formattedDate = `${year}-${month}-${day}`;

      const data = await getSquadsByDate(formattedDate);
      setAllData(data);
      console.log(data);
      setAllLeagues(Object.keys(data));
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
  const [date, setDate] = useState("");
  const [league, setLeague] = useState("");
  const [match, setMatch] = useState("");
  const [allData, setAllData] = useState(null);
  const [allLeagues, setAllLeagues] = useState(null);
  const [allMatches, setAllMatches] = useState(null);

  const prevPage = "/instructions";
  const nextPage = "/player-selection";

  const objForNextPage = {
    pathname: "/player-selection",
    query: {
      allData,
      match,
    },
  };

  return (
    <div>
      <PageTemplate title="INPUT DETAILS" />
      <div className="selectMatchDiv">
        <MatchDateInput date={date} setDate={setDate} setAllData={setAllData} setAllLeagues={setAllLeagues} />
        <LeagueSelector setLeague={setLeague} allLeagues={allLeagues} setAllMatches={setAllMatches} allData={allData} />
        <MatchSelector setMatch={setMatch} allMatches={allMatches} />
      </div>
      <div className="buttonCompDiv">
        <ButtonComponent nextPage={prevPage}>BACK</ButtonComponent>
        <ButtonComponent nextPage={nextPage}>NEXT</ButtonComponent>
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

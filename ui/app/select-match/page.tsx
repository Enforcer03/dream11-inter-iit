"use client";

import { useState } from "react";
import AudioComponent from "../components/audioSet";
import ButtonComponent from "../components/buttonComp";
import PageTemplate from "../components/pageTemplate";
import VideoComp from "../components/videoSet";
import LeagueSelector from "../components/leagueSelector";
import MatchSelector from "../components/matchSelector";

function MatchDateInput({ date, setDate }) {
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
  };

  const displayValue = () => {
    const numericDate = date.replace(/[^0-9/]/g, "");
    return formatWithPlaceholder(numericDate);
  };

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

  const prevPage = "/instructions";
  const nextPage = "/player-selection"

  return (
    <div>
      <PageTemplate title="INPUT DETAILS" />
      <div className="selectMatchDiv">
        <MatchDateInput date={date} setDate={setDate} />
        <LeagueSelector setLeague={setLeague} />
        <MatchSelector setMatch={setMatch} />
      </div>
      <div className="buttonCompDiv">
        <ButtonComponent nextPage={prevPage}>BACK</ButtonComponent>
        <ButtonComponent nextPage={nextPage}>NEXT</ButtonComponent>
      </div>
      <div className="videoCompDiv">
        <VideoComp nextPage="/video-instructions">VIDEO <span className="text-white">DEMO</span></VideoComp>
      </div>
    </div>
  );
}

export default SelectMatchScreen;

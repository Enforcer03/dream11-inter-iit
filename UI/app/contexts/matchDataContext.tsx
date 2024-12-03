"use client";

import React, { createContext, ReactNode, useContext, useState } from "react";
import { AggregateApiResponse } from "../types/aggregateApiResponse";
import { RevaluateTeamApiResponse } from "../types/modelApiResponse";
import { MatchDetails } from "../types/squadApiResponse";

interface MatchDataContextProps {
  matchData: MatchDetails | null;
  setMatchData: React.Dispatch<React.SetStateAction<MatchDetails | null>>;
  date: string;
  setDate: React.Dispatch<React.SetStateAction<string>>;
  aggregateStats: AggregateApiResponse | null;
  setAggregateStats: React.Dispatch<React.SetStateAction<AggregateApiResponse | null>>;
  covMatrix: string;
  setCovMatrix: React.Dispatch<React.SetStateAction<string>>;
  predictedTeam: string[];
  setPredictedTeam: React.Dispatch<React.SetStateAction<string[]>>;
  playerStats: PlayerStats[];
  setPlayerStats: React.Dispatch<React.SetStateAction<PlayerStats[]>>;
  selectedPlayersTeamA: string[];
  setSelectedPlayersTeamA: React.Dispatch<React.SetStateAction<string[]>>;
  selectedPlayersTeamB: string[];
  setSelectedPlayersTeamB: React.Dispatch<React.SetStateAction<string[]>>;
  teamStats: RevaluateTeamApiResponse;
  setTeamStats: React.Dispatch<React.SetStateAction<RevaluateTeamApiResponse>>;
  instructionLLM: TeamLLMPara;
  setInstructionLLM: React.Dispatch<React.SetStateAction<TeamLLMPara>>;
  totalScore: number;
  setTotalScore: React.Dispatch<React.SetStateAction<number>>;
}

export type PlayerStats = {
  player: string;
  mean_points: number;
  variance: number;
  batting_points: number;
  bowling_points: number;
  fielding_points: number;
  team: string;
};

export type TeamLLMPara = {
  team: string[];
  instruction: string;
};

const MatchDataContext = createContext<MatchDataContextProps | undefined>(undefined);

export const MatchDataProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [matchData, setMatchData] = useState<MatchDetails | null>(null);
  const [date, setDate] = useState<string>("");
  const [aggregateStats, setAggregateStats] = useState<AggregateApiResponse | null>(null);
  const [covMatrix, setCovMatrix] = useState<string>("");
  const [predictedTeam, setPredictedTeam] = useState<string[]>([]);
  const [playerStats, setPlayerStats] = useState<PlayerStats[]>([]);
  const [selectedPlayersTeamA, setSelectedPlayersTeamA] = useState<string[]>([]);
  const [selectedPlayersTeamB, setSelectedPlayersTeamB] = useState<string[]>([]);
  const [teamStats, setTeamStats] = useState<RevaluateTeamApiResponse>({
    team_consistency_score: 0,
    team_diversity_score: 0,
    form_score: 0,
  });
  const [instructionLLM, setInstructionLLM] = useState<TeamLLMPara>({ team: [], instruction: "" });
  const [totalScore, setTotalScore] = useState<number>(0);

  return (
    <MatchDataContext.Provider
      value={{
        matchData,
        setMatchData,
        date,
        setDate,
        aggregateStats,
        setAggregateStats,
        covMatrix,
        setCovMatrix,
        predictedTeam,
        setPredictedTeam,
        playerStats,
        setPlayerStats,
        selectedPlayersTeamA,
        setSelectedPlayersTeamA,
        selectedPlayersTeamB,
        setSelectedPlayersTeamB,
        teamStats,
        setTeamStats,
        instructionLLM,
        setInstructionLLM,
        totalScore,
        setTotalScore,
      }}
    >
      {children}
    </MatchDataContext.Provider>
  );
};

export const useMatchData = (): MatchDataContextProps => {
  const context = useContext(MatchDataContext);
  if (!context) {
    throw new Error("useMatchData must be used within a MatchDataProvider");
  }
  return context;
};

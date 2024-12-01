"use client";

import React, { createContext, ReactNode, useContext, useState } from "react";
import { AggregateApiResponse } from "../types/aggregateApiResponse";
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

const MatchDataContext = createContext<MatchDataContextProps | undefined>(undefined);

export const MatchDataProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [matchData, setMatchData] = useState<MatchDetails | null>(null);
  const [date, setDate] = useState<string>("");
  const [aggregateStats, setAggregateStats] = useState<AggregateApiResponse | null>(null);
  const [covMatrix, setCovMatrix] = useState<string>("");
  const [predictedTeam, setPredictedTeam] = useState<string[]>([]);
  const [playerStats, setPlayerStats] = useState<PlayerStats[]>([]);

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

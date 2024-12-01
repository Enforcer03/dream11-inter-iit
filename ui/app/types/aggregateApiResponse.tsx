type AggregateStats = {
  Batting: string;
  "Batting Avg": number;
  "Batting S/R": number;
  Bowling: string;
  "Bowling S/R": number;
  "Economy Rate": number;
  Runs: number;
  Wickets: number;
};

type Formats = "T20" | "ODI" | "Test";

export type AggregateApiResponse = {
  [playerName: string]: {
    [K in Formats]: AggregateStats;
  };
};

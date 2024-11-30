type FixedMatchDetails = {
  Format: "T20" | "ODI" | "Test";
};

type DynamicMatchDetails = {
  [teamName: string]: string[];
};

type MatchDetails = FixedMatchDetails & DynamicMatchDetails;

export type SquadApiResponse = {
  [seriesName: string]: {
    [matchName: string]: MatchDetails;
  };
};

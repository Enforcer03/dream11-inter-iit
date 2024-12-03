export type PlayerInfo = {
  [key: string]: string[];
};

export type ModelApiResponse = {
  best_team: string[];
  cov_matrix: string;
  player_stats: string;
};

export type RevaluateTeamApiResponse = {
  team_consistency_score: number;
  team_diversity_score: number;
  form_score: number;
};

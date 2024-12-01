import axios from "axios";
import { ModelApiResponse, RevaluateTeamApiResponse } from "@/app/types/modelApiResponse";

export async function getPredicted11(date: string, format: "T20" | "Test" | "ODI"): Promise<ModelApiResponse> {
  try {
    const obj = { date, format, player_info };
    const response = await axios.post("http://localhost:8089/generate_best_team", obj);
    return response.data;
  } catch (error) {
    console.error(error);
    throw error;
  }
}

export async function revaluateTeamSwap(
  cov_matrix: string,
  player_stats: string,
  best_team: string[]
): Promise<RevaluateTeamApiResponse> {
  try {
    const obj = { best_team, player_stats, cov_matrix };
    const response = await axios.post("http://localhost:8089/generate_best_team", obj);
    return response.data;
  } catch (error) {
    console.error(error);
    throw error;
  }
}

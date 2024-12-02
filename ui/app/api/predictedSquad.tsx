import axios from "axios";
import { ModelApiResponse, PlayerInfo, RevaluateTeamApiResponse } from "@/app/types/modelApiResponse";

export async function getPredicted11(
  date: string,
  format: "T20" | "Test" | "ODI",
  player_info: PlayerInfo
): Promise<ModelApiResponse> {
  try {
    const [day, month, year] = date.split("/");
    const formattedDate = `${year}-${month}-${day}`;

    const obj = { date: formattedDate, format, player_info };
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

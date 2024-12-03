import axios from "axios";
import { LLMPlayerApiResponse, LLMTeamApiResponse } from "../types/llmApiResponse";

export async function handleLLMTeam(
  best_team: string[],
  player_stats: string,
  format: "T20" | "Test" | "ODI"
): Promise<LLMTeamApiResponse> {
  try {
    const obj = { best_team, format, player_stats };
    const response = await axios.post("http://localhost:3002/analyze_team", obj);
    return response.data;
  } catch (error) {
    console.error(error);
    throw error;
  }
}

export async function handleLLMPlayer(
  format: string,
  playerName: string,
  best_team: string[]
): Promise<LLMPlayerApiResponse> {
  try {
    const obj = { Player: playerName, best_team, format };
    const response = await axios.post("http://localhost:3002/analyze_player", obj);
    return response.data;
  } catch (error) {
    console.error(error);
    throw error;
  }
}

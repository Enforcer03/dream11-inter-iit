import axios from "axios";
import { AggregateApiResponse } from "@/app/types/aggregateApiResponse";

export async function getAggregateStats(
  playerNames: string[],
  format: "T20" | "Test" | "ODI"
): Promise<AggregateApiResponse> {
  try {
    const response = await axios.post("http://localhost:3002/aggregate_stats", {
      Players: playerNames,
      Format: format,
    });
    return response.data;
  } catch (error) {
    console.error(error);
    throw error;
  }
}

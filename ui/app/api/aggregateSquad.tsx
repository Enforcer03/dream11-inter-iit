import axios from "axios";
import { AggregateApiResponse } from "@/app/types/aggregateApiResponse";

export async function getAggregateStats(playerNames: string[]): Promise<AggregateApiResponse> {
  try {
    const response = await axios.post("http://localhost:8080/aggregate_stats", { Players: playerNames });
    return response.data;
  } catch (error) {
    console.error(error);
    throw error;
  }
}

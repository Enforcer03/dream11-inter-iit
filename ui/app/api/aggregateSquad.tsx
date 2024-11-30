import axios from "axios";

export async function getAggregateStats(playerName: string) {
  try {
    const response = await axios.post("http://localhost:8080/aggregate_stats", { Player: playerName });
    return response.data;
  } catch (error) {
    console.error(error);
    return error;
  }
}

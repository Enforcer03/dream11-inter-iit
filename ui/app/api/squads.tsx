import axios from "axios";
import { SquadApiResponse } from "@/app/types/squadApiResponse";

export async function getSquadsByDate(date: string): Promise<SquadApiResponse> {
  try {
    const response = await axios.post("http://localhost:5000/squads", { Date: date });
    return response.data;
  } catch (error) {
    console.error(error);
    throw error;
  }
}

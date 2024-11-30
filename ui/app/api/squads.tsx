import axios from "axios";

export async function getSquadsByDate(date: string) {
  try {
    const response = await axios.post("http://localhost:5000/squads", { Date: date });
    return response.data;
  } catch (error) {
    console.error(error);
    return error;
  }
}

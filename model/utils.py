import streamlit as st
import openai
import json
import os
from dotenv import load_dotenv
import plotly.graph_objects as go



load_dotenv()
KEY = os.getenv('OPENAI_KEY')

# Initialize OpenAI API client
client = openai.OpenAI(api_key=KEY)



def get_optimal_team_llm(player_data, client= client):
    prompt = f"""
    You are an expert fantasy cricket selector. Create the best team of 11 players from the following 22 players based on their expected fantasy scores. Make sure to include at least one player from each team. 

    Players and their scores:
    {player_data}

    Return the team as a list of player names. For each player, output the most important attribute for the player's selection. The only constraint is that at least one player from each team be selected.
    """

    # Call the chat completion API
    response = client.chat.completions.create(
        model="gpt-4",  # Use the correct OpenAI model
        messages=[
            {"role": "system", "content": "You are a fantasy cricket expert. Suggest the best 11 players out of the ones given. Ensure one player from each team is selected."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.9
    )

    return response.choices[0].message.content

def best_team_button():
    if st.button("Generate Best Team LLM"):
        if len(player_data) < 22:
            st.error("Please ensure data for at least 22 players is provided.")
        else:
            player_input = "\n".join(
                [f"{p['name']} ({p['role']}): {p['score']}" for p in player_data]
            )
            st.write("Processing your team selection...")

            raw_response = get_optimal_team_llm(player_input)

            if raw_response:
                st.success("Optimal Team Generated Successfully!")
                st.subheader("Optimal Team")
                st.text(raw_response)
            else:
                st.error("Error generating the optimal team.")


def get_past_match_performance(player_name, fantasy_points, num_matches=100):
  player_data = fantasy_points.get(player_name)
  if player_data is None:
      print(f"Warning: Player not found in data: {player_name}")
      return [], []  # Return empty lists if player data is not found

  # Since player_data is a list of tuples (match_key, match_data)
  # Get the last 'num_matches' matches
  last_matches_data = player_data[-num_matches:]

  # Extract match names and total points
  last_matches = [match_key for match_key, _ in last_matches_data]
  last_points = [match_data['total_points'] for _, match_data in last_matches_data]

  return last_matches, last_points
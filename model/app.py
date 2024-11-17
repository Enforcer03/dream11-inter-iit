import streamlit as st
import openai
from openai import OpenAI
import json

# Set your OpenAI API 
import os
from dotenv import load_dotenv

load_dotenv()

KEY = os.getenv('OPENAI_KEY')

client = OpenAI(api_key=KEY)

def load_sample_players(json_file):
    with open(json_file, "r") as file:
        return json.load(file)

# Function to get the optimal team using OpenAI API
def get_optimal_team(player_data):
    prompt = f"""
    You are an expert fantasy cricket selector. Create the best team of 11 players from the following 22 players based on their expected fantasy scores. Make sure to include at least 4 bowlers, 1 wicket-keeper, and 2 all-rounders. The team should have a good balance of batters, bowlers, and all-rounders. 

    Players and their scores:
    {player_data}

    Return the team as a list of player names. For each player output the most important attribute for player's selection. The only constraint is that at least one player from each team be selected.
    """
    
    # Call the chat completion API
    response = client.chat.completions.create(
        model="gpt-4",  # Use the correct OpenAI model
        messages=[
            {"role": "system", "content": "You are a fantasy cricket expert. You have to suggest the best 11 players out of the ones given. The only constraint is that one player from each team must be selected."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    
    # Extract and return the response
    return response.choices[0].message.content

# Streamlit UI setup
st.title("Fantasy Cricket Team Selector")
st.markdown(
    """
    - Upload player data from a JSON file or manually input details.
    - Generate the best team of 11 players using AI.
    """
)

# Sidebar options for loading or inputting data
st.sidebar.header("Options")
upload_sample = st.sidebar.checkbox("Load Sample Players from JSON")
manual_input = st.sidebar.checkbox("Add Players Manually")

# Data input handling
player_data = []

if upload_sample:
    try:
        teams = load_sample_players("sample_players.json")
        for team_idx, team in enumerate(teams.values()):
            for player in team['players']:
                player['team']= team_idx
                player_data.append(player)
        st.success("Sample players loaded successfully!")
    except FileNotFoundError:
        st.error("Sample file not found. Please ensure 'sample_players.json' exists.")
elif manual_input:
    st.write("Enter details for each player:")
    for i in range(22):
        col1, col2, col3 = st.columns(3)
        with col1:
            name = st.text_input(f"Player {i+1} Name:", key=f"name_{i}")
        with col2:
            role = st.selectbox(
                f"Player {i+1} Role:",
                ['Batter', 'Bowler', 'All-Rounder', 'Wicket-Keeper'],
                key=f"role_{i}"
            )
        with col3:
            score = st.number_input(
                f"Player {i+1} Fantasy Score:",
                min_value=0,
                step=1,
                key=f"score_{i}"
            )
        if name:
            player_data.append({"name": name, "role": role, "score": score})

# Process and generate team
if st.button("Generate Best Team"):
    if len(player_data) < 22:
        st.error("Please ensure data for atleast 22 players is provided.")
    else:
        player_input = "\n".join(
            [f"{p['name']} ({p['role']}): {p['score']}" for p in player_data]
        )
        st.write("Processing your team selection...")

        raw_response = get_optimal_team(player_input)

        if raw_response:
            st.success("Optimal Team Generated Successfully!")
            
            st.subheader("Raw AI Response")
            st.text(raw_response)
            
            optimal_team = raw_response.strip().split("\n")  # Split the response into individual player names
            st.subheader("Optimal Team")
            st.write(optimal_team)
        else:
            st.error("Error generating the optimal team.")

# Visual enhancements
st.sidebar.info("To try with IPL players, load the sample JSON!")
st.markdown("---")
st.caption("Powered by OpenAI")
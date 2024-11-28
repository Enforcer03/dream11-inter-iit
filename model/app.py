import streamlit as st
import openai
import json
import os
from dotenv import load_dotenv
import plotly.graph_objects as go
import re
from heuristic_solver import load_player_fantasy_points_for_optimization, compute_player_stats, compute_covariance_matrix, optimize_team, optimize_team_sharpe
import datetime
from utils import get_optimal_team_llm, get_past_match_performance, best_team_button
import pandas as pd
import numpy as np
# from heuristic_solver import load_player_fantasy_points_for_optimization

@st.cache_data()
def load_sample_players(json_file):
    with open(json_file, "r") as file:
        return json.load(file)

@st.cache_data()
def get_optim_file():
    return load_player_fantasy_points_for_optimization(fantasy_points_path)


@st.cache_data()
def load_player_fantasy_points(json_file):
  with open(json_file, "r") as file:
      data = json.load(file)
      # For each player, sort the matches by date
      sorted_data = {}
      for player, matches in data.items():
          # Convert matches dict to list of tuples (match_key, match_data)
          match_list = list(matches.items())
          # Function to extract date from match_key
          def extract_date_from_match_key(match_key):
              # Regex pattern to match date in format YYYY-MM-DD
              date_pattern = r'(\d{4}-\d{2}-\d{2})'
              match = re.search(date_pattern, match_key)
              if match:
                  date_str = match.group(1)
                  try:
                      date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
                  except ValueError:
                      date = datetime.datetime.min  # Assign a min date if parsing fails
              else:
                  date = datetime.datetime.min  # Assign a min date if date not found
              return date
          # Now sort the match_list by date
          match_list_sorted = sorted(match_list, key=lambda x: extract_date_from_match_key(x[0]))
          # Assign the sorted list to the player
          sorted_data[player] = match_list_sorted  # List of tuples (match_key, match_data)
      return sorted_data

# Streamlit UI setup
st.title("Fantasy Cricket Team Selector")
st.markdown(
    """
    - Load data from scheduled matches or manually input details.
    - Generate the best team of 11 players using AI.
    """
)

# File paths
fantasy_points_path = "/Users/ved14/Library/CloudStorage/GoogleDrive-v_umrajkar@ma.iitr.ac.in/My Drive/SEM7/extras/dream11-inter-iit/data/player_fantasy_points_t20.json"
json_file_path = "/Users/ved14/Library/CloudStorage/GoogleDrive-v_umrajkar@ma.iitr.ac.in/My Drive/SEM7/extras/dream11-inter-iit/T20_Match_Level_Till_training_date_Players.json"
aggregate_stats_path = "/Users/ved14/Library/CloudStorage/GoogleDrive-v_umrajkar@ma.iitr.ac.in/My Drive/SEM7/extras/dream11-inter-iit/data/aggregate_cricket_stats_t20.json"

# Load player data and aggregate statistics
try:
    match_data = load_sample_players(json_file_path)
    match_keys = list(match_data.keys())
except FileNotFoundError:
    st.error("JSON file not found. Please ensure the file path is correct.")

try:
    fantasy_points = load_player_fantasy_points(fantasy_points_path)
    # print(fantasy_points)
except FileNotFoundError:
    st.error("Fantasy points JSON file not found.")

try:
    aggregate_stats = load_sample_players(aggregate_stats_path)
except FileNotFoundError:
    st.error("Aggregate stats JSON file not found.")

# Sidebar options
st.sidebar.header("Options")
upload_sample = st.sidebar.checkbox("Load Sample Players from JSON")
manual_input = st.sidebar.checkbox("Add Players Manually")
squad_info = st.sidebar.checkbox("Load squads from scheduled matches")
assess_players = st.sidebar.checkbox("Assess Players from the squads")
optimize_team_option = st.sidebar.checkbox("Optimize Team Selection")
st.sidebar.selectbox("Select Format", [])



if squad_info:
  # Initialize assigned_weights_df in session_state if not already present
  if 'assigned_weights_df' not in st.session_state:
      st.session_state['assigned_weights_df'] = None
  if 'stats_df' not in st.session_state:
      st.session_state['stats_df'] = None

  # Select a match
  selected_match = st.selectbox("Select a Match", match_keys)

  if selected_match:
      squads = match_data[selected_match]
      st.subheader("Squads for the Match")

      player_info = {}
      for team_name, players in squads.items():
          player_info[team_name] = []
          with st.expander(team_name, expanded=True):
              st.write("Players:")
              for player in players:
                  st.markdown(f"- **{player}**")
                  player_info[team_name].append(f"{player} : {team_name}")

  # Assess Players Section
  if assess_players:
      optim_fantasy_points = get_optim_file()
      # Store the selected player in session state
      if 'selected_player' not in st.session_state:
          st.session_state.selected_player = None

      # Combine players from all teams
      all_players = [player for team in player_info.values() for player in team]
      all_players = list(set(all_players))

      selected_player = st.selectbox("Select a Player", sorted(all_players), key="player_select")
      st.session_state.selected_player = selected_player
      all_keys = ['total_points', 'batting_points', 'fielding_points', 'bowling_points']

      if selected_player:
          selected_key = st.selectbox("Select a Key", all_keys)
          player_name = selected_player.split(":")[0].strip()
          st.session_state.selected_key = selected_key

          if selected_key:
              matches, total_points = get_past_match_performance(player_name, fantasy_points, key=selected_key)

              if matches and total_points:
                  fig = go.Figure()
                  fig.add_trace(go.Bar(x=matches, y=total_points, name='Total Points'))
                  fig.update_layout(
                      title=f"Total Points for {selected_player} in Past Matches",
                      xaxis_title="Matches",
                      yaxis_title="Total Points",
                      template="plotly_white"
                  )
                  st.plotly_chart(fig)
              else:
                  st.error(f"No data available for {player_name}.")

  # Optimize Team Section
  if optimize_team_option:
      # Combine players from all teams
      all_players = [player.split(":")[0].strip() for team in player_info.values() for player in team]
      all_players = list(set(all_players))

      # Set risk tolerance
      st.write("Players available for selection:")
      st.write(all_players)
      risk_tolerance = st.slider("Set Risk Tolerance", min_value=0.01, max_value=10.0, value=1.0, step=0.01)

      # Perform optimization when the "Optimize Team" button is clicked
      if st.button("Optimize Team"):
          # Compute expected points and variances
          stats_df = compute_player_stats(optim_fantasy_points, list(all_players), num_matches=100)
          print(f"stats_df {stats_df.shape}")
          print(f"length of the stats_df {len(stats_df['player'].tolist())}")

          if stats_df.empty:
              st.error("No player statistics available.")
          else:
              # Compute covariance matrix
              cov_matrix = compute_covariance_matrix(
                  optim_fantasy_points, stats_df['player'].tolist(), num_matches=100
              )

              # Optimize team using Sharpe Ratio
              selected_players, weights_df = optimize_team_sharpe(
                  stats_df, cov_matrix, risk_aversion=risk_tolerance, boolean=True
              )

              if weights_df is not None and not weights_df.empty:
                  # Store the results in session_state
                  st.session_state['assigned_weights_df'] = weights_df
                  st.session_state['stats_df'] = stats_df
                  st.success("Optimization successful!")

              else:
                  st.error("Failed to select an optimal team.")

      # Display optimization results if available
      if (
          'assigned_weights_df' in st.session_state and st.session_state['assigned_weights_df'] is not None and
          'stats_df' in st.session_state and st.session_state['stats_df'] is not None
      ):
          weights_df = st.session_state['assigned_weights_df']
          stats_df = st.session_state['stats_df']

          # Merge weights_df with stats_df to include expected scores and variances
          weights_df_display = weights_df.merge(
              stats_df[['player', 'mean_points', 'variance']],
              on='player',
              how='left'
          )

          # Show the dataframe
          st.success("Optimal Weights assigned:")
          st.write(weights_df_display)

          # Output the weights, expected scores, and variances as a grouped bar plot
          weights_df_display = weights_df_display.sort_values(by='weight', ascending=True)

          fig = go.Figure()
          fig.add_trace(go.Bar(
              x=weights_df_display['weight'],
              y=weights_df_display['player'],
              name='Selection Weight',
              orientation='h',
              marker_color='blue'
          ))
          fig.add_trace(go.Bar(
              x=weights_df_display['mean_points'],
              y=weights_df_display['player'],
              name='Expected Score',
              orientation='h',
              marker_color='green'
          ))
          fig.add_trace(go.Bar(
              x=np.sqrt(weights_df_display['variance']),
              y=weights_df_display['player'],
              name='Standard Deviation',
              orientation='h',
              marker_color='red'
          ))
          fig.update_layout(
              title="Player Selection Weights, Expected Scores, and Standard Deviations",
              xaxis_title="Value",
              yaxis_title="Player",
              barmode='group',
              template="plotly_white",
              height=600  # Adjust the height for better UI
          )
          st.plotly_chart(fig)

  # Get Optimal Team Section
  if st.button("Get Optimal Team"):
      if len(player_info) < 1:
          st.error("Please ensure data for at least 22 players is provided.")
      else:
          player_input = []
          for team_name, players in player_info.items():
              for player in players:
                  player_name = player.split(" : ")[0]
                  stats = aggregate_stats.get(player_name, {})
                  if stats:
                      stats_info = (
                          f"{player_name} (Team: {team_name}) - "
                          f"Games: {stats.get('Games', 0)}, "
                          f"Wins: {stats.get('Won', 0)}, "
                          f"Win %: {stats.get('Win %', 0)}, "
                          f"Runs: {stats.get('Runs', 0)}, "
                          f"Fours: {stats.get('Fours', 0)}"
                      )
                  else:
                      stats_info = f"{player_name} (Team: {team_name}) - No statistics available"
                  player_input.append(stats_info)

          # Convert player information to a single string
          player_input_str = "\n".join(player_input)

          # Now, include the assigned_weights_df in the input string
          if (
              'assigned_weights_df' in st.session_state and st.session_state['assigned_weights_df'] is not None
          ):
              assigned_weights_df = st.session_state['assigned_weights_df']
              weights_info = []
              for index, row in assigned_weights_df.iterrows():
                  weights_info.append(f"{row['player']} - Selection Weight: {row['weight']}")
              weights_info_str = "\n".join(weights_info)
              # Append weights information to the player_input_str
              player_input_str += "\n\nPlayer Weights:\n" + weights_info_str
          else:
              st.warning("Weights data not found. Proceeding without weights information.")

          st.write("Processing your team selection...")

          # Pass the updated player_input_str to the LLM
          raw_response = get_optimal_team_llm(player_input_str)

          if raw_response:
              st.success("Optimal Team Generated Successfully!")
              st.subheader("Optimal Team")
              st.text(raw_response)
          else:
              st.error("Error generating the optimal team.")

player_data = []
if upload_sample:
    try:
        teams = load_sample_players("sample_players.json")
        for team_idx, team in enumerate(teams.values()):
            for player in team['players']:
                player['team'] = team_idx
                player_data.append(player)
        st.success("Sample players loaded successfully!")
    except FileNotFoundError:
        st.error("Sample file not found.")
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
    best_team_button()

# Generate team based on manual input or sample data


st.markdown("---")
st.caption("Powered by OpenAI")

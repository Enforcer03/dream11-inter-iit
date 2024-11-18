# heuristic_mean_variance_solver.py

import numpy as np
import pandas as pd
import json
import re
import datetime
import cvxpy as cp


# Function to load and sort fantasy points data
def load_player_fantasy_points_for_optimization(json_file):
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
          # Reconstruct the matches dict, now it's ordered
          sorted_data[player] = dict(match_list_sorted)
      return sorted_data

# Function to compute expected points and variance
def compute_player_stats(fantasy_points, players, num_matches=100):
  data = []
  for player in players:
      player_data = fantasy_points.get(player)
      if player_data is None:
          # Assign dummy values for expected points and variance
          expected_points = 0.0
          variance = 0.0
      else:
          # Extract total points
          matches = list(player_data.values())

          # Get the last 'num_matches' matches
          matches = matches[-num_matches:]

          total_points = [match['total_points'] for match in matches]

          expected_points = np.mean(total_points) if total_points else 0.0
          variance = np.var(total_points) if total_points else 0.0

      data.append({
          'player': player,
          'mean_points': expected_points,
          'variance': variance
      })
  stats_df = pd.DataFrame(data)
  return stats_df

# Function to compute covariance matrix
def compute_covariance_matrix(fantasy_points, players, num_matches=100):
  player_point_series = {}
  max_length = 0
  print(f"length of players :  {len(players)}")
  print(players)

  for player in players:
      player_data = fantasy_points.get(player)
      if player_data is None:
          # Assign a dummy series of zeros
          total_points = [0.0] * num_matches
      else:
          # Extract total points
          matches = list(player_data.values())

          # Get the last 'num_matches' matches
          matches = matches[-num_matches:]
          total_points = [match['total_points'] for match in matches]

      # Pad the series if it's shorter than 'num_matches'
      if len(total_points) < num_matches:
          total_points = [0.0] * (num_matches - len(total_points)) + total_points

      # Update max_length
      if len(total_points) > max_length:
          max_length = len(total_points)

      player_point_series[player] = pd.Series(total_points)

  # Create a DataFrame from the series, align them by index
  print(f"length of player_points_series:  {len(player_point_series)}")

  points_df = pd.DataFrame(player_point_series)
  print(f"shape of points_df:  {len(points_df.shape)}")

  # Handle missing values by filling with 0.0
  points_df = points_df.fillna(0.0)

  # Compute covariance matrix
  cov_matrix = points_df.cov()
  return cov_matrix

# Function to optimize the team
def optimize_team(stats_df, cov_matrix, risk_tolerance=0.1):
  """
  Optimize the fantasy cricket team using mean-variance optimization.

  Parameters:
  - stats_df: pandas DataFrame, contains 'player', 'mean_points', 'variance_points'.
  - cov_matrix: pandas DataFrame, covariance matrix of players.
  - risk_tolerance: float, hyperparameter for risk tolerance (lambda).

  Returns:
  - selected_players: list, names of selected players.
  """
  # Number of players
  n = len(stats_df)

  # Variable for selection (binary variables)
  w = cp.Variable(n, boolean=False)

  # Parameters
  mu = stats_df['mean_points'].values
  Sigma = cov_matrix.values

  # Objective function
  print(f"Shape of w: {w.shape}")
  print(f"Shape of Sigma: {Sigma.shape}")
  expected_points = mu.T @ w
  variance = cp.quad_form(w, Sigma)
  objective = cp.Maximize(expected_points - (1- risk_tolerance) * variance)

  # Constraints
  constraints = []

  # Total number of players constraint
  constraints.append(cp.sum(w) == 2)

  # Solve the problem
  prob = cp.Problem(objective, constraints)
  try:
      prob.solve(solver=cp.GUROBI, verbose=True)
  except cp.error.SolverError:
      # If GUROBI is not available, try CBC
      prob.solve(solver=cp.CBC, verbose=True)

  # Check if the problem was solved
  if prob.status not in ["optimal", "optimal_inaccurate"]:
      print(f"Optimization failed: {prob.status}")
      return [], pd.DataFrame()

  # Get the selected players
  w_values = w.value
  selected_indices = [i for i in range(n) if w_values[i] > 0.5]
  selected_players = stats_df.iloc[selected_indices]['player'].tolist()

  # Prepare weights output
  weights = pd.DataFrame({
      'player': stats_df['player'],
      'weight': w_values
  })

  return None, weights

# Main function to run the optimization
def main():
  # File paths (modify these paths according to your files)
  fantasy_points_path = '/Users/ved14/Library/CloudStorage/GoogleDrive-v_umrajkar@ma.iitr.ac.in/My Drive/SEM7/extras/dream11-inter-iit/data/player_fantasy_points_t20.json'
  squad_players_path = 'squad_players.json'       

  # Load data
  fantasy_points = load_player_fantasy_points_for_optimization(fantasy_points_path)

  # Load squad players
  with open(squad_players_path, 'r') as f:
      squad_players = json.load(f)

  # Prepare the list of players
#   players =[]
#   for team, data in squad_players.items():
#       for player in data['players']:
#           players.append(player["name"])
  players = squad_players
          

  stats_df = compute_player_stats(fantasy_points, players, num_matches=100)

  if stats_df.empty:
      print("No player statistics available. Exiting.")
      return

  # Compute covariance matrix
  cov_matrix = compute_covariance_matrix(fantasy_points, stats_df['player'].tolist(), num_matches=100)

  # Set risk tolerance hyperparameter
  risk_tolerance = 0.1  # Adjust this value as needed

  # Optimize team
  selected_players, weights = optimize_team(stats_df, cov_matrix, risk_tolerance=risk_tolerance)

#   if selected_players:
#       print("Optimal Team Selected:")
#       for player in selected_players:
#           print(player)

      # Output the weights (selection decisions)
  print("\nPlayer Selection Weights:")
  print(weights)
#   else:
#       print("Failed to select an optimal team.")

if __name__ == "__main__":
  main()
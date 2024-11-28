# heuristic_mean_variance_solver.py

import numpy as np
import pandas as pd
import json
import re
import datetime
import cvxpy as cp
from utils import get_optimal_team_llm, get_past_match_performance, best_team_button, extract_date_from_match_key
import pulp
import numpy as np
from scipy.stats import entropy

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
def compute_player_stats(fantasy_points, players, num_matches=100, date_of_match=None):
  # Compute the mean and variance of fantasy points for each player
  stats_list = []
  for player in players:
      matches, points = get_past_match_performance(
          player,
          fantasy_points,
          num_matches=num_matches,
          key='total_points',
          date_of_match=date_of_match
      )
      if points:
          mean_points = np.mean(points)
          variance_points = np.var(points)
          stats_list.append({
              'player': player,
              'mean_points': mean_points,
              'variance': variance_points
          })

  stats_df = pd.DataFrame(stats_list)
  return stats_df

# Function to compute covariance matrix
def compute_covariance_matrix(fantasy_points, players, num_matches=100, date_of_match=None):
  # Create a DataFrame of player fantasy points time series
  time_series_data = {}
  for player in players:
      matches, points = get_past_match_performance(
          player,
          fantasy_points,
          num_matches=num_matches,
          key='total_points',
          date_of_match=date_of_match
      )
      if points:
          time_series_data[player] = points
      else:
          # If no data available, fill with the mean of existing points
          time_series_data[player] = [np.mean(points)] * num_matches

  # Create DataFrame
  df = pd.DataFrame(time_series_data)

  # Compute covariance matrix
  cov_matrix = df.cov()
  return cov_matrix

def optimize_team_sharpe(stats_df, cov_matrix, num_players=11, risk_aversion=1.0, boolean=True):
    """
    Enhanced optimization with DCP-compliant objectives.
    """
    n = len(stats_df)
    w = cp.Variable(n, boolean=boolean)

    # Core parameters
    mu = stats_df['mean_points'].values
    Sigma = cov_matrix.values if isinstance(cov_matrix, pd.DataFrame) else cov_matrix
    
    # Make sure Sigma is positive semidefinite
    Sigma = (Sigma + Sigma.T) / 2  # Ensure symmetry
    min_eig = np.min(np.real(np.linalg.eigvals(Sigma)))
    if min_eig < 0:
        Sigma -= 1.1 * min_eig * np.eye(Sigma.shape[0])  # Make positive definite
    
    # Objectives that comply with DCP rules
    expected_points = mu @ w
    risk_term = cp.quad_form(w, Sigma)  # Now using positive semidefinite matrix
    
    # Use DCP-compliant objective
    objective = cp.Maximize(expected_points - risk_aversion * risk_term)

    # Basic constraint
    constraints = [cp.sum(w) == num_players]

    # Solve with multiple solver options
    prob = cp.Problem(objective, constraints)
    
    try:
        prob.solve(solver=cp.GUROBI, verbose=True)
    except (cp.error.SolverError, cp.error.DCPError):
        try:
            prob.solve(solver=cp.CBC, verbose=True)
        except:
            prob.solve(solver=cp.SCS, verbose=True)

    if prob.status not in ["optimal", "optimal_inaccurate"]:
        print(f"Optimization failed: {prob.status}")
        return [], pd.DataFrame()

    w_values = w.value
    selected_indices = [i for i in range(n) if w_values[i] > 0.5]
    selected_players = stats_df.iloc[selected_indices]['player'].tolist()

    weights = pd.DataFrame({
        'player': stats_df['player'],
        'weight': w_values
    })

    return selected_players, weights

# def optimize_team_advanced(stats_df, cov_matrix, num_players=11, boolean=True, risk_aversion =1):
#     """
#     Advanced optimization using alternative objectives beyond quadratic programming.
#     """
#     import pulp
#     import numpy as np
#     from scipy.stats import entropy
    
#     # Initialize PuLP problem (Linear Programming)
#     prob = pulp.LpProblem("FantasyTeam", pulp.LpMaximize)
    
#     # Decision variables
#     players = list(range(len(stats_df)))
#     x = pulp.LpVariable.dicts("select", players, cat='Binary')
    
#     # Parameters
#     mu = stats_df['mean_points'].values
#     std_dev = np.sqrt(np.diag(cov_matrix))
    
#     # Calculate additional metrics
#     consistency = mu / std_dev  # Sharpe-like ratio for each player
#     entropy_score = entropy(mu / sum(mu))  # Diversity in scoring
    
#     # 1. Expected Points Term
#     prob += pulp.lpSum([mu[i] * x[i] for i in players])
    
#     # 2. Team Size Constraint
#     prob += pulp.lpSum([x[i] for i in players]) == num_players
    
#     # 3. Consistency Constraint 
#     prob += pulp.lpSum([consistency[i] * x[i] for i in players]) >= np.mean(consistency) * num_players/2
    
#     # 4. Entropy-based Diversity
#     prob += pulp.lpSum([entropy_score * x[i] for i in players]) >= entropy_score * num_players/2
    
#     # Additional Constraints based on historical performance patterns
#     recent_form = np.percentile(mu, 75)  # Top 25% performers
#     prob += pulp.lpSum([x[i] for i in players if mu[i] >= recent_form]) >= num_players/3
    
#     # Solve the problem
#     prob.solve()
    
#     # Extract results
#     selected_indices = [i for i in players if x[i].value() > 0.5]
#     selected_players = stats_df.iloc[selected_indices]['player'].tolist()
    
#     # Create weights DataFrame
#     weights = pd.DataFrame({
#         'player': stats_df['player'],
#         'weight': [x[i].value() if i in selected_indices else 0 for i in range(len(stats_df))]
#     })
    
#     return selected_players, weights
def optimize_team_advanced(stats_df, cov_matrix, num_players=11, boolean=True, risk_aversion=1):
    """
    Advanced optimization with minimum one player per team constraint.
    """
    
    
    # Initialize PuLP problem
    prob = pulp.LpProblem("FantasyTeam", pulp.LpMaximize)
    
    # Decision variables
    players = list(range(len(stats_df)))
    x = pulp.LpVariable.dicts("select", players, cat='Binary')
    
    # Parameters
    mu = stats_df['mean_points'].values
    std_dev = np.sqrt(np.diag(cov_matrix))
    
    # Get unique teams
    teams = stats_df['team'].unique()  # Assuming 'team' column exists in stats_df
    
    # Calculate additional metrics
    consistency = mu / std_dev
    entropy_score = entropy(mu / sum(mu))
    
    # Objective: Expected Points
    prob += pulp.lpSum([mu[i] * x[i] for i in players])
    
    # Existing constraints
    prob += pulp.lpSum([x[i] for i in players]) == num_players  # Team size
    prob += pulp.lpSum([consistency[i] * x[i] for i in players]) >= np.mean(consistency) * num_players/2  # Consistency
    prob += pulp.lpSum([entropy_score * x[i] for i in players]) >= entropy_score * num_players/2  # Diversity
    
    # Recent form constraint
    recent_form = np.percentile(mu, 75)
    prob += pulp.lpSum([x[i] for i in players if mu[i] >= recent_form]) >= num_players/3
    
    # New constraint: At least one player per team
    for team in teams:
        team_players_indices = [i for i, p in enumerate(players) 
                              if stats_df.iloc[i]['team'] == team]
        prob += pulp.lpSum([x[i] for i in team_players_indices]) >= 1
    
    # Solve
    prob.solve()
    
    # Results
    selected_indices = [i for i in players if x[i].value() > 0.5]
    selected_players = stats_df.iloc[selected_indices]['player'].tolist()
    
    weights = pd.DataFrame({
        'player': stats_df['player'],
        'weight': [x[i].value() if i in selected_indices else 0 for i in range(len(stats_df))]
    })
    
    return selected_players, weights
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
  selected_players, weights = optimize_team_sharpe(stats_df, cov_matrix, risk_tolerance=risk_tolerance)

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
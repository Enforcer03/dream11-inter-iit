import numpy as np
import pandas as pd
import json
import re
import datetime
import cvxpy as cp
import pulp
from scipy.stats import entropy
from typing import List, Dict, Tuple, Union
from utils import get_past_match_performance

def load_player_fantasy_points_for_optimization(json_file: str) -> Dict:
    """
    Loads and sorts player fantasy points data chronologically.
    
    Logic:
    1. Reads JSON file containing player match data
    2. For each player's matches, extracts dates using regex
    3. Sorts matches chronologically using datetime parsing
    4. Returns reconstructed dictionary with sorted matches
    
    Args:
        json_file (str): Path to JSON file with player fantasy points
    
    Returns:
        Dict: Player data with chronologically sorted matches
    """
    with open(json_file, "r") as file:
        data = json.load(file)
        sorted_data = {}
        for player, matches in data.items():
            match_list = list(matches.items())
            match_list_sorted = sorted(
                match_list,
                key=lambda x: datetime.datetime.strptime(
                    re.search(r'(\d{4}-\d{2}-\d{2})', x[0]).group(1),
                    '%Y-%m-%d'
                ) if re.search(r'(\d{4}-\d{2}-\d{2})', x[0]) else datetime.datetime.min
            )
            sorted_data[player] = dict(match_list_sorted)
        return sorted_data

def compute_player_stats(fantasy_points: Dict, players: List[str], 
                        num_matches: int = 50, date_of_match: str = None, 
                        key: str = 'total_points') -> pd.DataFrame:
    """
    Computes mean and variance of fantasy points for each player.
    
    Logic:
    1. For each player, retrieves last N matches performance
    2. Calculates mean and variance of points
    3. Handles missing data by computing stats on available matches
    
    Args:
        fantasy_points (Dict): Historical fantasy points data
        players (List[str]): List of player names
        num_matches (int): Number of past matches to consider
        date_of_match (str): Optional cutoff date
        key (str): Key for points data in match info
    
    Returns:
        pd.DataFrame: DataFrame with player statistics (mean_points, variance)
    """
    stats_list = []
    for player in players:
        matches, points = get_past_match_performance(
            player, fantasy_points, num_matches, key, date_of_match
        )
        if points:
            mean_points = np.mean(points)
            variance_points = np.var(points)
            stats_list.append({
                'player': player,
                'mean_points': mean_points,
                'variance': variance_points
            })
    
    return pd.DataFrame(stats_list)

def compute_covariance_matrix(fantasy_points: Dict, players: List[str], 
                            num_matches: int = 100, 
                            date_of_match: str = None) -> pd.DataFrame:
    """
    Computes covariance matrix of player performances.
    
    Logic:
    1. Creates time series of player points
    2. Handles missing data by using mean imputation
    3. Computes covariance matrix using pandas
    
    Args:
        fantasy_points (Dict): Historical fantasy points data
        players (List[str]): List of player names
        num_matches (int): Number of past matches to consider
        date_of_match (str): Optional cutoff date
    
    Returns:
        pd.DataFrame: Covariance matrix of player performances
    """
    time_series_data = {}
    for player in players:
        matches, points = get_past_match_performance(
            player, fantasy_points, num_matches, 'total_points', date_of_match
        )
        time_series_data[player] = points if points else [np.mean(points)] * num_matches

    return pd.DataFrame(time_series_data).cov()

def optimize_team_sharpe(stats_df: pd.DataFrame, cov_matrix: Union[pd.DataFrame, np.ndarray], 
                        num_players: int = 11, risk_aversion: float = 1.0, 
                        boolean: bool = True) -> Tuple[List[str], pd.DataFrame]:
    """
    Optimizes team selection using Sharpe ratio approach with CVXPY.
    
    Logic:
    1. Sets up CVXPY optimization problem with binary variables
    2. Maximizes expected points while penalizing risk
    3. Ensures positive semidefinite covariance matrix
    4. Attempts multiple solvers if primary solver fails
    
    Args:
        stats_df (pd.DataFrame): Player statistics
        cov_matrix (Union[pd.DataFrame, np.ndarray]): Covariance matrix
        num_players (int): Target team size
        risk_aversion (float): Risk aversion parameter
        boolean (bool): Whether to use binary variables
    
    Returns:
        Tuple[List[str], pd.DataFrame]: Selected players and weights
    """
    n = len(stats_df)
    w = cp.Variable(n, boolean=boolean)
    
    mu = stats_df['mean_points'].values
    Sigma = cov_matrix.values if isinstance(cov_matrix, pd.DataFrame) else cov_matrix
    
    Sigma = (Sigma + Sigma.T) / 2
    min_eig = np.min(np.real(np.linalg.eigvals(Sigma)))
    if min_eig < 0:
        Sigma -= 1.1 * min_eig * np.eye(Sigma.shape[0])
    
    objective = cp.Maximize(mu @ w - risk_aversion * cp.quad_form(w, Sigma))
    constraints = [cp.sum(w) == num_players]
    prob = cp.Problem(objective, constraints)
    
    for solver in [cp.GUROBI, cp.CBC, cp.SCS]:
        try:
            prob.solve(solver=solver, verbose=True)
            break
        except:
            continue
    
    if prob.status not in ["optimal", "optimal_inaccurate"]:
        return [], pd.DataFrame()
    
    w_values = w.value
    selected_indices = [i for i in range(n) if w_values[i] > 0.5]
    selected_players = stats_df.iloc[selected_indices]['player'].tolist()
    
    return selected_players, pd.DataFrame({
        'player': stats_df['player'],
        'weight': w_values
    })

def optimize_team_advanced(stats_df: pd.DataFrame, cov_matrix: np.ndarray, 
                         num_players: int = 11, boolean: bool = True, 
                         risk_aversion: float = 1,
                         consistency_threshold: float = 0.5,
                         diversity_threshold: float = 0.5,
                         form_threshold: float = 0.333,
                         quantile_form = 75
                         ) -> Tuple[List[str], pd.DataFrame]:
    """
    Advanced team optimization with configurable constraints using PuLP.
    Falls back to selecting top players by expected score if optimization fails.
    
    """
    
    prob = pulp.LpProblem("FantasyTeam", pulp.LpMaximize)
    players = list(range(len(stats_df)))
    x = pulp.LpVariable.dicts("select", players, cat='Binary')
    
    
    mu = stats_df['mean_points'].values
    std_dev = np.sqrt(np.diag(cov_matrix))
    
    with np.errstate(divide='ignore', invalid='ignore'):
        consistency = np.where(std_dev > 0, mu / std_dev, 0)
    consistency = np.nan_to_num(consistency, nan=0.0, 
                              posinf=np.nanmax(consistency[~np.isinf(consistency)]))
    
    total_mu = np.sum(mu)
    entropy_score = entropy(mu / total_mu) if total_mu > 0 else 0
    
    # Objective: maximize expected points
    prob += pulp.lpSum([mu[i] * x[i] for i in players])
    
    # Constraint 1: Team size
    prob += pulp.lpSum([x[i] for i in players]) == num_players
    
    # Constraint 2: Consistency
    valid_consistency = consistency[~np.isnan(consistency) & ~np.isinf(consistency)]
    if len(valid_consistency) > 0:
        mean_consistency = np.mean(valid_consistency)
        prob += pulp.lpSum([consistency[i] * x[i] for i in players]) >= (
            consistency_threshold * num_players * mean_consistency
        )
    
    # Constraint 3: Diversity
    if entropy_score > 0:
        prob += pulp.lpSum([entropy_score * x[i] for i in players]) >= (
            diversity_threshold * num_players * entropy_score
        )
    
    # Constraint 4: Form
    valid_mu = mu[~np.isnan(mu) & ~np.isinf(mu)]
    if len(valid_mu) > 0:
        recent_form = np.percentile(valid_mu, quantile_form)  # Q₇₅
        high_form_players = [i for i in players if mu[i] >= recent_form]
        if high_form_players:
            prob += pulp.lpSum([x[i] for i in high_form_players]) >= (
                form_threshold * num_players
            )
    
    # Constraint 5: Team representation
    for team in stats_df['team'].unique():
        team_players_indices = [i for i, p in enumerate(players) 
                              if stats_df.iloc[i]['team'] == team]
        if team_players_indices:
            prob += pulp.lpSum([x[i] for i in team_players_indices]) >= 1
    
    # Solve with suppressed output
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    
    # If optimization fails, fall back to top players by expected score
    if prob.status != pulp.LpStatusOptimal:
        print(f"Warning: Optimization failed with status {pulp.LpStatus[prob.status]} Falling back to top players by expected score")
        team_players = {}
        remaining_slots = num_players
        selected_indices = []
        
        # First, get the best player from each team
        for team in stats_df['team'].unique():
            team_df = stats_df[stats_df['team'] == team]
            if not team_df.empty:
                best_player_idx = team_df['mean_points'].idxmax()
                selected_indices.append(best_player_idx)
                team_players[team] = [best_player_idx]
                remaining_slots -= 1
        
        # Then fill remaining slots with best remaining players
        if remaining_slots > 0:
            remaining_players_df = stats_df.drop(selected_indices)
            top_remaining = remaining_players_df.nlargest(remaining_slots, 'mean_points')
            selected_indices.extend(top_remaining.index)
        
        selected_players = stats_df.loc[selected_indices, 'player'].tolist()
        
        # Create weights DataFrame
        weights = pd.DataFrame({
            'player': stats_df['player'],
            'weight': [1 if i in selected_indices else 0 for i in range(len(stats_df))]
        })
        
        return selected_players, weights
    
    # If optimization succeeded, return original results
    selected_indices = [i for i in players if x[i].value() > 0.5]
    selected_players = stats_df.iloc[selected_indices]['player'].tolist()


    
    return selected_players, pd.DataFrame({
        'player': stats_df['player'],
        'weight': [x[i].value() if i in selected_indices else 0 
                  for i in range(len(stats_df))]
    })


## This function include the risk aversion factor properly

def optimize_team_advanced_test(stats_df: pd.DataFrame, cov_matrix: np.ndarray, 
                         num_players: int = 11, boolean: bool = True, 
                         risk_aversion: float = 0.1,
                         consistency_threshold: float = 0.5,
                         diversity_threshold: float = 0.5,
                         form_threshold: float = 0.333,
                         quantile_form = 75
                         ) -> Tuple[List[str], pd.DataFrame]:
    """
    Advanced team optimization with configurable constraints using PuLP.
    Incorporates risk aversion in the objective function.
    Falls back to selecting top players by expected score if optimization fails.
    """
    
    prob = pulp.LpProblem("FantasyTeam", pulp.LpMaximize)
    players = list(range(len(stats_df)))
    x = pulp.LpVariable.dicts("select", players, cat='Binary')
    
    mu = stats_df['mean_points'].values
    std_dev = np.sqrt(np.diag(cov_matrix))
    
    with np.errstate(divide='ignore', invalid='ignore'):
        consistency = np.where(std_dev > 0, mu / std_dev, 0)
    consistency = np.nan_to_num(consistency, nan=0.0, 
                              posinf=np.nanmax(consistency[~np.isinf(consistency)]))
    
    total_mu = np.sum(mu)
    entropy_score = entropy(mu / total_mu) if total_mu > 0 else 0
    
    # Modified Objective: maximize expected points while penalizing risk
    # Higher risk_aversion means more weight on minimizing variance
    prob += pulp.lpSum([mu[i] * x[i] for i in players]) - \
            risk_aversion * pulp.lpSum([std_dev[i] * x[i] for i in players])
    
    # Constraint 1: Team size
    prob += pulp.lpSum([x[i] for i in players]) == num_players
    
    # Constraint 2: Consistency (modified with risk aversion)
    valid_consistency = consistency[~np.isnan(consistency) & ~np.isinf(consistency)]
    if len(valid_consistency) > 0:
        mean_consistency = np.mean(valid_consistency)
        adjusted_threshold = consistency_threshold   
        prob += pulp.lpSum([consistency[i] * x[i] for i in players]) >= (
            adjusted_threshold * num_players * mean_consistency
        )
    
    # Constraint 3: Diversity
    if entropy_score > 0:
        prob += pulp.lpSum([entropy_score * x[i] for i in players]) >= (
            diversity_threshold * num_players * entropy_score
        )
    
    # Constraint 4: Form (modified with risk aversion)
    valid_mu = mu[~np.isnan(mu) & ~np.isinf(mu)]
    if len(valid_mu) > 0:
        # Adjust form percentile based on risk aversion
        adjusted_quantile = min(quantile_form, 90)  # Lower percentile for higher risk aversion
        recent_form = np.percentile(valid_mu, adjusted_quantile)
        high_form_players = [i for i in players if mu[i] >= recent_form]
        if high_form_players:
            adjusted_form_threshold = form_threshold * (1)  # Increase threshold with risk aversion
            prob += pulp.lpSum([x[i] for i in high_form_players]) >= (
                adjusted_form_threshold * num_players
            )
    
    # Constraint 5: Team representation
    for team in stats_df['team'].unique():
        team_players_indices = [i for i, p in enumerate(players) 
                              if stats_df.iloc[i]['team'] == team]
        if team_players_indices:
            prob += pulp.lpSum([x[i] for i in team_players_indices]) >= 1
    
    # Solve with suppressed output
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    
    # Rest of the code remains the same
    if prob.status != pulp.LpStatusOptimal:
        print(f"Warning: Optimization failed with status {pulp.LpStatus[prob.status]} Falling back to top players by expected score")
        team_players = {}
        remaining_slots = num_players
        selected_indices = []
        
        for team in stats_df['team'].unique():
            team_df = stats_df[stats_df['team'] == team]
            if not team_df.empty:
                best_player_idx = team_df['mean_points'].idxmax()
                selected_indices.append(best_player_idx)
                team_players[team] = [best_player_idx]
                remaining_slots -= 1
        
        if remaining_slots > 0:
            remaining_players_df = stats_df.drop(selected_indices)
            # Modified fallback to consider risk in player selection
            remaining_players_df['mean_score'] = remaining_players_df['mean_points']
            top_remaining = remaining_players_df.nlargest(remaining_slots, 'mean_score')
            selected_indices.extend(top_remaining.index)
        
        selected_players = stats_df.loc[selected_indices, 'player'].tolist()
        weights = pd.DataFrame({
            'player': stats_df['player'],
            'weight': [1 if i in selected_indices else 0 for i in range(len(stats_df))]
        })
        return selected_players, weights
    
    selected_indices = [i for i in players if x[i].value() > 0.5]
    selected_players = stats_df.iloc[selected_indices]['player'].tolist()
    
    return selected_players, pd.DataFrame({
        'player': stats_df['player'],
        'weight': [x[i].value() if i in selected_indices else 0 
                  for i in range(len(stats_df))]
    })
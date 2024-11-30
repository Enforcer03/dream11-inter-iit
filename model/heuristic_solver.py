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
                         risk_aversion: float = 1) -> Tuple[List[str], pd.DataFrame]:
    """
    Advanced team optimization with multiple constraints using PuLP.
    
    Logic:
    1. Sets up PuLP optimization problem with multiple objectives
    2. Implements constraints for:
       - Team size
       - Team representation
       - Player consistency
       - Team diversity
       - Recent form
    3. Handles numerical instabilities and edge cases
    4. Returns optimal selection with weights
    
    Args:
        stats_df (pd.DataFrame): Player statistics with team information
        cov_matrix (np.ndarray): Covariance matrix
        num_players (int): Target team size
        boolean (bool): Whether to use binary variables
        risk_aversion (float): Risk aversion parameter
    
    Returns:
        Tuple[List[str], pd.DataFrame]: Selected players and weights
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
    
    prob += pulp.lpSum([mu[i] * x[i] for i in players])
    prob += pulp.lpSum([x[i] for i in players]) == num_players
    
    valid_consistency = consistency[~np.isnan(consistency) & ~np.isinf(consistency)]
    if len(valid_consistency) > 0:
        mean_consistency = np.mean(valid_consistency)
        prob += pulp.lpSum([consistency[i] * x[i] for i in players]) >= mean_consistency * num_players/2
    
    if entropy_score > 0:
        prob += pulp.lpSum([entropy_score * x[i] for i in players]) >= entropy_score * num_players/2
    
    valid_mu = mu[~np.isnan(mu) & ~np.isinf(mu)]
    if len(valid_mu) > 0:
        recent_form = np.percentile(valid_mu, 75)
        high_form_players = [i for i in players if mu[i] >= recent_form]
        if high_form_players:
            prob += pulp.lpSum([x[i] for i in high_form_players]) >= num_players/3
    
    for team in stats_df['team'].unique():
        team_players_indices = [i for i, p in enumerate(players) 
                              if stats_df.iloc[i]['team'] == team]
        if team_players_indices:
            prob += pulp.lpSum([x[i] for i in team_players_indices]) >= 1
    
    prob.solve()
    
    if prob.status != pulp.LpStatusOptimal:
        return [], pd.DataFrame(columns=['player', 'weight'])
    
    selected_indices = [i for i in players if x[i].value() > 0.5]
    selected_players = stats_df.iloc[selected_indices]['player'].tolist()
    
    return selected_players, pd.DataFrame({
        'player': stats_df['player'],
        'weight': [x[i].value() if i in selected_indices else 0 
                  for i in range(len(stats_df))]
    })
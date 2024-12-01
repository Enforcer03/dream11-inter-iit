# team_optimizer.py

import pandas as pd
import numpy as np
import datetime
from heuristic_solver import compute_player_stats, compute_covariance_matrix, optimize_team_advanced, optimize_team_sharpe
from utils import load_player_fantasy_points, calculate_team_metrics
import requests
import json

def calculate_optimal_team(player_info, num_matches=50, date_of_match=None, risk_tolerance=1.0, solver='pulp', fantasy_points_data=None):
    """
    Given a list of player names (combined squad), calculates the optimal team.
    Returns selected_players and stats_df.
    """
    # Extract unique player names from player_info
    player_list = []
    for team, players in player_info.items():
        for player in players:
            player_name = player.split(":")[0].strip()
            if player_name not in player_list:  # Only add if not already in list
                player_list.append(player_name)
    
    if fantasy_points_data is None:
        raise ValueError("Fantasy points data must be provided.")

    # Compute player statistics for different point types
    stats_df = compute_player_stats(
        fantasy_points_data,
        player_list,
        num_matches=num_matches,
        date_of_match=date_of_match,
        key='total_points'
    )
    print("before_comp")
    print(stats_df)

    if stats_df.empty:
        print("No player statistics available.")
        return None, stats_df, None

    # Add additional point type statistics
    point_types = {
        'batting_points': 'batting_points',
        'bowling_points': 'bowling_points',
        'fielding_points': 'fielding_points'
    }

    for point_type, column_name in point_types.items():
        type_stats = compute_player_stats(
            fantasy_points_data,
            player_list,
            num_matches=num_matches,
            date_of_match=date_of_match,
            key=point_type
        )
        # Add point type columns to main stats_df
        stats_df[column_name] = type_stats['mean_points']

    # Remove any potential duplicates
    stats_df = stats_df.drop_duplicates(subset=['player'])

    # Compute covariance matrix
    cov_matrix = compute_covariance_matrix(
        fantasy_points_data,
        stats_df['player'].tolist(),
        num_matches=num_matches,
        date_of_match=date_of_match
    )

    # Create team mapping
    player_team_mapping = {}
    for team_name, players in player_info.items():
        for player in players:
            player_name = player.split(" : ")[0].strip()
            if player_name not in player_team_mapping:  # Only add if not already mapped
                player_team_mapping[player_name] = team_name

    stats_df['team'] = stats_df['player'].map(player_team_mapping)

    # Select optimizer based on solver argument
    optimizer = optimize_team_advanced if solver == 'pulp' else optimize_team_sharpe

    # Optimize team selection
    selected_players, weights_df = optimizer(
        stats_df, 
        cov_matrix, 
        risk_aversion=risk_tolerance, 
        boolean=True
    )

    return selected_players, stats_df, cov_matrix

def evaluate_team(selected_players, stats_df, cov_matrix):
    """
    Given a set of 11 players, returns the 'consistency_score', 'diversity_score', and 'form_score'.
    """
    # Create a DataFrame to represent player weights (selection status)
    weights_df = pd.DataFrame({'player': stats_df['player'], 'weight': 0})
    weights_df.loc[weights_df['player'].isin(selected_players), 'weight'] = 1

    # Calculate team metrics
    team_metrics = calculate_team_metrics(stats_df, weights_df, cov_matrix)

    return (
        team_metrics['consistency_score'],
        team_metrics['diversity_score'],
        team_metrics['form_score']
    )


def analyze_player_selection(selected_players, player_name, format_lower='t20'):
    """
    Analyzes why a player was selected or not selected for the optimal team using LLM.
    
    Args:
        stats_df (pd.DataFrame): DataFrame containing player statistics
        selected_players (list): List of selected players for optimal team
        player_name (str): Name of the player to analyze
        format_lower (str): Cricket format (t20, odi, test)
        
    Returns:
        str: LLM analysis of player selection
    """
    # Load aggregate stats
    try:
        aggregate_stats_path = f"../data/aggregate_cricket_stats_{format_lower}.json"
        with open(aggregate_stats_path, 'r') as f:
            aggregate_stats = json.load(f)
    except FileNotFoundError:
        return f"Error: Could not load aggregate statistics for {format_lower} format"
    
    

    player_aggregate_stats = aggregate_stats.get(player_name, {})
    if not player_aggregate_stats:
        return f"Error: No aggregate statistics found for {player_name}"
    
    # Prepare prompt for LLM
    selection_status = "selected" if player_name in selected_players else "not selected"
    
    prompt = f"""
Based on the following statistics, explain why {player_name} was {selection_status} for the optimal fantasy cricket team:

Key Aggregate Statistics:
Batting Statistics:
- Batting Style: {player_aggregate_stats.get('Batting', 'N/A')}
- Total Runs: {player_aggregate_stats.get('Runs', 'N/A')}
- Batting Average: {player_aggregate_stats.get('Batting Avg', 'N/A')}
- Strike Rate: {player_aggregate_stats.get('Batting S/R', 'N/A')}
- Boundary Percentage: {player_aggregate_stats.get('Boundary %', 'N/A')}
- Mean Score: {player_aggregate_stats.get('Mean Score', 'N/A')}
- Dismissal Rate: {player_aggregate_stats.get('Dismissal Rate', 'N/A')}

Bowling Statistics:
- Bowling Style: {player_aggregate_stats.get('Bowling', 'N/A')}
- Wickets: {player_aggregate_stats.get('Wickets', 'N/A')}
- Economy Rate: {player_aggregate_stats.get('Economy Rate', 'N/A')}
- Bowling Average: {player_aggregate_stats.get('Bowling Avg', 'N/A')}
- Bowling Strike Rate: {player_aggregate_stats.get('Bowling S/R', 'N/A')}
- Dot Ball Bowled %: {player_aggregate_stats.get('Dot Ball Bowled %', 'N/A')}
- Boundary Given %: {player_aggregate_stats.get('Boundary Given %', 'N/A')}

Fielding Statistics:
- Catches: {player_aggregate_stats.get('Catches', 'N/A')}
- Runouts: {player_aggregate_stats.get('Runouts', 'N/A')}
- Stumpings: {player_aggregate_stats.get('Stumpings', 'N/A')}

A negative value for an aggregate statistic means that value does not exist and is not be to considered in the analysis.

Please provide a concise and brief analysis of why this player was {selection_status}, considering only their overall cricket statistics. Output the best statistics of the player. Be crisp.
"""

    # Send request to LLM
    url = "https://8001-01jdya9bpnhj5dqyfzh17zdghv.cloudspaces.litng.ai/predict"
    headers = {"Content-Type": "application/json"}
    data = {"input": prompt}

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        analysis = response.json()['output']
        return analysis
    except requests.exceptions.RequestException as e:
        return f"Error querying LLM: {str(e)}"

# Example usage:
# analysis = analyze_player_selection(stats_df, selected_players, "SR Watson")
# print(analysis)


if __name__ == "__main__":
    # Example usage
    player_info ={"Nottinghamshire":["BT Slater : Nottinghamshire","FW McCann : Nottinghamshire","JA Haynes : Nottinghamshire","H Hameed : Nottinghamshire","LW James : Nottinghamshire","TJ Moores : Nottinghamshire","LA Patterson-White : Nottinghamshire","CG Harrison : Nottinghamshire","BA Hutton : Nottinghamshire","R Lord : Nottinghamshire","LJ Fletcher : Nottinghamshire","OJ Price : Nottinghamshire"],"Gloucestershire":["James Bracey : Gloucestershire","GL van Buuren : Gloucestershire","AS Dale : Gloucestershire","CT Bancroft : Gloucestershire","Zaman Akhter : Gloucestershire","OJ Price : Gloucestershire","JMR Taylor : Gloucestershire","TMJ Smith : Gloucestershire","DC Goodman : Gloucestershire","Miles Hammond : Gloucestershire","BG Charlesworth : Gloucestershire"]}    # Load fantasy points data
    fantasy_points_path = "../data/player_fantasy_points_odi.json"
    fantasy_points_data = load_player_fantasy_points(fantasy_points_path)

    # Set match date
    date_of_match = "2024-08-09"

    # Calculate the optimal team
    selected_players, stats_df, cov_matrix = calculate_optimal_team(
        player_info=player_info,
        num_matches=50,
        date_of_match=date_of_match,
        risk_tolerance=1.0,
        solver='pulp',
        fantasy_points_data=fantasy_points_data
    )

    print("\nStats DataFrame:")
    print(stats_df)

    print("\nSelected Players for the Optimal Team:")
    for player in selected_players:
        print(player)

    # Evaluate the selected team
    consistency_score, diversity_score, form_score = evaluate_team(
        selected_players,
        stats_df,
        cov_matrix
    )

    print("\nTeam Evaluation Metrics:")
    print(f"Consistency Score: {consistency_score:.2f}")
    print(f"Diversity Score: {diversity_score:.2f}")
    print(f"Form Score: {form_score:.2f}")

    for player in selected_players:
        print(f"\n{player}:")
        # Analyze each selected player
        analysis = analyze_player_selection( selected_players, player, format_lower='odi')
        print(analysis)
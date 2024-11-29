# team_optimizer.py

import pandas as pd
import numpy as np
import datetime
from heuristic_solver import compute_player_stats, compute_covariance_matrix, optimize_team_advanced, optimize_team_sharpe
from utils import load_player_fantasy_points, calculate_team_metrics

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
        date_of_match=date_of_match
    )

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

if __name__ == "__main__":
    # Example usage
    player_info = {
        "England": [
            "LS Livingstone : England", "MM Ali : England", "SM Curran : England",
            "DJ Willey : England", "CJ Jordan : England", "RJ Gleeson : England",
            "MW Parkinson : England", "JJ Roy : England", "JC Buttler : England",
            "DJ Malan : England", "HC Brook : England"
        ],
        "India": [
            "RG Sharma : India", "RR Pant : India", "V Kohli : India",
            "SA Yadav : India", "HH Pandya : India", "RA Jadeja : India",
            "KD Karthik : India", "HV Patel : India", "B Kumar : India",
            "JJ Bumrah : India", "YS Chahal : India"
        ]
    }

    # Load fantasy points data
    fantasy_points_path = "../data/player_fantasy_points_t20.json"
    fantasy_points_data = load_player_fantasy_points(fantasy_points_path)

    # Set match date
    date_of_match = "2022-07-09"

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
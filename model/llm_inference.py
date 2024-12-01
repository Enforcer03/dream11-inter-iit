import json
import requests
import pandas as pd

from pipeline import calculate_optimal_team
from utils import load_player_fantasy_points, calculate_team_metrics



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


def main():
    # Define player info
    player_info = {
        "Nottinghamshire": [
            "BT Slater : Nottinghamshire", "FW McCann : Nottinghamshire", 
            "JA Haynes : Nottinghamshire", "H Hameed : Nottinghamshire",
            "LW James : Nottinghamshire", "TJ Moores : Nottinghamshire",
            "LA Patterson-White : Nottinghamshire", "CG Harrison : Nottinghamshire",
            "BA Hutton : Nottinghamshire", "R Lord : Nottinghamshire",
            "LJ Fletcher : Nottinghamshire", "OJ Price : Nottinghamshire"
        ],
        "Gloucestershire": [
            "James Bracey : Gloucestershire", "GL van Buuren : Gloucestershire",
            "AS Dale : Gloucestershire", "CT Bancroft : Gloucestershire",
            "Zaman Akhter : Gloucestershire", "OJ Price : Gloucestershire",
            "JMR Taylor : Gloucestershire", "TMJ Smith : Gloucestershire",
            "DC Goodman : Gloucestershire", "Miles Hammond : Gloucestershire",
            "BG Charlesworth : Gloucestershire"
        ]
    }

    # Load fantasy points data
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

    if selected_players is None:
        print("Failed to calculate optimal team")
        return

    print("\nSelected Players:")
    for player in selected_players:
        print(f"\n{player}:")
        # Analyze each selected player
        analysis = analyze_player_selection( selected_players, player, format_lower='odi')
        print(analysis)

    print("\nNon-Selected Players Analysis:")
    # Get all players who weren't selected
    all_players = []
    for team_players in player_info.values():
        for player in team_players:
            player_name = player.split(" : ")[0].strip()
            if player_name not in all_players:
                all_players.append(player_name)

    non_selected = [p for p in all_players if p not in selected_players]
    
    for player in non_selected:
        print(f"\n{player}:")
        # Analyze each non-selected player
        analysis = analyze_player_selection(selected_players, player, format_lower='odi')
        print(analysis)

if __name__ == "__main__":
    main()
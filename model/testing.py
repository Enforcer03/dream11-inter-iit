import json
from calculator_test import calculate_fantasy_points_test

# Path to the input JSON file containing player match data
# assuming running from the root directory
file_path = './model/player_match_test_data.json'

# Load the player match data from the file
with open(file_path, 'r') as file:
    player_data = json.load(file)

# Initialize a dictionary to store fantasy points for each player and each match
fantasy_points = {}

# Loop through each player and their respective match data
for player, matches in player_data.items():
    fantasy_points[player] = {}
    
    for match_id, stats in matches.items():
        # Calculate points for each match using the existing function
        points = calculate_fantasy_points_test(stats)
        
        # Include the relevant statistics in the output dictionary
        extended_stats = {
            "total_points": points["total_points"],
            "batting_points": points["batting_points"],
            "bowling_points": points["bowling_points"],
            "fielding_points": points["fielding_points"],
            
            # Numeric Statistics from provided data
            "total_runs": stats.get("Total Runs Scored"),
            "avg_runs_per_inning": stats.get("Avg Runs Per Inning"),
            "boundaries": stats.get("Boundaries"),
            "sixes": stats.get("Sixes"),
            "average_sixes_per_inning": stats.get("Average Sixes Per Inning"),
            "fours": stats.get("Fours"),
            "average_fours_per_inning": stats.get("Average Fours Per Inning"),
            "boundary_percent_per_inning": stats.get("Boundary% Per Inning"),
            # "boundary_rate_per_inning": stats.get("Boundary Rate Per Inning"),
            "wickets": stats.get("Wickets"),
            "avg_wickets_per_inning": stats.get("Avg Wickets Per Inning"),
            "catches_taken": stats.get("Catches Taken"),
            "stumped_outs_made": stats.get("Stumped Outs Made"),
            "run_outs_made": stats.get("Run Outs Made"),
            "balls_faced": stats.get("Balls Faced"),
            "avg_balls_faced_per_inning": stats.get("Avg Balls Faced Per Inning"),
            "avg_batting_sr_per_inning": stats.get("Avg Batting S/R Per Inning"),
            "avg_runs_ball_per_inning": stats.get("Avg Runs/Ball Per Inning"),
            "overs_bowled": stats.get("Overs Bowled"),
            "bowls_bowled": stats.get("Bowls Bowled"),
            "average_bowls_bowled_per_inning": stats.get("Average Bowls Bowled Per Inning"),
            "avg_economy_rate_per_inning": stats.get("Avg Economy Rate per inning"),
            # "bowling_average": stats.get("Bowling Average"),
            "average_consecutive_dot_balls": stats.get("*Average Consecutive Dot Balls"),
            # "bowling_sr": stats.get("Bowling S/R"),
            "runs_given": stats.get("Runs Given"),
            "runs_given_ball_per_inning": stats.get("RunsGiven/Ball Per Inning"),
            "batting_sr_aa": stats.get("*Batting S/R AA(Above Average)")
        }

        # Store the extended stats and points for the player
        fantasy_points[player][match_id] = extended_stats

# Optionally, write the results to a new JSON file
output_path = './player_fantasy_points_test.json'
with open(output_path, 'w') as outfile:
    json.dump(fantasy_points, outfile, indent=4)
print("saved the fantasy points")


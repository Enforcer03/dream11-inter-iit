import json
from calculator import calculate_fantasy_points_t20
from calculate_odi import calculate_fantasy_points_odi
from calculator_test import calculate_fantasy_points_test
from tqdm import tqdm

def process_match_data(match_data_path, aggregate_data_path, output_path):
    """
    Process match data and calculate fantasy points for all formats
    
    Args:
        match_data_path (str): Path to combined player match data JSON
        aggregate_data_path (str): Path to aggregate data JSON
        output_path (str): Path to save output JSON
    """
    # Load both data files
    try:
        with open(match_data_path, 'r') as file:
            player_data = json.load(file)
        
        with open(aggregate_data_path, 'r') as file:
            aggregate_data = json.load(file)
    except Exception as e:
        print(f"Error loading input files: {str(e)}")
        return

    # Initialize fantasy points dictionary
    fantasy_points = {}

    # Loop through each player and their respective match data
    for player, matches in tqdm(player_data.items(), desc="Processing players"):
        fantasy_points[player] = {}
        player_aggregate_stats = aggregate_data.get(player, {})
        
        for match_id, stats in matches.items():
            # Determine format and calculate points
            if match_id[-3:] == "T20":
                points = calculate_fantasy_points_t20(stats)
            elif match_id[-4:] == "Test" or match_id[-3:] == "MDM":
                points = calculate_fantasy_points_test(stats)
            elif match_id[-3:] == "ODI" or match_id[-3:] == "ODM":
                points = calculate_fantasy_points_odi(stats)
            else:
                print(f"Unknown format for match_id: {match_id}")
                continue

            # Combine all stats into a single level dictionary
            extended_stats = {
                # Fantasy points
                "total_points": points["total_points"],
                "batting_points": points["batting_points"],
                "bowling_points": points["bowling_points"],
                "fielding_points": points["fielding_points"],
                
                # Match Statistics
                "venue": stats.get("Venue"),
                "opponent": stats.get("Opposition Team"),
                "total_runs": stats.get("Total Runs Scored"),
                "avg_runs_per_inning": stats.get("Avg Runs Per Inning"),
                "boundaries": stats.get("Boundaries"),
                "sixes": stats.get("Sixes"),
                "average_sixes_per_inning": stats.get("Average Sixes Per Inning"),
                "fours": stats.get("Fours"),
                "average_fours_per_inning": stats.get("Average Fours Per Inning"),
                "boundary_percent_per_inning": stats.get("Boundary% Per Inning"),
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
                "average_consecutive_dot_balls": stats.get("*Average Consecutive Dot Balls"),
                "runs_given": stats.get("Runs Given"),
                "runs_given_ball_per_inning": stats.get("RunsGiven/Ball Per Inning"),
                "batting_sr_aa": stats.get("*Batting S/R AA(Above Average)"),
                
                # Add all aggregate stats
                **player_aggregate_stats
            }
            
            fantasy_points[player][match_id] = extended_stats

    # Write the results to output file
    try:
        with open(output_path, 'w') as outfile:
            json.dump(fantasy_points, outfile, indent=4)
        print(f"Successfully saved fantasy points to {output_path}")
    except Exception as e:
        print(f"Error saving output file: {str(e)}")

def main():
    # Process T20 data
    print("\nProcessing T20 data...")
    process_match_data(
        '../data/interim/T20_player_match_data.json',
        '../data/processed/T20_aggregate_data.json',
        '../data/processed/player_fantasy_points_t20.json'
    )
    
    # Process ODI/ODM data
    print("\nProcessing ODI/ODM data...")
    process_match_data(
        '../data/interim/ODI_ODM_player_match_data.json',
        '../data/processed/ODI_ODM_aggregate_data.json',
        '../data/processed/player_fantasy_points_odi.json'
    )
    
    # Process MDM Test data
    print("\nProcessing MDM Test data...")
    process_match_data(
        '../data/interim/Test_MDM_player_match_data.json',
        '../data/processed/Test_MDM_aggregate_data.json',
        '../data/processed/player_fantasy_points_test.json'
    )

if __name__ == "__main__":
    main()
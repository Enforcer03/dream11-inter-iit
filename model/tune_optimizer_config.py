import streamlit as st
import openai
import json
import os
from dotenv import load_dotenv
import plotly.graph_objects as go
import datetime
import re
import numpy as np
import scipy.stats as stats
from heuristic_solver import compute_player_stats, compute_covariance_matrix, optimize_team_advanced,load_player_fantasy_points_for_optimization
import pandas as pd
from tqdm import tqdm

from itertools import product
from tqdm.auto import tqdm
import os
import datetime
import threading
from typing import Dict, List

def extract_date_from_match_key(match_key):
  date_pattern = r'(\d{4}-\d{2}-\d{2})'
  match = re.search(date_pattern, match_key)
  if match:
      return match.group(1)
  else:
      return None


def get_team_selection_snapshot(match_keys, match_data, fantasy_points, 
                           optim_fantasy_points_t20, optim_fantasy_points_odi, 
                           optim_fantasy_points_test, num_matches=50,
                           from_date=None, to_date=None, consistency_threshold= 0.5, diversity_threshold =0.5, form_threshold =0.3333, quantile_form =75):
    """
    Generate a CSV snapshot of team selections for a specified date range and match count
    
    Parameters:
    match_keys (list): List of match identifiers
    match_data (dict): Dictionary containing match data
    fantasy_points (dict): Dictionary containing fantasy points data
    optim_fantasy_points_t20 (dict): Dictionary containing optimized fantasy points for T20
    optim_fantasy_points_odi (dict): Dictionary containing optimized fantasy points for ODI
    optim_fantasy_points_test (dict): Dictionary containing optimized fantasy points for Test
    num_matches (int): Number of past matches to consider for computing statistics (default: 50)
    from_date (str): Start date in 'YYYY-MM-DD' format (inclusive)
    to_date (str): End date in 'YYYY-MM-DD' format (inclusive)
    
    Returns:
    pd.DataFrame: DataFrame containing team selections and scores
    """
    snapshot_data = []
    
    # Convert date strings to datetime objects if provided
    from_date_dt = None
    to_date_dt = None
    
    if from_date:
        try:
            from_date_dt = datetime.datetime.strptime(from_date, '%Y-%m-%d').date()
        except ValueError:
            print(f"Invalid from_date format: {from_date}. Using no start date filter.")
            
    if to_date:
        try:
            to_date_dt = datetime.datetime.strptime(to_date, '%Y-%m-%d').date()
        except ValueError:
            print(f"Invalid to_date format: {to_date}. Using no end date filter.")
        print(len(match_keys))
        print(len(list(set(match_keys))))
    
    for match_key in tqdm(match_keys):
        # Extract date string from match key
        match_date_str = extract_date_from_match_key(match_key)
        if not match_date_str:
            continue
            
        try:
            match_date = datetime.datetime.strptime(match_date_str, '%Y-%m-%d').date()
        except ValueError:
            continue
            
        # Apply date range filters
        if from_date_dt and match_date < from_date_dt:
            continue
        if to_date_dt and match_date > to_date_dt:
            continue
        
        # Determine match format from key suffix
        if match_key.endswith('T20'):
            optim_fantasy_points = optim_fantasy_points_t20
        elif match_key.endswith('ODM') or  match_key.endswith('ODI'):
            optim_fantasy_points = optim_fantasy_points_odi
        elif match_key.endswith('Test') or match_key.endswith('MDM'):
            optim_fantasy_points = optim_fantasy_points_test
        else:
            print(f"Unknown format for match: {match_key}")
            continue
        
        # Get squads for the match
        squads = match_data[match_key]
        all_players = []
        player_team_mapping = {}
        
        # Create player list and team mapping
        for team_name, players in squads.items():
            all_players.extend(players)
            for player in players:
                player_name = player.split(" : ")[0].strip()
                player_team_mapping[player_name] = team_name
                
        # Remove duplicates while preserving order
        all_players = list(dict.fromkeys(all_players))
        
        # Get player stats and optimize team using specified number of matches
        stats_df = compute_player_stats(
            optim_fantasy_points,
            list(all_players),
            num_matches=num_matches,
            date_of_match=match_date_str
        )
        
        if not stats_df.empty:
            # Compute covariance matrix using specified number of matches
            cov_matrix = compute_covariance_matrix(
                optim_fantasy_points,
                stats_df['player'].tolist(),
                num_matches=num_matches,
                date_of_match=match_date_str
            )
            
            # Add team information
            stats_df['team'] = stats_df['player'].map(player_team_mapping)
            
            # Optimize team using advanced optimizer
            selected_players, weights_df = optimize_team_advanced(
                stats_df, 
                cov_matrix,
                boolean=True,
                consistency_threshold=consistency_threshold,
                diversity_threshold=diversity_threshold,
                form_threshold=form_threshold
            )
            
            if weights_df is not None and not weights_df.empty:
                # Merge weights with stats
                weights_df_display = weights_df.merge(
                    stats_df[['player', 'mean_points', 'variance']],
                    on='player',
                    how='left'
                )
                
                # Calculate team metrics
                total_expected_score = (weights_df_display['weight'] * weights_df_display['mean_points']).sum()
                
                # Calculate team variance and standard deviation
                selected_indices = [stats_df.index[stats_df['player'] == player].tolist()[0] 
                                 for player in selected_players]
                selected_cov = cov_matrix.iloc[selected_indices, selected_indices]
                weights = np.ones(len(selected_players))
                team_variance = weights.dot(selected_cov).dot(weights)
                team_std = np.sqrt(team_variance)
                
                # Calculate actual points for the match
                actual_points = sum(
                    optim_fantasy_points.get(player, {}).get(match_key, {}).get('total_points', 0)
                    for player in selected_players
                )
                
                # Get top 11 players by actual points
                player_points = {
                    player: optim_fantasy_points.get(player, {}).get(match_key, {}).get('total_points', 0)
                    for player in all_players
                }
                top_11_by_actual = (pd.DataFrame(list(player_points.items()), 
                                               columns=['player', 'actual_points'])
                                  .nlargest(11, 'actual_points'))
                optimal_score = top_11_by_actual['actual_points'].sum()
                
                # Create row data
                row_data = {
                    'match_name': match_key,
                    'match_date': match_date_str,
                    'format': 'T20' if match_key.endswith('T20') else 'ODI' if match_key.endswith('ODM') else 'Test',
                    'predicted_score': total_expected_score,
                    'predicted_std': team_std,
                    'actual_score': actual_points,
                    'optimal_score': optimal_score,
                    'performance_ratio': actual_points / optimal_score if optimal_score > 0 else 0,
                    'num_matches_used': num_matches  # Added for tracking
                }
                
                # Add selected players and their predicted scores
                for i, player in enumerate(selected_players, 1):
                    player_stats = stats_df[stats_df['player'] == player]
                    if not player_stats.empty:
                        row_data[f'Player{i}'] = player
                        row_data[f'Predicted_score{i}'] = player_stats['mean_points'].iloc[0]
                
                # Add top performers and their actual scores
                for i, (_, row) in enumerate(top_11_by_actual.iterrows(), 1):
                    row_data[f'Top_player{i}'] = row['player']
                    row_data[f'Top_score{i}'] = row['actual_points']
                
                snapshot_data.append(row_data)
    
    # Create final DataFrame and sort by date
    snapshot_df = pd.DataFrame(snapshot_data)
    if not snapshot_df.empty:
        snapshot_df = snapshot_df.sort_values(
            by='match_date',
            key=lambda x: pd.to_datetime(x)
        )
    
    return snapshot_df




def run_optimization_cv(match_keys: List[str], 
                       match_data: Dict,
                       fantasy_points: Dict,
                       optim_fantasy_points_t20: Dict,
                       optim_fantasy_points_odi: Dict,
                       optim_fantasy_points_test: Dict,
                       output_file: str = 'optimization_cv_results.json'):
    """
    Run cross-validation style analysis for team optimization parameters.
    
    Parameters:
        match_keys: List of match identifiers
        match_data: Dictionary containing match data
        fantasy_points: Dictionary containing fantasy points data
        optim_fantasy_points_t20: Dictionary containing optimized fantasy points for T20
        optim_fantasy_points_odi: Dictionary containing optimized fantasy points for ODI
        optim_fantasy_points_test: Dictionary containing optimized fantasy points for Test
        output_file: Path to store results JSON
    """
    # Define parameter ranges
    num_matches_range = range(20,81,20)
    consistency_range = [0.5]
    quantile_range = [ 40,50, 60, 70, 80]
    diversity_range = [0.5]
    
    # Initialize results storage
    try:
        with open(output_file, 'r') as f:
            results = json.load(f)
            print(f"Loaded {len(results)} existing results")
    except (FileNotFoundError, json.JSONDecodeError):
        results = {}
        print("Starting new results file")
    
    def calculate_metrics(snapshot_df):
        """Calculate performance metrics from snapshot DataFrame."""
        if snapshot_df.empty:
            return {
                'performance_ratio_mean': 0,
                'performance_ratio_std': 0,
                'optimal_mae': 0,
                'expected_mae': 0,
                'num_matches_processed': 0
            }
            
        metrics = {
            'performance_ratio_mean': float(snapshot_df['performance_ratio'].mean()),
            'performance_ratio_std': float(snapshot_df['performance_ratio'].std()),
            'optimal_mae': float(np.mean(np.abs(snapshot_df['optimal_score'] - snapshot_df['actual_score']))),
            'expected_mae': float(np.mean(np.abs(snapshot_df['predicted_score'] - snapshot_df['actual_score']))),
            'num_matches_processed': len(snapshot_df)
        }
        return metrics
    
    # Total iterations for progress bar
    total_iterations = (len(num_matches_range) * 
                       len(consistency_range) * 
                       len(quantile_range) * 
                       len(diversity_range))
    print(f"Total experiments to run: {total_iterations}")
    
    # Run optimization for each parameter combination
    for nm in tqdm(num_matches_range, desc="Num Matches"):
        for cons in consistency_range:
            for quantile in quantile_range:
                for div in diversity_range:
                    # Generate experiment key
                    exp_key = f"nm{nm}_c{cons:.2f}_q{quantile:.3f}_d{div:.2f}"
                    
                    # Skip if already processed
                    if exp_key in results:
                        print(f"Skipping existing experiment: {exp_key}")
                        continue
                    
                    try:
                        print(f"\nRunning experiment: {exp_key}")
                        
                        # Run team selection with current parameters
                        snapshot_df = get_team_selection_snapshot(
                            match_keys=match_keys,
                            match_data=match_data,
                            fantasy_points=fantasy_points,
                            optim_fantasy_points_t20=optim_fantasy_points_t20,
                            optim_fantasy_points_odi=optim_fantasy_points_odi,
                            optim_fantasy_points_test=optim_fantasy_points_test,
                            num_matches=nm,
                            from_date='2024-01-01',
                            to_date='2024-07-06',
                            consistency_threshold=cons,
                            diversity_threshold= div,
                            quantile_form=quantile
                        )
                        
                        # Calculate metrics
                        metrics = calculate_metrics(snapshot_df)
                        
                        # Store results
                        results[exp_key] = {
                            'parameters': {
                                'num_matches': nm,
                                'consistency_threshold': float(cons),
                                'quantile_form': float(quantile),
                                'diversity_threshold': float(div)
                            },
                            'metrics': metrics,
                            # 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        }
                        
                        # Save after each iteration
                        with open(output_file, 'w') as f:
                            json.dump(results, f, indent=4)
                        
                        print(f"Saved results for {exp_key}")
                        print(f"Metrics: {metrics}")
                        
                    except Exception as e:
                        print(f"Error in experiment {exp_key}: {str(e)}")
    
    return results

def analyze_cv_results(results_file: str):
    """
    Analyze cross-validation results and return best parameters.
    
    Args:
        results_file: Path to JSON file containing CV results
        
    Returns:
        Tuple[pd.DataFrame, Dict]: Results DataFrame and best parameters dict
    """
    try:
        with open(results_file, 'r') as f:
            results = json.load(f)
    except FileNotFoundError:
        print(f"Results file not found: {results_file}")
        return pd.DataFrame(), {}
    except json.JSONDecodeError:
        print(f"Error reading results file: {results_file}")
        return pd.DataFrame(), {}
    
    # Convert to DataFrame for easier analysis
    df_data = []
    for exp_key, data in results.items():
        try:
            row = {
                **data['parameters'],
                **data['metrics']
            }
            df_data.append(row)
        except KeyError as e:
            print(f"Skipping malformed result {exp_key}: {e}")
    
    results_df = pd.DataFrame(df_data)
    
    if results_df.empty:
        print("No valid results found")
        return results_df, {}
    
    # Find best parameters for different metrics
    best_params = {
        'performance_ratio': results_df.loc[results_df['performance_ratio_mean'].idxmax()].to_dict(),
        'optimal_mae': results_df.loc[results_df['optimal_mae'].idxmin()].to_dict(),
        'expected_mae': results_df.loc[results_df['expected_mae'].idxmin()].to_dict()
    }
    
    return results_df, best_params

# Example usage:
if __name__ == "__main__":
    # Run CV
    all_paths = [f"../data/player_fantasy_points_{format_lower}.json" for format_lower in ["t20", "odi", "test"]]
    squads_path = f"../data/combined_squad.json"
    def load_sample_players(json_file):
        with open(json_file, "r") as file:
            return json.load(file)

    match_data = load_sample_players(squads_path)
    match_keys = list(match_data.keys())
    print(len(match_keys))
    # print (match_keys)


    results = run_optimization_cv(
        match_keys=match_keys,
        match_data=match_data,
        fantasy_points=None,
        optim_fantasy_points_t20=load_player_fantasy_points_for_optimization(all_paths[0]),
        optim_fantasy_points_odi=load_player_fantasy_points_for_optimization(all_paths[1]),
        optim_fantasy_points_test=load_player_fantasy_points_for_optimization(all_paths[2]),
    )
    print(results)
    # Analyze results
    results_df, best_params = analyze_cv_results('optimization_cv_results.json')
    
    print("\nBest parameters by metric:")
    for metric, params in best_params.items():
        print(f"\n{metric}:")
        for key, value in params.items():
            print(f"{key}: {value:.4f}")
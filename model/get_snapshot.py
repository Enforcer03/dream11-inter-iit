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
from heuristic_solver import compute_player_stats, compute_covariance_matrix, optimize_team_advanced, optimize_team_advanced_test
import pandas as pd
from tqdm import tqdm

def extract_date_from_match_key(match_key):
  date_pattern = r'(\d{4}-\d{2}-\d{2})'
  match = re.search(date_pattern, match_key)
  if match:
      return match.group(1)
  else:
      return None



def get_team_selection_snapshot(match_keys, match_data, fantasy_points, 
                           optim_fantasy_points_t20, optim_fantasy_points_odi, 
                           optim_fantasy_points_test, input_date=None, num_matches =50, quantile_form=75, consistency_threshold =0.5, form_threshold =0.333, diversity_threshold=0.5):
    """
    Generate a CSV snapshot of team selections after a specified date
    
    Parameters:
    match_keys (list): List of match identifiers
    match_data (dict): Dictionary containing match data
    fantasy_points (dict): Dictionary containing fantasy points data
    optim_fantasy_points_t20 (dict): Dictionary containing optimized fantasy points for T20
    optim_fantasy_points_odi (dict): Dictionary containing optimized fantasy points for ODI
    optim_fantasy_points_test (dict): Dictionary containing optimized fantasy points for Test
    input_date (datetime.date, optional): Date to filter matches
    
    Returns:
    pd.DataFrame: DataFrame containing team selections and scores
    """
    snapshot_data = []
    
    for match_key in tqdm(match_keys):
        # Extract date string from match key
        match_date_str = extract_date_from_match_key(match_key)
        if not match_date_str:
            continue
            
        try:
            match_date = datetime.datetime.strptime(match_date_str, '%Y-%m-%d').date()
        except ValueError:
            continue
            
        if input_date and match_date < input_date:
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
        
        # Get player stats and optimize team
        stats_df = compute_player_stats(
            optim_fantasy_points,
            list(all_players),
            num_matches=num_matches,
            date_of_match=match_date_str
        )
        
        if not stats_df.empty:
            # Compute covariance matrix
            cov_matrix = compute_covariance_matrix(
                optim_fantasy_points,
                stats_df['player'].tolist(),
                num_matches=num_matches,
                date_of_match=match_date_str
            )
            
            # Add team information
            stats_df['team'] = stats_df['player'].map(player_team_mapping)
            
            # Optimize team using advanced optimizer
            selected_players, weights_df = optimize_team_advanced_test(
                stats_df, 
                cov_matrix,
                boolean=True,
                quantile_form=quantile_form,
                consistency_threshold=consistency_threshold,
                form_threshold=form_threshold,
                diversity_threshold= diversity_threshold

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
                    'performance_ratio': actual_points / optimal_score if optimal_score > 0 else 0
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
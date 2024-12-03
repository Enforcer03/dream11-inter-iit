from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import pandas as pd
from pipeline import calculate_optimal_team, evaluate_team
from utils import load_player_fantasy_points, calculate_team_metrics

# # Path to the JSON file
T20_fantasy_points = "../data/processed/player_fantasy_points_t20.json"
ODI_fantasy_points = "../data/processed/player_fantasy_points_odi.json"
Test_fantasy_points = "../data/processed/player_fantasy_points_test.json"


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
 

@app.route('/generate_best_team', methods=['POST'])
def generate_best_team():
    # Get the player name from the query string
    data = request.get_json()
    if 'player_info' not in data:
        return jsonify({'error': 'Squad Not Found'}), 400
    if 'date' not in data:
        return jsonify({'error': 'Please Enter the Date in YYYY-MM-DD Format'}), 400
    if 'format' not in data:
        return jsonify({'error': 'Please Enter the correct format: ODI/Test/T20'}), 400
    player_info = data['player_info']
    date = data['date']
    format = data['format']
    

    if player_info and date and format:
        fantasy_points_data = None
        if format=="T20":
            fantasy_points_data = load_player_fantasy_points(T20_fantasy_points)
        elif format=="ODI":
            fantasy_points_data = load_player_fantasy_points(ODI_fantasy_points)
        elif format=="Test":
            fantasy_points_data = load_player_fantasy_points(Test_fantasy_points)
            
            
        selected_players, stats_df, cov_matrix = calculate_optimal_team(
        player_info=player_info,
        num_matches=50,
        date_of_match= date,
        risk_aversion=0.1,
        solver='pulp',
        fantasy_points_data=fantasy_points_data
        )
        # Check if the player exists in the data
        player_stats_json = stats_df.to_json(orient='records')
        cov_matrix_json = cov_matrix.to_json(orient='records')
        
        if selected_players:
            return jsonify({"best_team": selected_players,
                            "player_stats": player_stats_json,
                            "cov_matrix": cov_matrix_json
                            })
        else:
            return jsonify({"error": "Team is Not Selected Correctly"}), 404
            
    else:
        return jsonify({"error": "Error in Player Info/Date/Foramt"}), 400
    
    
@app.route('/team_evaluation', methods=['POST'])
def team_evaluation():
    # Get the player name from the query string
    data = request.get_json()
    if 'best_team' not in data:
        return jsonify({'error': 'Best Team not loaded correctly'}), 400
    if 'player_stats' not in data:
        return jsonify({'error': 'Player Stats not loaded correctly'}), 400
    if 'cov_matrix' not in data:
        return jsonify({'error': 'Player Covariance Matrix not loaded correctly'}), 400
    selected_players = data['best_team']
    stats_df_json = data['player_stats']
    cov_matrix_json = data['cov_matrix']
    stats_df = pd.DataFrame(json.loads(stats_df_json))
    cov_matrix = pd.DataFrame(json.loads(cov_matrix_json))
    
    if selected_players and stats_df_json and cov_matrix_json:
        evaluation_tuple = evaluate_team(selected_players,stats_df,cov_matrix)
        if evaluation_tuple:
            return jsonify({"team_consistency_score": evaluation_tuple[0],
                            "team_diversity_score": evaluation_tuple[1],
                            "form_score": evaluation_tuple[2]
                            })
        else:
            return jsonify({"error": "Team Evalaution is not done correctly"}), 404
            
    else:
        return jsonify({"error": "Players are not selected correctly or Player Stats are corrupted or Covariance Matrix is Corrupted"}), 400
    
    
    

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=8080, debug=True)

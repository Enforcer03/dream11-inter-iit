from flask import Flask, jsonify, request
import json
from pipeline import calculate_optimal_team, evaluate_team
from utils import load_player_fantasy_points, calculate_team_metrics

# # Path to the JSON file
T20_fantasy_points = "player_fantasy_points_t20.json"
ODI_fantasy_points = "player_fantasy_points_odi.json"
Test_fantasy_points = "player_fantasy_points_test.json"


app = Flask(__name__)
 

@app.route('/generate_best_team', methods=['POST'])
def generate_best_team():
    best_team = []
    # Get the player name from the query string
    data = request.get_json()
    if 'Player_info' not in data:
        return jsonify({'error': 'Squad Not Found'}), 400
    if 'Date' not in data:
        return jsonify({'error': 'Please Enter the Date in YYYY-MM-DD Format'}), 400
    if 'Format' not in data:
        return jsonify({'error': 'Please Enter the correct format: ODI/Test/T20'}), 400
    player_info = data['Player_info']
    date = data['date']
    format = data['Format']
    

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
        risk_tolerance=1.0,
        solver='pulp',
        fantasy_points_data=fantasy_points_data
        )
        # Check if the player exists in the data
        
        if selected_players:
            return jsonify(f"Best Team: {selected_players}")
        else:
            return jsonify({"error": "Team is Not Selected Correctly"}), 404
            
    else:
        return jsonify({"error": "Error in Player Info/Date/Foramt"}), 400

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=8080, debug=True)

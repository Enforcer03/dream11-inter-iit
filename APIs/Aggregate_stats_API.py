from flask import Flask, jsonify, request
import json
import requests


# Path to the JSON file
T20_aggregate_points = "/Users/ayush_arya/Downloads/Inter_IIT_Tech_13/dream11-inter-iit/data/Aggregate_till_training_date_data/T20_aggregate_data.json"
ODI_ODM_aggregate_points = "/Users/ayush_arya/Downloads/Inter_IIT_Tech_13/dream11-inter-iit/data/Aggregate_till_training_date_data/ODI_ODM_aggregate_data.json"
Test_MDM_aggregate_points = "/Users/ayush_arya/Downloads/Inter_IIT_Tech_13/dream11-inter-iit/data/Aggregate_till_training_date_data/Test_MDM_aggregate_data.json"


app = Flask(__name__)

# Load the data from your JSON file
with open(T20_aggregate_points, "r") as file:
    player_T20_data = json.load(file)

with open(ODI_ODM_aggregate_points, "r") as file:
    player_ODI_data = json.load(file)

with open(T20_aggregate_points, "r") as file:
    player_Test_data = json.load(file)


@app.route("/aggregate_stats", methods=["POST"])
def get_player_stats():
    stats = {}
    stats["ODI"] = "Not available"
    stats["Test"] = "Not available"
    stats["T20"] = "Not available"
    # Get the player name from the query string
    data = request.get_json()
    if "Player" not in data:
        return jsonify({"error": "Missing query parameter"}), 400
    player_name = data["Player"]

    if player_name:
        # Check if the player exists in the data
        player_T20_stats = player_T20_data.get(player_name)
        player_ODI_stats = player_ODI_data.get(player_name)
        player_Test_stats = player_Test_data.get(player_name)
        stats["ODI"] = player_ODI_stats
        stats["T20"] = player_T20_stats
        stats["Test"] = player_Test_stats
        if stats["ODI"] or stats["Test"] or stats["T20"]:
            return jsonify(stats)
        else:
            return jsonify({"error": "Player not found"}), 404

    else:
        return jsonify({"error": "Player name is required"}), 400
    
@app.route('/analyze_player', methods=['POST'])
def analyze_player():
    # Get the player name from the query string
    data = request.get_json()
    if 'best_team' not in data:
        return jsonify({'error': 'Best Team not found'}), 400
    if 'Player' not in data:
        return jsonify({'error': 'Player name not found'}), 400
    if 'format' not in data:
        return jsonify({'error': 'Please enter format as ODI/Test/T20'}), 400
    
    
    selected_players = data['best_team']
    player_name = data['Player']
    format = data['format'].lower()
    player_aggregate_stats = None
    if format == "t20":
        player_aggregate_stats = player_T20_data.get(player_name, {})
    elif format == "odi":
        player_aggregate_stats = player_ODI_data.get(player_name, {})
    elif format == "test":
        player_aggregate_stats = player_Test_data.get(player_name, {})
    
    
    if not player_aggregate_stats:
        return jsonify({'error': f'No aggregate statistics found for {player_name}'}), 400 
    
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
        return jsonify({"analysis": analysis})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Error Querying LLM"}), 404
    


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000,debug=True)

from flask import Flask, jsonify, request
import json


# Path to the JSON file
T20_aggregate_points = "/Users/ayush_arya/Downloads/Inter_IIT_Tech_13/dream11-inter-iit/data/Aggregate_till_training_date_data/T20_aggregate_data.json"
ODI_ODM_aggregate_points= "/Users/ayush_arya/Downloads/Inter_IIT_Tech_13/dream11-inter-iit/data/Aggregate_till_training_date_data/ODI_ODM_aggregate_data.json"
Test_MDM_aggregate_points= "/Users/ayush_arya/Downloads/Inter_IIT_Tech_13/dream11-inter-iit/data/Aggregate_till_training_date_data/Test_MDM_aggregate_data.json"


app = Flask(__name__)

# Load the data from your JSON file
with open(T20_aggregate_points, 'r') as file:
    player_T20_data = json.load(file)
    
with open(ODI_ODM_aggregate_points, 'r') as file:
    player_ODI_data = json.load(file)

with open(T20_aggregate_points, 'r') as file:
    player_Test_data = json.load(file)
    

@app.route('/aggregate_stats', methods=['POST'])
def get_player_stats():
    stats = {}
    stats["ODI"] = "Not available"
    stats["Test"] = "Not available"
    stats["T20"] = "Not available"
    # Get the player name from the query string
    data = request.get_json()
    if 'Player' not in data:
        return jsonify({'error': 'Missing query parameter'}), 400
    player_name = data['Player']

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

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=8080, debug=True)

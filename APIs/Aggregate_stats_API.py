from flask import Flask, jsonify, request
from flask_cors import CORS
import json


# Path to the JSON file
T20_aggregate_points = "../../T20_aggregate_data.json"
ODI_ODM_aggregate_points = "../../ODI_ODM_aggregate_data.json"
Test_MDM_aggregate_points = "../../Test_MDM_aggregate_data.json"


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# Load the data from your JSON file
with open(T20_aggregate_points, "r") as file:
    player_T20_data = json.load(file)

with open(ODI_ODM_aggregate_points, "r") as file:
    player_ODI_data = json.load(file)

with open(T20_aggregate_points, "r") as file:
    player_Test_data = json.load(file)


@app.route("/aggregate_stats", methods=["POST"])
def get_player_stats():
    data = request.get_json()
    player_names = data["Players"]

    stats = {}
    for player_name in player_names:
        stats[player_name] = {}
        stats[player_name]["ODI"] = "Not available"
        stats[player_name]["Test"] = "Not available"
        stats[player_name]["T20"] = "Not available"
        # Get the player name from the query string
        if player_name:
            # Check if the player exists in the data
            player_T20_stats = player_T20_data.get(player_name)
            player_ODI_stats = player_ODI_data.get(player_name)
            player_Test_stats = player_Test_data.get(player_name)
            stats[player_name]["ODI"] = player_ODI_stats
            stats[player_name]["T20"] = player_T20_stats
            stats[player_name]["Test"] = player_Test_stats
    if stats:
        return jsonify(stats)
    else:
        return jsonify({"error": "Player name is required"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)

from flask import Flask, jsonify, request
import json
from flask_cors import CORS
import re

# Path to the JSON file
squads = "../data/processed/datewise_squad.json"

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})


with open(squads, "r") as file:
    squads_data = json.load(file)


@app.route("/squads", methods=["POST"])
def squads():
    # Get the player name from the query string
    data = request.get_json()
    if "Date" not in data:
        return jsonify({"error": "Missing query parameter"}), 400
    date = data["Date"]

    # Check if the date is in the correct format
    date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    if not date_pattern.match(date):
        return jsonify({"error": "Date format should be YYYY-MM-DD"}), 400

    if date in squads_data:
        # Check if the player exists in the data
        leagues = squads_data.get(date)
        if leagues:
            return jsonify(leagues)
        else:
            return jsonify({"error": "No Leagues Available"}), 404

    else:
        return jsonify({"error": "No match found"}), 400


if __name__ == "__main__":
    app.run(debug=True)

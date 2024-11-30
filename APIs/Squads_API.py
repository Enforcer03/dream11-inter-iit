from flask import Flask, jsonify, request
import json


# Path to the JSON file
squads = "/Users/ayush_arya/Downloads/Inter_IIT_Tech_13/dream11-inter-iit/data/Match_Level_players/Final_datewise_squad.json"

app = Flask(__name__)

with open(squads, 'r') as file:
    squads_data = json.load(file)
    

@app.route('/squads', methods=['POST'])
def squads():
    # Get the player name from the query string
    data = request.get_json()
    if 'Date' not in data:
        return jsonify({'error': 'Missing query parameter'}), 400
    date = data['Date']

    if date in squads_data:
        # Check if the player exists in the data
        leagues = squads_data.get(date)
        if leagues:
            return jsonify(leagues)
        else:
            return jsonify({"error": "No Leagues Available"}), 404
            
    else:
        return jsonify({"error": "Fill Date in YYYY-MM-DD format"}), 400

if __name__ == '__main__':
    app.run(debug=True)

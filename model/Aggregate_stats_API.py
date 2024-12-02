from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import requests
import pandas as pd


# Path to the JSON file
T20_aggregate_points = "../data/processed/T20_aggregate_data.json"
ODI_ODM_aggregate_points = "../data/processed/ODI_ODM_aggregate_data.json"
Test_MDM_aggregate_points = "../data/processed/Test_MDM_aggregate_data.json"


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
    format = data["Format"]

    stats = {}
    for player_name in player_names:
        stats[player_name] = {}
        stats[player_name][format] = "Not available"
        # Get the player name from the query string
        if player_name:
            # Check if the player exists in the data
            player_stats = []
            if format == "ODI":
                player_stats = player_ODI_data.get(player_name)
            elif format == "T20":
                player_stats = player_T20_data.get(player_name)
            elif format == "Test":
                player_stats = player_Test_data.get(player_name)

            stats[player_name] = player_stats
    if stats:

        for player, player_stats in stats.items():
            if player_stats:
                for key, value in player_stats.items():
                    if value == float("inf"):
                        player_stats[key] = "Infinity"

        print(stats)
        return jsonify(stats)
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
    
@app.route('/analyze_team', methods=['POST'])
def analyze_team():
    # Get the player name from the query string
    data = request.get_json()
    if 'best_team' not in data:
        return jsonify({'error': 'Best Team not found'}), 400
    if 'player_stats' not in data:
        return jsonify({'error': 'Player Stats not loaded correctly'}), 400
    if 'format' not in data:
        return jsonify({'error': 'Please enter format as ODI/Test/T20'}), 400
    
    
    selected_players = data['best_team']
    stats_df_json = data['player_stats']
    stats_df = pd.DataFrame(json.loads(stats_df_json))
    format = data['format'].lower()
    aggregate_stats = None
    if format == "t20":
        aggregate_stats = player_T20_data
    elif format == "odi":
        player_aggregate_stats = player_ODI_data
    elif format == "test":
        aggregate_stats = player_Test_data
    
    team_stats = []
    for player in selected_players:
        player_fantasy_stats = stats_df[stats_df['player'] == player].to_dict('records')[0]
        player_aggregate_stats = aggregate_stats.get(player, {})
        
        # Create player stat summary
        player_summary = {
            'name': player,
            'batting_style': player_aggregate_stats.get('Batting', 'N/A'),
            'bowling_style': player_aggregate_stats.get('Bowling', 'N/A'),
            'mean_fantasy_points': player_fantasy_stats.get('mean_points', 'N/A'),
            'batting_stats': {
                'average': player_aggregate_stats.get('Batting Avg', 'N/A'),
                'strike_rate': player_aggregate_stats.get('Batting S/R', 'N/A'),
                'consistency': player_aggregate_stats.get('Scoring Consistency', 'N/A'),
                'runs': player_aggregate_stats.get('Runs', 'N/A')
            },
            'bowling_stats': {
                'wickets': player_aggregate_stats.get('Wickets', 'N/A'),
                'economy': player_aggregate_stats.get('Economy Rate', 'N/A'),
                'average': player_aggregate_stats.get('Bowling Avg', 'N/A'),
                'strike_rate': player_aggregate_stats.get('Bowling S/R', 'N/A')
            },
            'fielding_stats': {
                'catches': player_aggregate_stats.get('Catches', 'N/A'),
                'runouts': player_aggregate_stats.get('Runouts', 'N/A'),
                'stumpings': player_aggregate_stats.get('Stumpings', 'N/A')
            },
            'overall_stats': {
                'games': player_aggregate_stats.get('Games', 'N/A'),
                'win_percentage': player_aggregate_stats.get('Win %', 'N/A')
            }
        }
        team_stats.append(player_summary)
    
    # Calculate team aggregate statistics
    team_summary = {
        'total_mean_points': sum(p.get('mean_fantasy_points', 0) for p in team_stats),
        'batting_styles': [p['batting_style'] for p in team_stats],
        'bowling_styles': [p['bowling_style'] for p in team_stats if p['bowling_style'] != 'N/A'],
        'avg_win_percentage': sum(float(p['overall_stats']['win_percentage']) for p in team_stats if p['overall_stats']['win_percentage'] != 'N/A') / len(team_stats),
        'total_experience': sum(int(p['overall_stats']['games']) for p in team_stats if p['overall_stats']['games'] != 'N/A')
    }
    
    # Create prompt for LLM
    prompt = f"""
        As a cricket analytics expert, provide a detailed analysis of why this team selection represents the optimal combination of players. Here's the team composition and their statistics:

        Team Overview:
        - Total Mean Fantasy Points: {team_summary['total_mean_points']:.2f}
        - Average Win Percentage: {team_summary['avg_win_percentage']:.2f}%
        - Total Combined Experience: {team_summary['total_experience']} matches
        - Batting Styles Distribution: {', '.join(str(team_summary['batting_styles']))}
        - Bowling Styles Distribution: {', '.join(str(team_summary['bowling_styles']))}

        Detailed Player Analysis:

        """

    # Add individual player details to prompt
    for player in team_stats:
        prompt += f"""
            {player['name']}:
            - Fantasy Points: {player['mean_fantasy_points']}
            - Role: {player['bowling_style']} bowler, {player['batting_style']} batsman
            - Batting: Avg {player['batting_stats']['average']}, SR {player['batting_stats']['strike_rate']}, Consistency {player['batting_stats']['consistency']}
            - Bowling: {player['bowling_stats']['wickets']} wickets, Econ {player['bowling_stats']['economy']}, Avg {player['bowling_stats']['average']}
            - Fielding: {player['fielding_stats']['catches']} catches, {player['fielding_stats']['runouts']} runouts
            - Experience: {player['overall_stats']['games']} games, {player['overall_stats']['win_percentage']}% wins
            """

    prompt += """
        Please provide a comprehensive analysis of this team selection, addressing:
        1. Overall team balance and composition
        2. Batting lineup strength and depth
        3. Bowling attack variety and effectiveness
        4. Fielding capabilities
        5. Experience and win-rate contribution
        6. Key player roles and their specific importance
        7. How the players complement each other
        8. Any potential weaknesses or risks
        9. Why this combination maximizes fantasy points while maintaining team balance

        Focus on why this specific combination of players forms the optimal team, considering both individual strengths and team synergy."""

    url = "https://8001-01jdya9bpnhj5dqyfzh17zdghv.cloudspaces.litng.ai/predict"
    headers = {"Content-Type": "application/json"}
    data = {"input": prompt}

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        analysis = response.json()['output']
        return jsonify({"team analysis": analysis})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Error Querying LLM"}), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000,debug=True)

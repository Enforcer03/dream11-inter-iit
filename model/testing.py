import json
import math
import numpy as np
from calculator import calculate_fantasy_points_t20
file_path = '/Users/ved14/Library/CloudStorage/GoogleDrive-v_umrajkar@ma.iitr.ac.in/My Drive/SEM7/extras/dream11-inter-iit/player_match_data.json'

with open(file_path, 'r') as file:
    player_data = json.load(file)
# Calculate and store fantasy points for each player and each match
fantasy_points = {}

for player, matches in player_data.items():
    fantasy_points[player] = {}
    for match_id, stats in matches.items():
        # Calculate points for each match
        split = calculate_fantasy_points_t20(stats)
        fantasy_points[player][match_id]=split

# print(fantasy_points)


# Optionally, write results to a new JSON file
output_path = '/Users/ved14/Library/CloudStorage/GoogleDrive-v_umrajkar@ma.iitr.ac.in/My Drive/SEM7/extras/dream11-inter-iit/player_fantasy_points.json'
with open(output_path, 'w') as outfile:
    json.dump(fantasy_points, outfile, indent=4)

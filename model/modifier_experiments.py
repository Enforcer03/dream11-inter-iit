"""
What we want to do or prove?
- We want to prove that applying certain modifiers to the mean estimate can help in improving the performance.
- Lets first get values for just the mean estimate performance
"""

import json
from datetime import datetime

# paths are relative to the root directory
points_json = "./data/player_fantasy_points_t20.json"
matches_json = "./data/player_match_data_2010_onwards.json"

# read the matches json and create a dictionary with the following structure
# {player_name -> {match_name -> opposition, venue}}
match_data = {}
with open(matches_json, "r") as file:
    player_matches = json.load(file)
    for player, matches in player_matches.items():
        match_data[player] = {}
        for match, features in matches.items():
            match_data[player][match] = {"opposition": features.get("Opposition Team", "Not Available"), "venue": features.get("Venue", "Not Available")}

# read the points json and create a dictionary with the following structure
# {player_name -> [(match_name, batting_points, bowling_points, fielding_points, total_points), sorted based on date]}
player_data = {}
with open(points_json, "r") as file:
    points_data = json.load(file)
    for player, matches in points_data.items():
        player_data[player] = []
        for match, points in matches.items():
            total_points = points.get("total_points", 0)
            batting_points = points.get("batting_points", 0)
            bowling_points = points.get("bowling_points", 0)
            fielding_points = points.get("fielding_points", 0)
            player_data[player].append({"match_name": match, "bat": batting_points, "bowl": bowling_points, "field": fielding_points, "total": total_points})
            if(match_data[player][match]["opposition"]):
                player_data[player][-1]["opposition"] = match_data[player][match]["opposition"]
            if(match_data[player][match]["venue"]):
                player_data[player][-1]["venue"] = match_data[player][match]["venue"]
        player_data[player] = sorted(player_data[player], key=lambda x: datetime.strptime("-".join(x["match_name"].split("-")[-5:-2]), "%Y-%m-%d"))

total_count = 0
total_delta = 0
batting_delta = 0
bowling_delta = 0
fielding_delta = 0
no_past_matches = 100
o_mod = 0
v_mod = 0
l_mod = 0

for player, matches in player_data.items():
    for i in range(1, len(matches)):
        divider = 0
        total_sum = 0
        batting_sum = 0
        bowling_sum = 0
        fielding_sum = 0
        past_matches = []
        if(0 < i < no_past_matches):
            past_matches = matches[:i]
        else:
            past_matches = matches[i-no_past_matches:i]
        for j, match in enumerate(past_matches):
            opp_same = o_mod*(match["opposition"] == matches[i]["opposition"])
            venue_same = v_mod*(match["venue"] == matches[i]["venue"])
            latest_modifier = l_mod*(j/no_past_matches)
            modifier = 1 + opp_same + venue_same + latest_modifier
            divider += modifier
            total_sum += match["total"]*(modifier)
            batting_sum += match["bat"]*(modifier)
            bowling_sum += match["bowl"]*(modifier)
            fielding_sum += match["field"]*(modifier)
        if(divider == 0):
            continue
        mean_total = total_sum/divider
        mean_batting = batting_sum/divider
        mean_bowling = bowling_sum/divider
        mean_fielding = fielding_sum/divider
        
        total_count += 1
        total_delta += abs(matches[i]["total"] - mean_total)
        batting_delta += abs(matches[i]["bat"] - mean_batting)
        bowling_delta += abs(matches[i]["bowl"] - mean_bowling)
        fielding_delta += abs(matches[i]["field"] - mean_fielding)

print("Average Total Points Delta: ", total_delta/total_count)
print("Average Batting Points Delta: ", batting_delta/total_count)
print("Average Bowling Points Delta: ", bowling_delta/total_count)
print("Average Fielding Points Delta: ", fielding_delta/total_count)

"""
Normal 10 Matches Average
-------------------------
Average Total Points Delta:  25.311382480486092
Average Batting Points Delta:  14.85002592483413
Average Bowling Points Delta:  13.978763316152227
Average Fielding Points Delta:  3.745466978633275

Modified 10 Matches Average
---------------------------
Average Total Points Delta:  25.338839395300553
Average Batting Points Delta:  14.86307288727171
Average Bowling Points Delta:  13.963618513881936
Average Fielding Points Delta:  3.7458436274724085

Highly Modified 10 Matches Average
----------------------------------
Average Total Points Delta:  25.661093446787234
Average Batting Points Delta:  15.02436988210924
Average Bowling Points Delta:  14.093208593904745
Average Fielding Points Delta:  3.7581101525511107

Normal 100 Matches Average
--------------------------
Average Total Points Delta:  24.80175104731126
Average Batting Points Delta:  14.522943248181894
Average Bowling Points Delta:  13.934247810427538
Average Fielding Points Delta:  3.7375506610524316

Highly Modified 100 Matches Average
-----------------------------------
Average Total Points Delta:  25.10946602933476
Average Batting Points Delta:  14.690278705435924
Average Bowling Points Delta:  14.005922568312727
Average Fielding Points Delta:  3.747925529279975

Conclusion
----------
These modifiers do not seem to benefit the average predictions, 
meaning the intuition behind them does not stand validated.

Also proving that having more data is not necessarily helping the estimates.
"""
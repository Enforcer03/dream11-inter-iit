# import json

# Function to calculate batting points
def calculate_batting_points(player_stats):
    points = 0
    runs_scored = player_stats.get("Total Runs Scored", 0)
    boundaries = player_stats.get("Fours", 0)
    sixes = player_stats.get("Sixes", 0)
    balls_faced = player_stats.get("Balls Faced", 0)
    inning1_not_out = player_stats.get("How Out Inning 1 (not out)", 0)
    inning2_not_out = player_stats.get("How Out Inning 2 (not out)", 0)
    inning1_not_played = player_stats.get("How Out Inning 1 (Not Played)", 0)
    inning2_not_played = player_stats.get("How Out Inning 2 (Not Played)", 0)
    
    
    # +1 point per run
    points += runs_scored * 1

    # +1 per boundary, +2 per six
    points += boundaries * 1
    points += sixes * 2

    # +4  half-century, +8 for a century
    if runs_scored >= 100:
        points += 8
    elif runs_scored >= 50:
        points += 4


    # TODO: MAKE THIS NOT FOR BOWLERS
    # -2 points if dismissed for a duck (only if not a bowler)
    if runs_scored == 0 and ((inning1_not_played==0 and inning1_not_out==0) or (inning2_not_played==0 and inning2_not_out==0)) and balls_faced > 0:
        points -= 3

    # TODO: MAKE THIS NOT FOR BOWLERS
    # Strike Rate Bonus (Min 20 balls faced)
    if balls_faced >= 20:
        strike_rate = player_stats.get("Avg Batting S/R Per Inning")
        if strike_rate > 140:
            points += 6
        elif 120 < strike_rate <= 140:
            points += 4
        elif 100 <= strike_rate <= 120:
            points += 2
        elif 40 <= strike_rate < 50:
            points -= 2
        elif 30 <= strike_rate < 40:
            points -= 4
        elif strike_rate < 30:
            points -= 6

    return points

# Function to calculate bowling points
def calculate_bowling_points(player_stats):
    points = 0
    wickets = player_stats.get("Wickets", 0)
    overs_bowled = player_stats.get("Overs Bowled", 0)
    economy_rate = player_stats.get("Avg Economy Rate per inning", 0)
    
    # Bowled and LBW features to be made yet
    bowled_or_lbw = player_stats.get("Bowled", 0) + player_stats.get("LBW", 0)

    # +25 points per wicket, +8 points for bowled/LBW dismissals
    points += wickets * 25
    points += bowled_or_lbw * 8

    # Bonus for 4 or >=5 wickets in a match
    if wickets >= 5:
        points += 8
    elif wickets == 4:
        points += 4

    # +4 for each maiden over
    maiden_overs = player_stats.get("Maiden Overs", 0)
    points += maiden_overs * 4

    # Economy Rate Bonus (Min 5 overs bowled)
    if overs_bowled >= 5:
        if economy_rate < 2.5:
            points += 6
        elif 2.5 <= economy_rate < 3.5:
            points += 4
        elif 3.5 <= economy_rate <= 4.5:
            points += 2
        elif 7 <= economy_rate <= 8:
            points -= 2
        elif 8 < economy_rate <= 9:
            points -= 4
        elif economy_rate > 9:
            points -= 6

    return points

# Function to calculate fielding points
def calculate_fielding_points(player_stats):
    points = 0
    catches_taken = player_stats.get("Catches Taken", 0)
    stumped_outs = player_stats.get("Stumped Outs Made", 0)
    # run_outs_direct = player_stats.get("Direct Hit Run Outs Made", 0)
    # run_outs_indirect = player_stats.get("Non-Direct Run Outs Made", 0)
    run_outs = player_stats.get("Run Outs Made", 0)


    # +8 points per catch, +12 for stumping, +12 for direct run-out, +6 for indirect
    points += catches_taken * 8
    points += stumped_outs * 12
    # points += run_outs_direct * 12
    # points += run_outs_indirect * 6
    ## considering probability of direct hit is less so -1 than the avg of +12 and +6
    points += run_outs * 8  

    # Bonus for 3 or more catches
    if catches_taken >= 3:
        points += 4

    return points

# Wrapper function to calculate total fantasy points
def calculate_fantasy_points_odi(player_stats):
    batting_points = calculate_batting_points(player_stats)
    bowling_points = calculate_bowling_points(player_stats)
    fielding_points = calculate_fielding_points(player_stats)
    
    # Total points
    total_points = batting_points + bowling_points + fielding_points
    # assuming every player is playing
    total_points += 4
    return {
        "total_points": total_points,
        "batting_points": batting_points,
        "bowling_points": bowling_points,
        "fielding_points": fielding_points
    }


if __name__== '__main__':
    # TODO: REPLACE WITH T20 EXAMPLE
    print(calculate_fantasy_points_odi({
            "Team Name": "Rajasthan Royals",
            "Batting Innings": 1,
            "Bowling Innings": 1,
            "Total Runs Scored": 60.0,
            "Avg Runs Per Inning": 60.0,
            "Boundaries": 10.0,
            "Sixes": 5.0,
            "Average Sixes Per Inning": 5.0,
            "Fours": 5.0,
            "Average Fours Per Inning": 5.0,
            "Boundary% Per Inning": 40.0,
            "Boundary Rate Per Inning": 2.5,
            "Wickets": 2.0,
            "Avg Wickets Per Inning": 2.0,
            "Opposition Team": "Chennai Super Kings",
            "Catches Taken": 1,
            "Stumped Outs Made": 0,
            "Run Outs Made": 0,
            "Match Date": "2010-04-03",
            "Match ID": "Chennai_Super_Kings-Rajasthan_Royals-2010-04-03-male-T20",
            "Match Type": "T20",
            "Venue": "MA Chidambaram Stadium, Chepauk",
            "Event": "Indian Premier League",
            "Match Winner": "Chennai Super Kings",
            "Balls Faced": 25.0,
            "Avg Balls Faced Per Inning": 25.0,
            "Avg Batting S/R Per Inning": 240.0,
            "Avg Runs/Ball Per Inning": 2.4,
            "*how Out": "Not Played",
            "Overs Bowled": 4.0,
            "Bowls Bowled": 24.0,
            "Average Bowls Bowled Per Inning": 24.0,
            "Avg Economy Rate per inning": 11.75,
            "Bowling Average": 23.5,
            "Average Consecutive Dot Balls": 2.0,
            "Maiden Overs": 0.0,
            "Avg Bowling S/R Per Inning": 12.0,
            "Runs Given": 47.0,
            "RunsGiven/Ball Per Inning": 1.9583333333333333,
            "Batting S/R AA(Above Average)": 134.52502446199924,
            "How Out Inning 1 (Not Played)": 0,
            "How Out Inning 1 (caught)": 1,
            "How Out Inning 1 (not out)": 0,
            "How Out Inning 1 (lbw)": 0,
            "How Out Inning 1 (bowled)": 0,
            "How Out Inning 1 (Run Out)": 0,
            "How Out Inning 1 (caught and bowled)": 0,
            "How Out Inning 1 (stumped)": 0,
            "How Out Inning 2 (Not Played)": 0,
            "How Out Inning 2 (caught)": 0,
            "How Out Inning 2 (not out)": 0,
            "How Out Inning 2 (lbw)": 0,
            "How Out Inning 2 (bowled)": 1,
            "How Out Inning 2 (Run Out)": 0,
            "How Out Inning 2 (caught and bowled)": 0,
            "How Out Inning 2 (stumped)": 0
        }))

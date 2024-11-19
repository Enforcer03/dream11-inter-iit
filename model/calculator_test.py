import json

# Function to calculate batting points for Test matches
def calculate_batting_points_test(player_stats):
    points = 0
    runs_scored = player_stats.get("Total Runs Scored", 0)
    boundaries = player_stats.get("Fours", 0)
    sixes = player_stats.get("Sixes", 0)
    balls_faced = player_stats.get("Balls Faced", 0)
    try:
        how_out = player_stats.get("how Out", "").lower()
    except AttributeError:
        print("how out issue ")
        how_out = "nan"
    
    # +1 point per run
    points += runs_scored * 1

    # +1 per boundary, +2 per six
    points += boundaries * 1
    points += sixes * 2

    # Bonus for milestones: +16 for a double century, +8 for a century, +4 for a half-century
    if runs_scored >= 200:
        points += 16
    elif runs_scored >= 100:
        points += 8
    elif runs_scored >= 50:
        points += 4

    # Penalty: -4 points if dismissed for a duck (except tailenders)
    if runs_scored == 0 and how_out != "not out" and balls_faced > 0:
        points -= 4

    # # Strike Rate Bonus (Min 50 balls faced)
    # if balls_faced >= 50:
    #     strike_rate = (runs_scored / balls_faced) * 100
    #     if strike_rate >= 100:
    #         points += 4
    #     elif strike_rate < 40:
    #         points -= 2

    return points

# Function to calculate bowling points for Test matches
def calculate_bowling_points_test(player_stats):
    points = 0
    wickets = player_stats.get("Wickets", 0)
    overs_bowled = player_stats.get("Overs Bowled", 0)
    bowled_or_lbw = player_stats.get("Bowled", 0) + player_stats.get("LBW", 0)

    # +16 points per wicket, +8 for bowled/LBW dismissals
    points += wickets * 16
    points += bowled_or_lbw * 8

    # Bonus for 5, 6, or 10 wickets in a match
    if wickets >= 10:
        points += 16  # Match bonus for 10 wickets
    elif wickets >= 6:
        points += 8
    elif wickets >= 5:
        points += 4

    # # Economy Rate Bonus (Min 10 overs bowled in an innings)
    # if overs_bowled >= 10:
    #     economy_rate = player_stats.get("Economy Rate", 0)
    #     if economy_rate < 2.5:
    #         points += 6
    #     elif 2.5 <= economy_rate <= 3.5:
    #         points += 4
    #     elif 3.5 < economy_rate <= 4.5:
    #         points += 2
    #     elif 4.5 < economy_rate <= 5.5:
    #         points -= 2
    #     elif economy_rate > 5.5:
            # points -= 4

    return points

# Function to calculate fielding points for Test matches
def calculate_fielding_points_test(player_stats):
    points = 0
    catches_taken = player_stats.get("Catches Taken", 0)
    stumped_outs = player_stats.get("Stumped Outs Made", 0)
    run_outs_direct = player_stats.get("Direct Hit Run Outs Made", 0)
    run_outs_indirect = player_stats.get("Non-Direct Run Outs Made", 0)

    # +8 points per catch, +12 for stumping, +12 for direct run-out, +6 for indirect
    points += catches_taken * 8
    points += stumped_outs * 12
    points += run_outs_direct * 12
    points += run_outs_indirect * 6

    # Bonus for 5 or more catches in a match
    if catches_taken >= 5:
        points += 8

    return points

# Wrapper function to calculate total fantasy points for Test matches
def calculate_fantasy_points_test(player_stats):
    batting_points = calculate_batting_points_test(player_stats)
    bowling_points = calculate_bowling_points_test(player_stats)
    fielding_points = calculate_fielding_points_test(player_stats)
    
    # Total points
    total_points = batting_points + bowling_points + fielding_points
    return {
        "total_points": total_points,
        "batting_points": batting_points,
        "bowling_points": bowling_points,
        "fielding_points": fielding_points
    }

if __name__== '__main__':
    print(calculate_fantasy_points_test({
                "Team Name": "India",
                "Batting Innings": 2,
                "Bowling Innings": 0,
                "Total Runs Scored": 45.0,
                "Avg Runs Per Inning": 22.5,
                "Boundaries": 6.0,
                "Sixes": 1.0,
                "Average Sixes Per Inning": 0.5,
                "Fours": 5.0,
                "Average Fours Per Inning": 2.5,
                "Boundary% Per Inning": 6.521739130434782,
                "Boundary Rate Per Inning": 3.8333333333333335,
                "Wickets": 0,
                "Avg Wickets Per Inning": 0,
                "Opposition Team": "Bangladesh",
                "Catches Taken": 1,
                "Stumped Outs Made": 0,
                "Run Outs Made": 0,
                "Match Date": "2024-09-27",
                "Match ID": "Bangladesh-India-2024-09-27-male-Test",
                "Match Type": "Test",
                "Venue": "Green Park, Kanpur",
                "Event": "Bangladesh tour of India",
                "Match Winner": "India",
                "Balls Faced": 46.0,
                "Avg Balls Faced Per Inning": 23.0,
                "Avg Batting S/R Per Inning": 48.91304347826087,
                "Avg Runs/Ball Per Inning": 0.4891304347826087,
                "*how Out": "caught",
                "Overs Bowled": 0,
                "Bowls Bowled": 0,
                "Average Bowls Bowled Per Inning": 0,
                "Avg Economy Rate per inning": 0,
                "Bowling Average": 0,
                "*Average Consecutive Dot Balls": 0,
                "Bowling S/R": 0,
                "Runs Given": 0,
                "RunsGiven/Ball Per Inning": 0,
                "*Batting S/R AA(Above Average)": 57.07736708860759
            }))

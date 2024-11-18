import pandas as pd
import json
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from calculator import calculate_fantasy_points_t20
from lazypredict.Supervised import LazyRegressor
import joblib
import matplotlib.pyplot as plt
import seaborn as sns


file_path = '/Users/ved14/Library/CloudStorage/GoogleDrive-v_umrajkar@ma.iitr.ac.in/My Drive/SEM7/extras/dream11-inter-iit/data/player_fantasy_points_t20.json'
with open(file_path, 'r') as file:
    player_data = json.load(file)

player_data =player_data
print("data fetched")
    
data = []
past_features = [
  "total_runs",
  "avg_runs_per_inning",
  "boundaries",
  "sixes",
  "average_sixes_per_inning",
  "fours",
  "average_fours_per_inning",
  "boundary_percent_per_inning",
  "wickets",
  "avg_wickets_per_inning",
  "catches_taken",
  "stumped_outs_made",
  "run_outs_made",
  "balls_faced",
  "avg_balls_faced_per_inning",
  "avg_batting_sr_per_inning",
  "avg_runs_ball_per_inning",
  "overs_bowled",
  "bowls_bowled",
  "average_bowls_bowled_per_inning",
  "avg_economy_rate_per_inning",
  "average_consecutive_dot_balls",
  "runs_given",
  "runs_given_ball_per_inning",
  "batting_sr_aa",
  
]

num_prev_matches = 10
num_prev_performance =100
print(len(player_data))

agg_cols =["Batting",
  "Bowling",
  "Games",
  "Won",
  "Drawn",
  "Win %",
  "Innings Batted",
  "Runs",
  "Singles",
  "Fours",
  "Sixes",
  "Dot Balls",
  "Balls Faced",
  "Outs",
  "Bowled Outs",
  "LBW Outs",
  "Hitwicket Outs",
  "Caught Outs",
  "Stumped Outs",
  "Run Outs",
  "Caught and Bowled Outs",
  "Dot Ball %",
  "Strike Turnover %",
  "Batting S/R",
  "Batting S/R MeanAD",
  "Batting Avg",
  "Mean Score",
  "Score MeanAD",
  "Scoring Consistency",
  "Boundary %",
  "Runs/Ball",
  "Mean Balls Faced",
  "Balls Faced MeanAD",
  "Survival Consistency",
  "Avg First Boundary Ball",
  "Dismissal Rate",
  "Boundary Rate",
  "Innings Bowled",
  "Runsgiven",
  "Singlesgiven",
  "Foursgiven",
  "Sixesgiven",
  "Wickets",
  "Balls Bowled",
  "Extras",
  "No Balls",
  "Wides",
  "Dot Balls Bowled",
  "Bowleds",
  "LBWs",
  "Hitwickets",
  "Caughts",
  "Stumpeds",
  "Caught and Bowleds",
  "Catches",
  "Runouts",
  "Stumpings",
  "Economy Rate",
  "Economy Rate MeanAD",
  "Dot Ball Bowled %",
  "Boundary Given %",
  "Bowling Avg",
  "Bowling Avg MeanAD",
  "Bowling S/R",
  "Bowling S/R MeanAD",
  "Runsgiven/Ball",
  "Boundary Given Rate",
  "Strike Turnovergiven %",
  "Avg Consecutive Dot Balls",
  "Runs Rate",
  "Runsgiven/Wicket",
  "Runs AA",
  "Runs/Ball AA",
  "Runsgiven AA",
  "Runsgiven/Ball AA"]
import itertools

# Define the number of players and matches per player to process
num_players = 1000  # Adjust this as needed
num_matches_per_player = 100  # Adjust this as needed

# Slice the player_data dictionary
subset_player_data = dict(itertools.islice(player_data.items(), num_players))

# Process each player's matches
for player, matches in subset_player_data.items():
    # Convert matches to a list of tuples and slice it
    matches = list(matches.items())[:num_matches_per_player]
    sorted_matches = sorted(matches, key=lambda x: x[0])

    # Lists to hold previous match stats
    prev_bat, prev_bowl, prev_field = [], [], []
    prev_stats = {feature: [] for feature in past_features}

    # Iterate through each match for the player
    for match_id, stats in sorted_matches:
        # Extract the points from the stats
        bat_points = stats.get('batting_points', 0)
        bowl_points = stats.get('bowling_points', 0)
        field_points = stats.get('fielding_points', 0)

        # Check if we have enough previous matches to create a row
        if len(prev_bat) >= num_prev_matches:
            # Create a new row for the current match
            row = {}

            # Add previous match points as features (batting, bowling, fielding)
            for i in range(min(len(prev_bat),num_prev_performance)):
                row[f'fantasy_bat_prev_{i+1}'] = prev_bat[-(i+1)]
                row[f'fantasy_bowl_prev_{i+1}'] = prev_bowl[-(i+1)]
                row[f'fantasy_field_prev_{i+1}'] = prev_field[-(i+1)]

            # Add previous match statistics as features
            for feature in prev_stats.keys():
                for i in range(num_prev_matches):
                    row[f'{feature}_prev_{i+1}'] = prev_stats[feature][-(i + 1)]

            # Add the current match points as the target variables
            row['bat_points'] = bat_points
            row['bowl_points'] = bowl_points
            row['field_points'] = field_points

            # Add other numerical features to the row
            for feature, value in stats.items():
                if feature not in ['bat_points', 'bowl_points', 'field_points', 'total_points']:
                    row[feature] = value
            for feature, value in stats.items():
                if feature  in agg_cols:
                    row[feature] = value

            # Append the row to the data list
            data.append(row)

        # Append the current match points and stats to the previous lists
        prev_bat.append(bat_points)
        prev_bowl.append(bowl_points)
        prev_field.append(field_points)

        # Append the current match's stats to the previous stats
        for feature in prev_stats.keys():
            prev_stats[feature].append(stats.get(feature, 0))

# Convert the data into a pandas DataFrame
df = pd.DataFrame(data)
df.to_csv('saved_features.csv', index=False)
df.fillna(0,inplace=True)
print(df)
df = df.iloc[:2000,:]

# Drop any rows with missing values (if any)
# df = df.dropna()

# Define the features (X) and target variables (y)
X = df.drop(['bat_points', 'bowl_points', 'field_points','batting_points', 'bowling_points', 'fielding_points' ,'total_runs', 'avg_runs_per_inning',
       'boundaries', 'sixes', 'average_sixes_per_inning', 'fours',
       'average_fours_per_inning', 'boundary_percent_per_inning', 'wickets',
       'avg_wickets_per_inning', 'catches_taken', 'stumped_outs_made',
       'run_outs_made', 'balls_faced', 'avg_balls_faced_per_inning',
       'avg_batting_sr_per_inning', 'avg_runs_ball_per_inning', 'overs_bowled',
       'bowls_bowled', 'average_bowls_bowled_per_inning',
       'avg_economy_rate_per_inning', 'average_consecutive_dot_balls',
       'runs_given', 'runs_given_ball_per_inning', 'batting_sr_aa'], axis=1)


from sklearn.linear_model import LassoCV
from sklearn.preprocessing import LabelEncoder

categorical_columns = X.select_dtypes(include=['object']).columns  # Detect categorical columns

# Apply Label Encoding to categorical columns
label_encoders = {}  # Dictionary to store label encoders for each categorical column
for col in categorical_columns:
    # Ensure the column is uniformly strings
    X[col] = X[col].astype(str)  # Convert everything to string before label encoding
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col])  # Label encode the column
    label_encoders[col] = le  # Store the encoder if needed later

# Convert all data to float (if it's not already)
X = X.astype(float)

# X = X.iloc[:3000,:]


print(X)
y_bat = df['bat_points']
y_bowl = df['bowl_points']
y_field = df['field_points']

print(X.shape)


# Train-test split for each target variable
X_train_bat, X_test_bat, y_train_bat, y_test_bat = train_test_split(X, y_bat, test_size=0.2, random_state=42)
X_train_bowl, X_test_bowl, y_train_bowl, y_test_bowl = train_test_split(X, y_bowl, test_size=0.2, random_state=42)
X_train_field, X_test_field, y_train_field, y_test_field = train_test_split(X, y_field, test_size=0.2, random_state=42)

# Step 1: LazyPredict Model Comparison for Batting Points
print("LazyPredict Model Comparison for Batting Points:")
lazy_bat = LazyRegressor()
models_bat, predictions_bat = lazy_bat.fit(X_train_bat, X_test_bat, y_train_bat, y_test_bat)
print(models_bat)

# Step 2: LazyPredict Model Comparison for Bowling Points
print("\nLazyPredict Model Comparison for Bowling Points:")
lazy_bowl = LazyRegressor()
models_bowl, predictions_bowl = lazy_bowl.fit(X_train_bowl, X_test_bowl, y_train_bowl, y_test_bowl)
print(models_bowl)

# Step 3: LazyPredict Model Comparison for Fielding Points
print("\nLazyPredict Model Comparison for Fielding Points:")
lazy_field = LazyRegressor()
models_field, predictions_field = lazy_field.fit(X_train_field, X_test_field, y_train_field, y_test_field)
print(models_field)

# Step 4: XGBoost for each target variable

# XGBoost model for Batting Points
xgb_model_bat = xgb.XGBRegressor(objective="reg:squarederror")
xgb_model_bat.fit(X_train_bat, y_train_bat)
y_pred_bat = xgb_model_bat.predict(X_test_bat)
rmse_bat = mean_squared_error(y_test_bat, y_pred_bat, squared=False)
print(f"XGBoost Batting Points RMSE: {rmse_bat}")

# XGBoost model for Bowling Points
xgb_model_bowl = xgb.XGBRegressor(objective="reg:squarederror")
xgb_model_bowl.fit(X_train_bowl, y_train_bowl)
y_pred_bowl = xgb_model_bowl.predict(X_test_bowl)
rmse_bowl = mean_squared_error(y_test_bowl, y_pred_bowl, squared=False)
print(f"XGBoost Bowling Points RMSE: {rmse_bowl}")

# XGBoost model for Fielding Points
xgb_model_field = xgb.XGBRegressor(objective="reg:squarederror")
xgb_model_field.fit(X_train_field, y_train_field)
y_pred_field = xgb_model_field.predict(X_test_field)
rmse_field = mean_squared_error(y_test_field, y_pred_field, squared=False)
print(f"XGBoost Fielding Points RMSE: {rmse_field}")

# Step 5: Save the trained models
joblib.dump(xgb_model_bat, 'xgb_model_batting.pth')
joblib.dump(xgb_model_bowl, 'xgb_model_bowling.pth')
joblib.dump(xgb_model_field, 'xgb_model_fielding.pth')

print("Models saved to .pth files successfully!")
print (df.dtypes)


def plot_feature_importance(model, feature_names, target_name):
    feature_importances = model.feature_importances_
    feature_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': feature_importances
    }).sort_values(by='Importance', ascending=False)

    plt.figure(figsize=(10, 6))
    feature_df =feature_df.iloc[:20,:]
    sns.barplot(x='Importance', y='Feature', data=feature_df)
    plt.title(f"Feature Importance for {target_name}")
    plt.tight_layout()
    plt.show()

plot_feature_importance(xgb_model_bat, X.columns, 'Batting Points')

plot_feature_importance(xgb_model_bowl, X.columns, 'Bowling Points')

plot_feature_importance(xgb_model_field, X.columns, 'Fielding Points')

# # Step 6: Save the trained models
# joblib.dump(xgb_model_bat, 'xgb_model_batting.pth')
# joblib.dump(xgb_model_bowl, 'xgb_model_bowling.pth')
# joblib.dump(xgb_model_field, 'xgb_model_fielding.pth')

# print("Models saved to .pth files successfully!")
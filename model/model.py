import pandas as pd
import json
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from calculator import calculate_fantasy_points_t20
from lazypredict.Supervised import LazyRegressor

# Load the JSON data
file_path = '/Users/ved14/Library/CloudStorage/GoogleDrive-v_umrajkar@ma.iitr.ac.in/My Drive/SEM7/extras/dream11-inter-iit/player_match_data.json'
with open(file_path, 'r') as file:
    player_data = json.load(file)


data = []

num_prev_matches = 2

for player, matches in player_data.items():
    sorted_matches = sorted(matches.items(), key=lambda x: x[0])

    prev_bat, prev_bowl, prev_field = [], [], []

    for match_id, stats in sorted_matches:
        points = calculate_fantasy_points_t20(stats)
        bat_points, bowl_points, field_points = points["batting_points"], points["bowling_points"], points["fielding_points"]

        if len(prev_bat) >= num_prev_matches:
            row = {}
            for i in range(num_prev_matches):
                row[f'fantasy_bat_prev_{i+1}'] = prev_bat[-(i+1)]
                row[f'fantasy_bowl_prev_{i+1}'] = prev_bowl[-(i+1)]
                row[f'fantasy_field_prev_{i+1}'] = prev_field[-(i+1)]

            row['bat_points'] = bat_points
            row['bowl_points'] = bowl_points
            row['field_points'] = field_points

            # Append row to data list
            data.append(row)

        prev_bat.append(bat_points)
        prev_bowl.append(bowl_points)
        prev_field.append(field_points)

# Convert data to DataFrame
df = pd.DataFrame(data)
df.to_csv("saved_features.csv")

# print(df.head())



X = df.drop(['bat_points', 'bowl_points', 'field_points'], axis=1)
y_bat = df['bat_points']
y_bowl = df['bowl_points']
y_field = df['field_points']

# Train-test split for each target variable
X_train_bat, X_test_bat, y_train_bat, y_test_bat = train_test_split(X, y_bat, test_size=0.2, random_state=42)
X_train_bowl, X_test_bowl, y_train_bowl, y_test_bowl = train_test_split(X, y_bowl, test_size=0.2, random_state=42)
X_train_field, X_test_field, y_train_field, y_test_field = train_test_split(X, y_field, test_size=0.2, random_state=42)

print("LazyPredict Model Comparison for Batting Points:")
lazy_bat = LazyRegressor()
models_bat, predictions_bat = lazy_bat.fit(X_train_bat, X_test_bat, y_train_bat, y_test_bat)
print(models_bat)

print("\nLazyPredict Model Comparison for Bowling Points:")
lazy_bowl = LazyRegressor()
models_bowl, predictions_bowl = lazy_bowl.fit(X_train_bowl, X_test_bowl, y_train_bowl, y_test_bowl)
print(models_bowl)

print("\nLazyPredict Model Comparison for Fielding Points:")
lazy_field = LazyRegressor()
models_field, predictions_field = lazy_field.fit(X_train_bat, X_test_bowl, y_train_field, y_test_field)
print(models_field)

# Step 4: XGBoost for each target
xgb_model_bat = xgb.XGBRegressor(objective="reg:squarederror")
xgb_model_bat.fit(X_train_bat, y_train_bat)
y_pred_bat = xgb_model_bat.predict(X_test_bat)
rmse_bat = mean_squared_error(y_test_bat, y_pred_bat, squared=False)
print(f"XGBoost Batting Points RMSE: {rmse_bat}")

xgb_model_bowl = xgb.XGBRegressor(objective="reg:squarederror")
xgb_model_bowl.fit(X_train_bowl, y_train_bowl)
y_pred_bowl = xgb_model_bowl.predict(X_test_bowl)
rmse_bowl = mean_squared_error(y_test_bowl, y_pred_bowl, squared=False)
print(f"XGBoost Bowling Points RMSE: {rmse_bowl}")

xgb_model_field = xgb.XGBRegressor(objective="reg:squarederror")
xgb_model_field.fit(X_train_field, y_train_field)
y_pred_field = xgb_model_field.predict(X_test_field)
rmse_field = mean_squared_error(y_test_field, y_pred_field, squared=False)
print(f"XGBoost Fielding Points RMSE: {rmse_field}")
# dream11-inter-iit


### Lazy Predict initial results

```
(env) (base) ➜  model git:(main) ✗ python model.py
Index(['fantasy_bat_prev_1', 'fantasy_bowl_prev_1', 'fantasy_field_prev_1',
       'fantasy_bat_prev_2', 'fantasy_bowl_prev_2', 'fantasy_field_prev_2',
       'total_runs_prev_1', 'total_runs_prev_2', 'avg_runs_per_inning_prev_1',
       'avg_runs_per_inning_prev_2', 'boundaries_prev_1', 'boundaries_prev_2',
       'sixes_prev_1', 'sixes_prev_2', 'average_sixes_per_inning_prev_1',
       'average_sixes_per_inning_prev_2', 'fours_prev_1', 'fours_prev_2',
       'average_fours_per_inning_prev_1', 'average_fours_per_inning_prev_2',
       'boundary_percent_per_inning_prev_1',    
       'boundary_percent_per_inning_prev_2', 'wickets_prev_1',
       'wickets_prev_2', 'avg_wickets_per_inning_prev_1',
       'avg_wickets_per_inning_prev_2', 'catches_taken_prev_1',
       'catches_taken_prev_2', 'stumped_outs_made_prev_1',
       'stumped_outs_made_prev_2', 'run_outs_made_prev_1',
       'run_outs_made_prev_2', 'balls_faced_prev_1', 'balls_faced_prev_2',
       'avg_balls_faced_per_inning_prev_1',
       'avg_balls_faced_per_inning_prev_2', 'avg_batting_sr_per_inning_prev_1',
       'avg_batting_sr_per_inning_prev_2', 'avg_runs_ball_per_inning_prev_1',
       'avg_runs_ball_per_inning_prev_2', 'overs_bowled_prev_1',
       'overs_bowled_prev_2', 'bowls_bowled_prev_1', 'bowls_bowled_prev_2',
       'average_bowls_bowled_per_inning_prev_1',
       'average_bowls_bowled_per_inning_prev_2',
       'avg_economy_rate_per_inning_prev_1',
       'avg_economy_rate_per_inning_prev_2',
       'average_consecutive_dot_balls_prev_1',
       'average_consecutive_dot_balls_prev_2', 'runs_given_prev_1',
       'runs_given_prev_2', 'runs_given_ball_per_inning_prev_1',
       'runs_given_ball_per_inning_prev_2', 'batting_sr_aa_prev_1',
       'batting_sr_aa_prev_2', 'total_runs', 'avg_runs_per_inning',
       'boundaries', 'sixes', 'average_sixes_per_inning', 'fours',
       'average_fours_per_inning', 'boundary_percent_per_inning', 'wickets',
       'avg_wickets_per_inning', 'catches_taken', 'stumped_outs_made',
       'run_outs_made', 'balls_faced', 'avg_balls_faced_per_inning',
       'avg_batting_sr_per_inning', 'avg_runs_ball_per_inning', 'overs_bowled',
       'bowls_bowled', 'average_bowls_bowled_per_inning',
       'avg_economy_rate_per_inning', 'average_consecutive_dot_balls',
       'runs_given', 'runs_given_ball_per_inning', 'batting_sr_aa'],
      dtype='object')
LazyPredict Model Comparison for Batting Points:
 98%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▊   | 41/42 [00:01<00:00, 25.13it/s][LightGBM] [Info] Auto-choosing row-wise multi-threading, the overhead of testing was 0.000844 seconds.
You can set `force_row_wise=true` to remove the overhead.
And if memory is not enough, you can set `force_col_wise=true`.
[LightGBM] [Info] Total Bins 2082
[LightGBM] [Info] Number of data points in the train set: 166, number of used features: 75
[LightGBM] [Info] Start training from score 56.578313
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 42/42 [00:01<00:00, 22.36it/s]
                               Adjusted R-Squared  R-Squared    RMSE  Time Taken
Model                                                                           
Lars                                      6580.63   -6418.15 3837.28        0.01
GaussianProcessRegressor                     3.20      -1.15   70.24        0.01
KernelRidge                                  2.46      -0.43   57.24        0.01
QuantileRegressor                            2.09      -0.07   49.50        0.02
DummyRegressor                               2.04      -0.01   48.16        0.00
SVR                                          1.96       0.06   46.37        0.01
NuSVR                                        1.92       0.10   45.44        0.01
MLPRegressor                                 1.58       0.44   35.93        0.07
KNeighborsRegressor                          1.40       0.61   29.81        0.07
ExtraTreeRegressor                           1.13       0.87   17.01        0.01
TweedieRegressor                             1.07       0.93   12.67        0.01
ElasticNet                                   1.04       0.96    9.34        0.01
LGBMRegressor                                1.03       0.97    8.39        0.10
HistGradientBoostingRegressor                1.03       0.97    8.16        0.19
LinearSVR                                    1.01       0.99    5.34        0.01
DecisionTreeRegressor                        1.01       0.99    4.90        0.01
ElasticNetCV                                 1.01       0.99    4.26        0.06
AdaBoostRegressor                            1.01       0.99    4.23        0.09
BaggingRegressor                             1.01       0.99    3.85        0.04
XGBRegressor                                 1.00       1.00    2.77        0.20
SGDRegressor                                 1.00       1.00    2.56        0.02
RandomForestRegressor                        1.00       1.00    2.49        0.27
ExtraTreesRegressor                          1.00       1.00    2.32        0.17
GradientBoostingRegressor                    1.00       1.00    2.23        0.20
Ridge                                        1.00       1.00    2.20        0.01
PassiveAggressiveRegressor                   1.00       1.00    1.92        0.01
HuberRegressor                               1.00       1.00    1.81        0.02
LassoLars                                    1.00       1.00    1.72        0.01
Lasso                                        1.00       1.00    1.72        0.01
RidgeCV                                      1.00       1.00    1.67        0.01
TransformedTargetRegressor                   1.00       1.00    1.63        0.01
RANSACRegressor                              1.00       1.00    1.63        0.01
LinearRegression                             1.00       1.00    1.63        0.02
BayesianRidge                                1.00       1.00    1.62        0.02
OrthogonalMatchingPursuit                    1.00       1.00    1.25        0.01
OrthogonalMatchingPursuitCV                  1.00       1.00    1.25        0.01
LassoCV                                      1.00       1.00    1.23        0.04
LassoLarsIC                                  1.00       1.00    1.23        0.02
LassoLarsCV                                  1.00       1.00    1.22        0.03
LarsCV                                       1.00       1.00    1.22        0.04

LazyPredict Model Comparison for Bowling Points:
 98%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▊   | 41/42 [00:01<00:00, 25.82it/s][LightGBM] [Info] Auto-choosing row-wise multi-threading, the overhead of testing was 0.000646 seconds.
You can set `force_row_wise=true` to remove the overhead.
And if memory is not enough, you can set `force_col_wise=true`.
[LightGBM] [Info] Total Bins 2082
[LightGBM] [Info] Number of data points in the train set: 166, number of used features: 75
[LightGBM] [Info] Start training from score 21.012048
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 42/42 [00:01<00:00, 24.95it/s]
                               Adjusted R-Squared   R-Squared      RMSE  Time Taken
Model                                                                              
Lars                                   9164724.47 -8941192.62 112178.48        0.01
PoissonRegressor                             3.29       -1.23     56.03        0.02
QuantileRegressor                            2.34       -0.31     42.88        0.02
GaussianProcessRegressor                     2.34       -0.31     42.88        0.01
DummyRegressor                               2.03       -0.00     37.52        0.00
SVR                                          2.01        0.01     37.27        0.01
RANSACRegressor                              1.98        0.04     36.72        0.11
NuSVR                                        1.93        0.09     35.75        0.01
KernelRidge                                  1.32        0.69     20.98        0.01
KNeighborsRegressor                          1.25        0.76     18.43        0.01
MLPRegressor                                 1.20        0.80     16.57        0.09
LGBMRegressor                                1.11        0.89     12.38        0.15
HistGradientBoostingRegressor                1.11        0.90     12.08        0.19
TweedieRegressor                             1.10        0.91     11.44        0.01
ExtraTreeRegressor                           1.09        0.91     11.11        0.01
ElasticNet                                   1.05        0.95      8.11        0.01
BaggingRegressor                             1.02        0.98      5.62        0.02
SGDRegressor                                 1.02        0.98      4.83        0.01
ElasticNetCV                                 1.01        0.99      4.15        0.06
LinearSVR                                    1.01        0.99      4.13        0.04
PassiveAggressiveRegressor                   1.01        0.99      3.95        0.01
ExtraTreesRegressor                          1.01        0.99      3.88        0.07
RandomForestRegressor                        1.01        0.99      3.40        0.22
Ridge                                        1.01        0.99      2.87        0.01
AdaBoostRegressor                            1.01        0.99      2.68        0.03
DecisionTreeRegressor                        1.00        1.00      2.47        0.01
HuberRegressor                               1.00        1.00      1.95        0.02
RidgeCV                                      1.00        1.00      1.23        0.01
OrthogonalMatchingPursuit                    1.00        1.00      1.15        0.01
GradientBoostingRegressor                    1.00        1.00      1.15        0.19
LinearRegression                             1.00        1.00      1.13        0.01
TransformedTargetRegressor                   1.00        1.00      1.13        0.01
BayesianRidge                                1.00        1.00      1.12        0.01
LassoLars                                    1.00        1.00      1.12        0.01
Lasso                                        1.00        1.00      1.12        0.01
LassoLarsCV                                  1.00        1.00      1.11        0.03
LassoCV                                      1.00        1.00      1.11        0.05
LarsCV                                       1.00        1.00      1.10        0.05
OrthogonalMatchingPursuitCV                  1.00        1.00      1.09        0.01
LassoLarsIC                                  1.00        1.00      1.00        0.02
XGBRegressor                                 1.00        1.00      0.20        0.14

LazyPredict Model Comparison for Fielding Points:
 98%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▊   | 41/42 [00:01<00:00, 27.01it/s][LightGBM] [Info] Auto-choosing row-wise multi-threading, the overhead of testing was 0.000791 seconds.
You can set `force_row_wise=true` to remove the overhead.
And if memory is not enough, you can set `force_col_wise=true`.
[LightGBM] [Info] Total Bins 2082
[LightGBM] [Info] Number of data points in the train set: 166, number of used features: 75
[LightGBM] [Info] Start training from score 6.867470
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
[LightGBM] [Warning] No further splits with positive gain, best gain: -inf
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 42/42 [00:01<00:00, 25.52it/s]
                               Adjusted R-Squared  R-Squared   RMSE  Time Taken
Model                                                                          
Lars                                       401.58    -389.81 298.66        0.01
PoissonRegressor                             3.82      -1.75  25.04        0.01
QuantileRegressor                            2.73      -0.69  19.65        0.02
GaussianProcessRegressor                     2.73      -0.69  19.65        0.01
NuSVR                                        2.20      -0.17  16.37        0.01
DummyRegressor                               2.17      -0.14  16.15        0.00
SVR                                          2.15      -0.12  16.01        0.01
KNeighborsRegressor                          1.66       0.36  12.11        0.01
RANSACRegressor                              1.46       0.56  10.07        0.10
MLPRegressor                                 1.45       0.56  10.00        0.08
HistGradientBoostingRegressor                1.39       0.62   9.27        0.15
LGBMRegressor                                1.37       0.64   9.09        0.15
TweedieRegressor                             1.29       0.72   7.97        0.01
KernelRidge                                  1.25       0.75   7.50        0.01
DecisionTreeRegressor                        1.24       0.77   7.25        0.01
ExtraTreeRegressor                           1.17       0.83   6.23        0.01
ElasticNet                                   1.16       0.84   6.02        0.01
BaggingRegressor                             1.14       0.86   5.65        0.03
RandomForestRegressor                        1.12       0.88   5.23        0.14
AdaBoostRegressor                            1.12       0.88   5.14        0.04
XGBRegressor                                 1.11       0.90   4.87        0.16
ExtraTreesRegressor                          1.08       0.92   4.28        0.07
GradientBoostingRegressor                    1.08       0.92   4.23        0.18
LassoLars                                    1.04       0.96   2.84        0.02
Lasso                                        1.04       0.96   2.84        0.01
PassiveAggressiveRegressor                   1.02       0.98   2.17        0.01
HuberRegressor                               1.02       0.98   2.14        0.02
LinearSVR                                    1.02       0.98   2.14        0.06
SGDRegressor                                 1.02       0.98   1.94        0.01
Ridge                                        1.02       0.98   1.92        0.01
RidgeCV                                      1.02       0.98   1.92        0.01
TransformedTargetRegressor                   1.02       0.98   1.90        0.01
LinearRegression                             1.02       0.98   1.90        0.01
BayesianRidge                                1.02       0.98   1.89        0.01
ElasticNetCV                                 1.02       0.98   1.88        0.04
LassoCV                                      1.01       0.99   1.80        0.12
LassoLarsCV                                  1.01       0.99   1.80        0.03
LassoLarsIC                                  1.01       0.99   1.79        0.01
LarsCV                                       1.01       0.99   1.77        0.05
OrthogonalMatchingPursuitCV                  1.01       0.99   1.75        0.01
OrthogonalMatchingPursuit                    1.01       0.99   1.75        0.01
XGBoost Batting Points RMSE: 2.76778876642957
XGBoost Bowling Points RMSE: 0.2035517165114903
XGBoost Fielding Points RMSE: 4.870118039430566
Models saved to .pth files successfully!
```
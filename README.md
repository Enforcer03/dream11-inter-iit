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
 98%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▊   | 41/42 [00:04<00:00, 12.34it/s][LightGBM] [Info] Auto-choosing row-wise multi-threading, the overhead of testing was 0.003086 seconds.

100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 42/42 [00:05<00:00,  7.92it/s]
                               Adjusted R-Squared    R-Squared     RMSE  Time Taken
Model                                                                              
Lars                                  14943960.94 -14579472.11 19739.44        0.04
GaussianProcessRegressor                     2.20        -0.17     5.59        0.05
DummyRegressor                               2.07        -0.05     5.29        0.01
QuantileRegressor                            2.03        -0.00     5.17        0.03
NuSVR                                        1.58         0.43     3.89        0.01
SVR                                          1.54         0.47     3.76        0.01
KNeighborsRegressor                          1.46         0.55     3.46        0.10
PassiveAggressiveRegressor                   1.39         0.62     3.18        0.01
TweedieRegressor                             1.22         0.79     2.40        0.02
MLPRegressor                                 1.21         0.79     2.35        0.13
ElasticNet                                   1.21         0.79     2.35        0.02
KernelRidge                                  1.18         0.82     2.18        0.03
LassoLars                                    1.18         0.82     2.16        0.01
Lasso                                        1.18         0.82     2.16        0.02
LinearSVR                                    1.15         0.85     1.99        0.05
OrthogonalMatchingPursuitCV                  1.15         0.85     1.98        0.02
ExtraTreeRegressor                           1.15         0.86     1.96        0.02
RANSACRegressor                              1.15         0.86     1.96        0.20
SGDRegressor                                 1.15         0.86     1.95        0.01
HuberRegressor                               1.14         0.86     1.94        0.05
ElasticNetCV                                 1.14         0.86     1.94        0.26
Ridge                                        1.14         0.86     1.90        0.01
LarsCV                                       1.14         0.87     1.89        0.11
LassoCV                                      1.14         0.87     1.89        0.24
LinearRegression                             1.14         0.87     1.89        0.01
TransformedTargetRegressor                   1.14         0.87     1.89        0.01
RidgeCV                                      1.14         0.87     1.89        0.01
BayesianRidge                                1.14         0.87     1.88        0.05
LassoLarsIC                                  1.13         0.87     1.84        0.03
LassoLarsCV                                  1.13         0.88     1.82        0.04
OrthogonalMatchingPursuit                    1.13         0.88     1.82        0.01
HistGradientBoostingRegressor                1.10         0.90     1.63        1.25
LGBMRegressor                                1.09         0.92     1.49        0.47
DecisionTreeRegressor                        1.05         0.95     1.20        0.03
AdaBoostRegressor                            1.04         0.96     1.03        0.42
BaggingRegressor                             1.03         0.97     0.93        0.08
RandomForestRegressor                        1.02         0.98     0.74        0.43
XGBRegressor                                 1.02         0.98     0.66        0.29
ExtraTreesRegressor                          1.01         0.99     0.58        0.29
GradientBoostingRegressor                    1.00         1.00     0.27        0.36

LazyPredict Model Comparison for Bowling Points:
 98%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▊   | 41/42 [00:04<00:00, 12.40it/s][LightGBM] [Info] Auto-choosing col-wise multi-threading, the overhead of testing was 0.000963 seconds.
You can set `force_col_wise=true` to remove the overhead.
[LightGBM] [Info] Total Bins 2034
[LightGBM] [Info] Number of data points in the train set: 166, number of used features: 75
[LightGBM] [Info] Start training from score 36.463855

100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 42/42 [00:05<00:00,  7.91it/s]
                               Adjusted R-Squared  R-Squared   RMSE  Time Taken
Model                                                                          
Lars                                        98.57     -94.19 614.17        0.05
RANSACRegressor                              6.79      -4.65 149.67        0.26
PoissonRegressor                             3.22      -1.17  92.63        0.06
QuantileRegressor                            2.36      -0.33  72.62        0.04
GaussianProcessRegressor                     2.36      -0.33  72.62        0.02
SVR                                          2.11      -0.08  65.49        0.01
DummyRegressor                               2.03      -0.00  62.95        0.01
NuSVR                                        2.00       0.03  62.08        0.02
KernelRidge                                  1.34       0.66  36.46        0.03
MLPRegressor                                 1.24       0.77  30.28        0.32
KNeighborsRegressor                          1.22       0.79  28.84        0.02
TweedieRegressor                             1.09       0.91  18.38        0.01
LGBMRegressor                                1.09       0.92  18.32        0.47
HistGradientBoostingRegressor                1.09       0.92  18.17        1.87
ElasticNet                                   1.05       0.96  13.25        0.01
BaggingRegressor                             1.02       0.98   9.23        0.05
DecisionTreeRegressor                        1.02       0.98   8.63        0.01
ExtraTreesRegressor                          1.01       0.99   7.42        0.16
LarsCV                                       1.01       0.99   7.39        0.14
LinearSVR                                    1.01       0.99   6.94        0.05
ElasticNetCV                                 1.01       0.99   6.65        0.12
RandomForestRegressor                        1.01       0.99   6.37        0.27
SGDRegressor                                 1.01       0.99   6.34        0.01
PassiveAggressiveRegressor                   1.01       0.99   4.81        0.02
AdaBoostRegressor                            1.01       0.99   4.68        0.07
Ridge                                        1.01       0.99   4.65        0.01
ExtraTreeRegressor                           1.00       1.00   3.97        0.01
HuberRegressor                               1.00       1.00   3.20        0.08
RidgeCV                                      1.00       1.00   2.85        0.01
BayesianRidge                                1.00       1.00   2.82        0.02
GradientBoostingRegressor                    1.00       1.00   2.64        0.38
LinearRegression                             1.00       1.00   2.60        0.04
TransformedTargetRegressor                   1.00       1.00   2.60        0.01
LassoLars                                    1.00       1.00   2.48        0.03
Lasso                                        1.00       1.00   2.48        0.04
LassoLarsCV                                  1.00       1.00   2.14        0.08
LassoCV                                      1.00       1.00   2.13        0.11
LassoLarsIC                                  1.00       1.00   2.11        0.06
OrthogonalMatchingPursuit                    1.00       1.00   2.07        0.02
OrthogonalMatchingPursuitCV                  1.00       1.00   2.07        0.02
XGBRegressor                                 1.00       1.00   0.07        0.27

LazyPredict Model Comparison for Fielding Points:
 98%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▊   | 41/42 [00:03<00:00, 13.84it/s][LightGBM] [Info] Auto-choosing row-wise multi-threading, the overhead of testing was 0.000900 seconds.
You can set `force_row_wise=true` to remove the overhead.
And if memory is not enough, you can set `force_col_wise=true`.

100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 42/42 [00:04<00:00,  9.93it/s]
                               Adjusted R-Squared  R-Squared  RMSE  Time Taken
Model                                                                         
PoissonRegressor                             4.29      -2.21 27.46        0.02
Lars                                         3.41      -1.35 23.49        0.03
QuantileRegressor                            2.75      -0.70 20.01        0.03
GaussianProcessRegressor                     2.74      -0.70 20.00        0.01
NuSVR                                        2.22      -0.19 16.71        0.01
DummyRegressor                               2.17      -0.14 16.39        0.01
SVR                                          2.16      -0.13 16.33        0.01
RANSACRegressor                              2.07      -0.04 15.65        0.28
KNeighborsRegressor                          1.63       0.38 12.05        0.02
MLPRegressor                                 1.42       0.59  9.78        0.11
HistGradientBoostingRegressor                1.34       0.67  8.86        1.34
LGBMRegressor                                1.33       0.68  8.66        0.55
TweedieRegressor                             1.27       0.74  7.80        0.01
KernelRidge                                  1.24       0.77  7.34        0.02
DecisionTreeRegressor                        1.14       0.86  5.76        0.02
ElasticNet                                   1.14       0.86  5.74        0.01
AdaBoostRegressor                            1.12       0.88  5.22        0.09
ExtraTreeRegressor                           1.09       0.91  4.54        0.02
RandomForestRegressor                        1.09       0.92  4.45        0.25
BaggingRegressor                             1.08       0.92  4.42        0.06
GradientBoostingRegressor                    1.07       0.93  4.03        0.28
XGBRegressor                                 1.07       0.93  4.00        0.28
ExtraTreesRegressor                          1.06       0.94  3.75        0.12
LassoLars                                    1.02       0.98  2.28        0.02
Lasso                                        1.02       0.98  2.28        0.02
LinearSVR                                    1.01       0.99  1.85        0.06
HuberRegressor                               1.01       0.99  1.76        0.05
ElasticNetCV                                 1.00       1.00  0.97        0.09
PassiveAggressiveRegressor                   1.00       1.00  0.95        0.01
Ridge                                        1.00       1.00  0.94        0.01
RidgeCV                                      1.00       1.00  0.94        0.01
SGDRegressor                                 1.00       1.00  0.93        0.01
LinearRegression                             1.00       1.00  0.92        0.01
TransformedTargetRegressor                   1.00       1.00  0.92        0.01
OrthogonalMatchingPursuit                    1.00       1.00  0.90        0.01
BayesianRidge                                1.00       1.00  0.89        0.02
LassoCV                                      1.00       1.00  0.88        0.08
LassoLarsCV                                  1.00       1.00  0.87        0.06
LarsCV                                       1.00       1.00  0.86        0.15
LassoLarsIC                                  1.00       1.00  0.86        0.02
OrthogonalMatchingPursuitCV                  1.00       1.00  0.79        0.01
XGBoost Batting Points RMSE: 0.6608541732771039
XGBoost Bowling Points RMSE: 0.06888652072253205
XGBoost Fielding Points RMSE: 3.9987071740533846
Models saved to .pth files successfully!
(env) (base) ➜  model git:(main) ✗ 
```
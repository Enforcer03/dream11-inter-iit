# dream11-inter-iit


### Lazy Predict initial results

```
LazyPredict Model Comparison for Batting Points:
 98%|███████████████████████████████████████████████████████████████████████████████████████▊  | 41/42 [00:02<00:00, 19.32it/s][LightGBM] [Info] Auto-choosing row-wise multi-threading, the overhead of testing was 0.000440 seconds.
You can set `force_row_wise=true` to remove the overhead.
And if memory is not enough, you can set `force_col_wise=true`.
[LightGBM] [Info] Total Bins 316
[LightGBM] [Info] Number of data points in the train set: 1968, number of used features: 6
[LightGBM] [Info] Start training from score 22.900915
100%|██████████████████████████████████████████████████████████████████████████████████████████| 42/42 [00:02<00:00, 17.96it/s]
                               Adjusted R-Squared  R-Squared     RMSE  Time Taken
Model                                                                            
MLPRegressor                                 0.09       0.10    31.97        0.35
TransformedTargetRegressor                   0.05       0.07    32.65        0.00
Lars                                         0.05       0.07    32.65        0.00
LinearRegression                             0.05       0.07    32.65        0.00
Ridge                                        0.05       0.07    32.65        0.00
RidgeCV                                      0.05       0.07    32.65        0.00
LassoLarsIC                                  0.05       0.07    32.66        0.01
BayesianRidge                                0.05       0.07    32.66        0.01
ElasticNetCV                                 0.05       0.06    32.67        0.02
OrthogonalMatchingPursuitCV                  0.05       0.06    32.69        0.01
LarsCV                                       0.05       0.06    32.69        0.01
LassoLarsCV                                  0.05       0.06    32.69        0.01
LassoCV                                      0.05       0.06    32.69        0.02
SGDRegressor                                 0.05       0.06    32.71        0.00
Lasso                                        0.05       0.06    32.78        0.00
LassoLars                                    0.05       0.06    32.78        0.00
ElasticNet                                   0.05       0.06    32.81        0.00
GradientBoostingRegressor                    0.04       0.06    32.83        0.09
TweedieRegressor                             0.04       0.05    32.84        0.00
OrthogonalMatchingPursuit                    0.01       0.02    33.40        0.00
DummyRegressor                              -0.01      -0.00    33.81        0.00
NuSVR                                       -0.02      -0.00    33.84        0.06
AdaBoostRegressor                           -0.02      -0.00    33.85        0.03
LGBMRegressor                               -0.04      -0.03    34.25        0.27
HistGradientBoostingRegressor               -0.05      -0.04    34.43        0.40
PassiveAggressiveRegressor                  -0.05      -0.04    34.46        0.00
RandomForestRegressor                       -0.07      -0.06    34.71        0.26
HuberRegressor                              -0.07      -0.06    34.73        0.01
KNeighborsRegressor                         -0.10      -0.09    35.26        0.01
BaggingRegressor                            -0.12      -0.11    35.54        0.03
SVR                                         -0.14      -0.13    35.90        0.08
LinearSVR                                   -0.15      -0.14    36.08        0.00
XGBRegressor                                -0.18      -0.17    36.48        0.18
ExtraTreesRegressor                         -0.19      -0.18    36.62        0.16
QuantileRegressor                           -0.25      -0.23    37.51        0.07
RANSACRegressor                             -0.35      -0.34    39.06        0.03
KernelRidge                                 -0.48      -0.46    40.87        0.06
ExtraTreeRegressor                          -0.83      -0.81    45.44        0.00
DecisionTreeRegressor                       -0.93      -0.91    46.68        0.01
GaussianProcessRegressor               -389589.93 -384829.15 20957.90        0.11

LazyPredict Model Comparison for Bowling Points:
 90%|█████████████████████████████████████████████████████████████████████████████████▍        | 38/42 [00:01<00:00, 21.96it/s][LightGBM] [Info] Auto-choosing row-wise multi-threading, the overhead of testing was 0.000345 seconds.
You can set `force_row_wise=true` to remove the overhead.
And if memory is not enough, you can set `force_col_wise=true`.
[LightGBM] [Info] Total Bins 316
[LightGBM] [Info] Number of data points in the train set: 1968, number of used features: 6
[LightGBM] [Info] Start training from score 19.209350
100%|██████████████████████████████████████████████████████████████████████████████████████████| 42/42 [00:02<00:00, 19.58it/s]
                               Adjusted R-Squared  R-Squared     RMSE  Time Taken
Model                                                                            
GradientBoostingRegressor                    0.17       0.18    28.28        0.08
MLPRegressor                                 0.16       0.17    28.38        0.34
Lasso                                        0.10       0.11    29.45        0.00
LassoLars                                    0.10       0.11    29.45        0.00
ElasticNet                                   0.10       0.11    29.48        0.00
SGDRegressor                                 0.10       0.11    29.49        0.00
ElasticNetCV                                 0.09       0.11    29.50        0.02
LassoCV                                      0.09       0.11    29.50        0.02
LarsCV                                       0.09       0.10    29.51        0.01
LassoLarsCV                                  0.09       0.10    29.51        0.01
BayesianRidge                                0.09       0.10    29.52        0.00
RidgeCV                                      0.09       0.10    29.53        0.00
Ridge                                        0.09       0.10    29.53        0.00
TransformedTargetRegressor                   0.09       0.10    29.53        0.00
LassoLarsIC                                  0.09       0.10    29.53        0.00
LinearRegression                             0.09       0.10    29.53        0.00
Lars                                         0.09       0.10    29.53        0.01
OrthogonalMatchingPursuitCV                  0.09       0.10    29.56        0.00
TweedieRegressor                             0.09       0.10    29.57        0.00
HistGradientBoostingRegressor                0.07       0.08    29.86        0.38
LGBMRegressor                                0.07       0.08    29.86        0.27
RandomForestRegressor                        0.07       0.08    29.93        0.22
AdaBoostRegressor                            0.07       0.08    29.97        0.02
NuSVR                                        0.06       0.07    30.10        0.06
OrthogonalMatchingPursuit                    0.05       0.06    30.18        0.00
XGBRegressor                                 0.04       0.05    30.36        0.17
SVR                                          0.03       0.04    30.52        0.07
HuberRegressor                               0.02       0.04    30.62        0.01
ExtraTreesRegressor                          0.02       0.03    30.69        0.14
BaggingRegressor                            -0.01       0.00    31.12        0.03
LinearSVR                                   -0.01       0.00    31.19        0.00
DummyRegressor                              -0.01      -0.00    31.21        0.00
PassiveAggressiveRegressor                  -0.02      -0.01    31.29        0.00
KNeighborsRegressor                         -0.02      -0.01    31.37        0.01
KernelRidge                                 -0.33      -0.31    35.70        0.05
QuantileRegressor                           -0.36      -0.34    36.12        0.06
ExtraTreeRegressor                          -0.37      -0.35    36.26        0.00
RANSACRegressor                             -0.42      -0.40    36.93        0.03
DecisionTreeRegressor                       -0.67      -0.65    40.10        0.01
GaussianProcessRegressor               -296781.91 -293155.24 16890.62        0.10

LazyPredict Model Comparison for Fielding Points:
 90%|█████████████████████████████████████████████████████████████████████████████████▍        | 38/42 [00:01<00:00, 20.58it/s][LightGBM] [Info] Auto-choosing row-wise multi-threading, the overhead of testing was 0.000355 seconds.
You can set `force_row_wise=true` to remove the overhead.
And if memory is not enough, you can set `force_col_wise=true`.
[LightGBM] [Info] Total Bins 316
[LightGBM] [Info] Number of data points in the train set: 1968, number of used features: 6
[LightGBM] [Info] Start training from score 3.180894
100%|██████████████████████████████████████████████████████████████████████████████████████████| 42/42 [00:02<00:00, 18.23it/s]
                               Adjusted R-Squared  R-Squared    RMSE  Time Taken
Model                                                                           
PoissonRegressor                             0.09       0.10    5.29        0.01
MLPRegressor                                 0.08       0.09    5.32        0.35
OrthogonalMatchingPursuitCV                  0.07       0.08    5.34        0.00
LassoLarsIC                                  0.07       0.08    5.34        0.00
LassoLarsCV                                  0.07       0.08    5.34        0.01
LarsCV                                       0.07       0.08    5.34        0.01
LinearRegression                             0.07       0.08    5.34        0.00
Lars                                         0.07       0.08    5.34        0.00
TransformedTargetRegressor                   0.07       0.08    5.34        0.00
Ridge                                        0.07       0.08    5.34        0.00
RidgeCV                                      0.07       0.08    5.34        0.00
LassoCV                                      0.07       0.08    5.34        0.02
BayesianRidge                                0.07       0.08    5.34        0.00
ElasticNetCV                                 0.07       0.08    5.34        0.02
SGDRegressor                                 0.07       0.08    5.35        0.00
TweedieRegressor                             0.06       0.07    5.39        0.00
ElasticNet                                   0.03       0.04    5.46        0.00
OrthogonalMatchingPursuit                    0.02       0.03    5.49        0.00
GradientBoostingRegressor                    0.00       0.01    5.54        0.08
Lasso                                       -0.01       0.00    5.58        0.00
LassoLars                                   -0.01       0.00    5.58        0.00
DummyRegressor                              -0.02      -0.00    5.60        0.00
HistGradientBoostingRegressor               -0.05      -0.03    5.67        0.38
NuSVR                                       -0.06      -0.04    5.70        0.19
LGBMRegressor                               -0.08      -0.07    5.76        0.28
KernelRidge                                 -0.17      -0.15    6.00        0.05
KNeighborsRegressor                         -0.20      -0.18    6.07        0.01
SVR                                         -0.21      -0.19    6.09        0.09
RandomForestRegressor                       -0.22      -0.21    6.14        0.22
HuberRegressor                              -0.26      -0.25    6.24        0.01
QuantileRegressor                           -0.27      -0.25    6.24        0.04
RANSACRegressor                             -0.27      -0.25    6.24        0.02
LinearSVR                                   -0.27      -0.25    6.24        0.00
XGBRegressor                                -0.30      -0.29    6.33        0.17
BaggingRegressor                            -0.32      -0.30    6.37        0.03
ExtraTreesRegressor                         -0.45      -0.43    6.67        0.13
AdaBoostRegressor                           -0.59      -0.57    6.99        0.02
PassiveAggressiveRegressor                  -1.21      -1.19    8.25        0.00
ExtraTreeRegressor                          -1.37      -1.34    8.54        0.00
DecisionTreeRegressor                       -1.61      -1.57    8.96        0.01
GaussianProcessRegressor               -373690.36 -369123.86 3390.93        0.09
XGBoost Batting Points RMSE: 36.47897030129975
XGBoost Bowling Points RMSE: 30.363479101607915
XGBoost Fielding Points RMSE: 6.33402583785739
```
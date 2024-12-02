graph TD
Start[Start Application]
Title[Display Title and Description]
Sidebar[Initialize Sidebar Options]
Format[Select Format (T20, ODI, Test)]
Options{Choose Action}
LoadSquads[Load Squads from Scheduled Matches]
GetSnapshot[Get Team Selection Snapshot]
SelectMatch[Select Match]
DisplaySquads[Display Squads]
AssessPlayers[Assess Players]
OptimizerConfig[Solver and Optimizer Configuration]
Optimization[Optimize Team]
DisplayResults[Display Results and Metrics]
GetOptimalTeam[Get Optimal Team Using LLM]
End[End Application]

    Start --> Title --> Sidebar --> Format --> Options
    Options -->|Option| LoadSquads
    Options -->|Option| GetSnapshot --> End
    LoadSquads --> SelectMatch --> DisplaySquads --> AssessPlayers
    AssessPlayers --> OptimizerConfig --> Optimization --> DisplayResults --> GetOptimalTeam --> End

#Data Preprocessing Files

1. aggregate_points --> extracts aggregate statistics of all players from cricketstats for each format T20/ODI/Test
2. Data_extracter --> extracts PlayerWise data for each MatchID, from cricketstats for each format T20/ODI/Test.

- Note: Some features like _Maiden Overs_ , _Fours_, _Sixes_ , _Bowled_, _LBW_ were not readily available, we have done changes in the **Cricketstats** source code since it is an open source library.

3. Match_level_players --> Generates two different formats of squads

- _MatchIDwise_ squads for both the teams (for Model UI)
- _Datewise_ hierarchial squads for both the teams (For Frontend). In this, wev have also made an adddtional squad for both the teams, which will include the players who played for that team in last 10 matches of the same format.

4. Json_Formatter --> Formats the raw data from cricketstats to the processable Json data
5. testing --> generates fantasy points from the interim Json data that we received from Json_formatter for each format T20/ODI/Test.

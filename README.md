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
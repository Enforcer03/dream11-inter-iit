<img src="media/d11_logo.png" width="200">

# AI Team Builder - Inter IIT 13.0

## Directory Structure

- `model/`: contains all the logic for the methodology implemented and other experiments.
- `data_preprocessing/`: COMPLETE TEXT
- `UI/`: contains the Product UI for the user to interact and predict the optimal team
<!-- add the test of the directories and their descriptions -->

## Dependencies

<!-- <mention what all to install (libraries)> -->

## How to run the Product UI?

- [`Product UI README`](./UI/README.md)

<!-- <mention steps to run the product UI> -->
<!-- <include screenshots> -->

## How to run the Model UI?

- [`Model README`](./model/README.md)

<!-- <mention steps to run the Model UI>
<and a walkthrough of the UI with SS> -->

## Preprocessing

<!-- mention how to run preprocessing -->

- [`Data Preprocessing README`](./data_preprocessing/README.md)

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

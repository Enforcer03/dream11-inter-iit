<img src="d11_logo.png" width="200">

# AI Team Builder - Inter IIT 13.0

## Directory Structure

- `model/`: contains all the logic for the methodology implemented and other experiments.
- `data_preprocessing/`: COMPLETE TEXT
- `UI/`: contains the Product UI which provides interactive experience to the user and predict the optimal team
<!-- add the test of the directories and their descriptions -->

## Dependencies

<!-- <mention what all to install (libraries)> -->

## How to run the Product UI?

- [`Product UI README`](./UI/README.md)

1. **Install Yarn** (if not already installed):

   ```bash
   npm install --global yarn
   ```

2. Navigate to the `UI/` folder:

   ```bash
   cd UI
   ```

3. Install the dependencies:

   ```bash
   yarn install
   ```

4. Start the development server:

   ```bash
   yarn dev
   ```

5. Open your browser and navigate to:

   ```
   http://localhost:3000
   ```

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

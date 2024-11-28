import streamlit as st
import openai
import json
import os
from dotenv import load_dotenv
import plotly.graph_objects as go
import re
from heuristic_solver import (
    load_player_fantasy_points_for_optimization,
    compute_player_stats,
    compute_covariance_matrix,
    optimize_team_sharpe,
    optimize_team_advanced
)
import datetime
from utils import get_optimal_team_llm, get_past_match_performance, best_team_button, extract_date_from_match_key, plot_team_distribution
import pandas as pd
import numpy as np

@st.cache_data()
def load_sample_players(json_file):
    with open(json_file, "r") as file:
        return json.load(file)

@st.cache_data()
def get_optim_file(fantasy_points_path):
    return load_player_fantasy_points_for_optimization(fantasy_points_path)

@st.cache_data()
def load_player_fantasy_points(json_file):
    with open(json_file, "r") as file:
        data = json.load(file)
        sorted_data = {}
        for player, matches in data.items():
            match_list = list(matches.items())
            def extract_date_from_match_key(match_key):
                date_pattern = r'(\d{4}-\d{2}-\d{2})'
                match = re.search(date_pattern, match_key)
                if match:
                    date_str = match.group(1)
                    try:
                        date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
                    except ValueError:
                        date = datetime.datetime.min
                else:
                    date = datetime.datetime.min
                return date
            match_list_sorted = sorted(match_list, key=lambda x: extract_date_from_match_key(x[0]))
            sorted_data[player] = match_list_sorted
        return sorted_data

st.title("Fantasy Cricket Team Selector")
st.markdown("""
    - Load data from scheduled matches or manually input details.
    - Generate the best team of 11 players using AI.
""")

st.sidebar.header("Options")
st.sidebar.image("logo-model-ui.jpg")
format_selected = st.sidebar.selectbox("Select Format", ['T20', 'ODI', 'Test'])
upload_sample = st.sidebar.checkbox("Load Sample Players from JSON")
manual_input = st.sidebar.checkbox("Add Players Manually")
squad_info = st.sidebar.checkbox("Load squads from scheduled matches")
assess_players = st.sidebar.checkbox("Assess Players from the squads")
optimize_team_option = st.sidebar.checkbox("Optimize Team Selection")

format_lower = format_selected.lower().replace('-', '').replace(' ', '')
data_dir = "/Users/ved14/Library/CloudStorage/GoogleDrive-v_umrajkar@ma.iitr.ac.in/My Drive/SEM7/extras/dream11-inter-iit/data"
fantasy_points_path = f"../data/player_fantasy_points_{format_lower}.json"
json_file_path = f"../data/{format_selected}_Match_Level_Till_training_date_Players.json"
aggregate_stats_path = f"../data/aggregate_cricket_stats_{format_lower}.json"

try:
    match_data = load_sample_players(json_file_path)
    match_keys = list(match_data.keys())
except FileNotFoundError:
    st.error(f"JSON file for {format_selected} not found. Please ensure the file path is correct.")

try:
    fantasy_points = load_player_fantasy_points(fantasy_points_path)
except FileNotFoundError:
    st.error(f"Fantasy points JSON file for {format_selected} not found.")
    st.stop()

try:
    aggregate_stats = load_sample_players(aggregate_stats_path)
except FileNotFoundError:
    st.error(f"Aggregate stats JSON file for {format_selected} not found.")
    st.stop()

player_data = []
if upload_sample:
    try:
        teams = load_sample_players("sample_players.json")
        for team_idx, team in enumerate(teams.values()):
            for player in team['players']:
                player['team'] = team_idx
                player_data.append(player)
        st.success("Sample players loaded successfully!")
    except FileNotFoundError:
        st.error("Sample file not found.")
elif manual_input:
    st.write("Enter details for each player:")
    for i in range(22):
        col1, col2, col3 = st.columns(3)
        with col1:
            name = st.text_input(f"Player {i+1} Name:", key=f"name_{i}")
        with col2:
            role = st.selectbox(
                f"Player {i+1} Role:",
                ['Batter', 'Bowler', 'All-Rounder', 'Wicket-Keeper'],
                key=f"role_{i}"
            )
        with col3:
            score = st.number_input(
                f"Player {i+1} Fantasy Score:",
                min_value=0,
                step=1,
                key=f"score_{i}"
            )
        if name:
            player_data.append({"name": name, "role": role, "score": score})
    best_team_button()

if squad_info:
    if 'assigned_weights_df' not in st.session_state:
        st.session_state['assigned_weights_df'] = None
    if 'stats_df' not in st.session_state:
        st.session_state['stats_df'] = None

    selected_match = st.selectbox("Select a Match", match_keys)

    if selected_match:
        squads = match_data[selected_match]
        st.subheader("Squads for the Match")

        player_info = {}
        # Create two columns for side by side display
        col1, col2 = st.columns(2)
        
        # Iterate through teams using enumeration
        for i, (team_name, players) in enumerate(squads.items()):
            player_info[team_name] = []
            # Use col1 for first team, col2 for second team
            with (col1 if i == 0 else col2):
                with st.expander(team_name, expanded=True):
                    st.write("Players:")
                    for player in players:
                        st.markdown(f"- **{player}**")
                        player_info[team_name].append(f"{player} : {team_name}")

if assess_players:
    optim_fantasy_points = get_optim_file(fantasy_points_path)
    
    if 'selected_player' not in st.session_state:
        st.session_state.selected_player = None

    all_players = [player.split(":")[0].strip() for team in player_info.values() for player in team]
    all_players = list(set(all_players))

    selected_player = st.selectbox("Select a Player", sorted(all_players), key="player_select")
    st.session_state.selected_player = selected_player

    num_matches_assess = st.slider(
        "Number of past matches to consider",
        min_value=1,
        max_value=500,
        value=100,
        step=1,
        key='num_matches_assess'
    )

    if selected_player:
        player_name = selected_player.split(":")[0].strip()
        date_of_match = extract_date_from_match_key(selected_match)
        if date_of_match is None:
            st.error(f"Could not extract date from match key: {selected_match}")
        else:
            player_data = fantasy_points.get(player_name)
            if player_data is None:
                st.error(f"Player data not found for {player_name}.")
            else:
                keys = ['total_points', 'batting_points', 'bowling_points', 'fielding_points']
                data = {}
                for key in keys:
                    matches, points = get_past_match_performance(
                        player_name,
                        fantasy_points,
                        num_matches=num_matches_assess,
                        key=key,
                        date_of_match=date_of_match
                    )
                    data[key] = (matches, points)
                if any(data[key][0] and data[key][1] for key in keys):
                    df_list = []
                    for key in keys:
                        matches, points = data[key]
                        df_temp = pd.DataFrame({
                            'match': matches,
                            'points': points,
                            'point_type': key
                        })
                        df_list.append(df_temp)
                    df_combined = pd.concat(df_list)
                    
                    import plotly.express as px
                    fig = px.bar(
                        df_combined,
                        x='match',
                        y='points',
                        color='point_type',
                        barmode='group',
                        title=f"Points for {selected_player} in Past Matches"
                    )
                    fig.update_layout(
                        xaxis_title="Matches",
                        yaxis_title="Points",
                        template="plotly_white",
                        xaxis_tickangle=-45
                    )
                    st.plotly_chart(fig)
                else:
                    st.error(f"No data available for {player_name} before {date_of_match}.")

if optimize_team_option:
    all_players = [player.split(":")[0].strip() for team in player_info.values() for player in team]
    all_players = list(set(all_players))

    # Initialize session state variables if they don't exist
    if 'solver' not in st.session_state:
        st.session_state.solver = 'cvpxy'
    if 'risk_tolerance' not in st.session_state:
        st.session_state.risk_tolerance = 1.0
    if 'num_matches' not in st.session_state:
        st.session_state.num_matches = 50
    if 'optimization_done' not in st.session_state:
        st.session_state.optimization_done = False

    # UI Elements
    risk_tolerance = st.slider("Set Risk Tolerance", 
                             min_value=0.01, 
                             max_value=10.0, 
                             value=st.session_state.risk_tolerance, 
                             step=0.01,
                             key='risk_tolerance_slider')
    
    num_matches = st.slider("Number of past matches to consider", 
                           min_value=20, 
                           max_value=500, 
                           value=st.session_state.num_matches, 
                           step=1,
                           key='num_matches_slider')

    # Solver selection before optimization
    solver = st.selectbox("Select Solver", 
                         ['cvpxy', 'pulp'], 
                         key='solver_select')
    
    date_of_match = extract_date_from_match_key(selected_match)
    if date_of_match is None:
        st.error(f"Could not extract date from match key: {selected_match}")
        date_of_match = None

    if st.button("Optimize Team"):
        st.session_state.optimization_done = True
        st.session_state.solver = solver
        st.session_state.risk_tolerance = risk_tolerance
        st.session_state.num_matches = num_matches

        stats_df = compute_player_stats(
            optim_fantasy_points,
            list(all_players),
            num_matches=num_matches,
            date_of_match=date_of_match
        )

        if stats_df.empty:
            st.error("No player statistics available.")
        else:
            cov_matrix = compute_covariance_matrix(
                optim_fantasy_points,
                stats_df['player'].tolist(),
                num_matches=num_matches,
                date_of_match=date_of_match
            )
            player_team_mapping = {}
            for team_name, players in player_info.items():
                for player in players:
                    player_name = player.split(" : ")[0].strip()
                    player_team_mapping[player_name] = team_name

            stats_df['team'] = stats_df['player'].map(player_team_mapping)

            optimizer = optimize_team_sharpe if solver == 'cvpxy' else optimize_team_advanced

            selected_players, weights_df = optimizer(
                stats_df, cov_matrix, risk_aversion=risk_tolerance, boolean=True
            )
            
            # st.write(stats_df)


            if weights_df is not None and not weights_df.empty:
                st.session_state.assigned_weights_df = weights_df
                st.session_state.stats_df = stats_df
                st.success("Optimization successful!")

                total_expected_score = (weights_df['weight'] * stats_df['mean_points']).sum()
                st.write(f"**Total Expected Score of the Selected Team:** {total_expected_score:.2f}")
                st.write("Processing your team selection...")

                # Display results
                weights_df_display = weights_df.merge(
                    stats_df[['player', 'mean_points', 'variance']],
                    on='player',
                    how='left'
                )
                

                match_points = {}
                for player in all_players:
                    player_matches = optim_fantasy_points.get(player, {})
                    match_points[player] = player_matches.get(selected_match, {}).get('total_points', 0)

                # Display results
                weights_df_display = weights_df.merge(
                    stats_df[['player', 'mean_points', 'variance']],
                    on='player',
                    how='left'
                )

                # Add match fantasy points and standard deviation columns
                weights_df_display['match_fantasy_points'] = weights_df_display['player'].map(match_points)
                weights_df_display['std'] = np.sqrt(weights_df_display['variance'])
                total_expected_score = (weights_df_display['weight'] * weights_df_display['mean_points']).sum()
                total_actual_points = weights_df_display['match_fantasy_points'].sum()

                # Calculate team standard deviation (using portfolio variance formula)
                # We need to consider the covariance matrix for proper portfolio std calculation
                total_expected_score = (weights_df_display['weight'] * weights_df_display['mean_points']).sum()
                total_actual_points = (weights_df_display['match_fantasy_points'] *weights_df_display['weight']).sum()

                # Get top 11 players by actual points
                top_11_by_actual = pd.DataFrame({
                    'player': all_players,
                    'actual_points': [optim_fantasy_points.get(player, {}).get(selected_match, {}).get('total_points', 0) 
                                    for player in all_players]
                }).nlargest(11, 'actual_points')

                top_11_total = top_11_by_actual['actual_points'].sum()

                # Calculate team standard deviation
                team_variance = 0
                for i, row1 in weights_df_display.iterrows():
                    for j, row2 in weights_df_display.iterrows():
                        team_variance += row1['weight'] * row2['weight'] * cov_matrix.loc[row1['player'], row2['player']]
                team_std = np.sqrt(team_variance)

                # Create metrics display
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric(
                        label="(Predicted) Score",
                        value=f"{total_expected_score:.2f}",
                        delta=f"{total_expected_score - total_actual_points:.2f}"
                    )

                with col2:
                    st.metric(
                        label="(Predicted) Std",
                        value=f"{team_std:.2f}"
                    )

                with col3:
                    st.metric(
                        label="Actual Points",
                        value=f"{total_actual_points:.2f}"
                    )

                with col4:
                    st.metric(
                        label="Optimal Team Score (Top-11)",
                        value=f"{top_11_total:.2f}",
                        delta=f"{total_actual_points - top_11_total:.2f}"
                    )

                # Add an expander to show the top 11 players
                with st.expander("View Top 11 Players by Actual Points"):
                    st.dataframe(top_11_by_actual)

                st.success("Optimal Weights assigned:")
                st.write(weights_df_display)
                score_dist_fig = plot_team_distribution(
                mu=total_expected_score,
                sigma=team_std,
                actual_score=total_actual_points,
                optimal_score=top_11_total
            )

                st.plotly_chart(score_dist_fig, use_container_width=False)
                with st.expander("View Optimization Method"):
                    st.markdown("""
                                $$
                                \\begin{align*}
                                & \\text{maximize} && \\sum_{i=1}^{n} \\mu_i x_i \\\\
                                & \\text{subject to:} && \\\\
                                & \\text{1. Team Size} && \\sum_{i=1}^{n} x_i = 11 \\\\
                                & \\text{2. Consistency} && \\sum_{i=1}^{n} \\frac{\\mu_i}{\\sigma_i} x_i \\geq \\frac{11}{2} \\cdot \\mathbb{E}[\\frac{\\mu}{\\sigma}] \\\\
                                & \\text{3. Diversity} && \\sum_{i=1}^{n} H(\\frac{\\mu_i}{\\sum_j \\mu_j}) x_i \\geq \\frac{11}{2} H(\\mathbf{\\mu}) \\\\
                                & \\text{4. Form} && \\sum_{i: \\mu_i \\geq Q_{75}(\\mu)} x_i \\geq \\frac{11}{3} \\\\
                                & \\text{5. Team Coverage} && \\sum_{i \\in T_k} x_i \\geq 1 \\quad \\forall k \\in \\text{Teams} \\\\
                                & \\text{where:} && x_i \\in \\{0,1\\} \\text{ for all } i \\\\
                                &&& T_k \\text{ is the set of players from team } k
                                \\end{align*}
                                $$

                                **Optimization Breakdown:**

                                **Objective Function:**
                                - Maximizes total expected fantasy points
                                - $\\mu_i$ represents average points for player i
                                - $x_i$ is binary (1 if player selected, 0 if not)

                                **Constraints Explained:**

                                1. **Team Size (Basic Rule)**
                                - Ensures exactly 11 players are selected
                                - Required for valid team formation

                                2. **Consistency (Risk Management)**
                                - Uses Sharpe ratio ($\\frac{\\mu_i}{\\sigma_i}$)
                                - Favors consistent performers over volatile ones
                                - Must exceed average team consistency

                                3. **Diversity (Point Distribution)**
                                - Uses entropy to measure scoring distribution
                                - Prevents overreliance on few players
                                - Ensures balanced point contribution

                                4. **Form (Recent Performance)**
                                - At least 1/3 of team from top 75% performers
                                - Captures players in good current form
                                - Balances historical data with recent performance

                                5. **Team Coverage (Balance)**
                                - Minimum one player from each team

                                **Decision Variables:**
                                - $x_i$ is binary (0 or 1)
                                - Represents player selection/non-selection
                                - One variable per available player
                                """)

                # Create visualization
                weights_df_display = weights_df_display.sort_values(by='weight', ascending=True)
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=weights_df_display['weight'],
                    y=weights_df_display['player'],
                    name='Selection Weight',
                    orientation='h',
                    marker_color='blue'
                ))
                fig.add_trace(go.Bar(
                    x=weights_df_display['mean_points'],
                    y=weights_df_display['player'],
                    name='Expected Score',
                    orientation='h',
                    marker_color='green'
                ))
                fig.add_trace(go.Bar(
                    x=np.sqrt(weights_df_display['variance']),
                    y=weights_df_display['player'],
                    name='Standard Deviation',
                    orientation='h',
                    marker_color='red'
                ))
                fig.update_layout(
                    title="Player Selection Weights, Expected Scores, and Standard Deviations",
                    xaxis_title="Value",
                    yaxis_title="Player",
                    barmode='group',
                    template="plotly_white",
                    height=600
                )
                st.plotly_chart(fig)
            else:
                st.error("Failed to select an optimal team.")

    # Allow solver change after optimization
    # if st.session_state.optimization_done:
    #     if st.button("Re-run Optimization with New Solver"):
    #         st.experimental_rerun()
    
    if st.button("Get Optimal Team"):
        if len(player_info) < 1:
            st.error("Please ensure data for at least 22 players is provided.")
        else:
            player_input = []
            for team_name, players in player_info.items():
                for player in players:
                    player_name = player.split(" : ")[0]
                    stats = aggregate_stats.get(player_name, {})
                    if stats:
                        stats_info = (
                            f"{player_name} (Team: {team_name}) - "
                            f"Games: {stats.get('Games', 0)}, "
                            f"Wins: {stats.get('Won', 0)}, "
                            f"Win %: {stats.get('Win %', 0)}, "
                            f"Runs: {stats.get('Runs', 0)}, "
                            f"Fours: {stats.get('Fours', 0)}"
                        )
                    else:
                        stats_info = f"{player_name} (Team: {team_name}) - No statistics available"
                    player_input.append(stats_info)

            player_input_str = "\n".join(player_input)

            if ('assigned_weights_df' in st.session_state and 
                st.session_state['assigned_weights_df'] is not None):
                assigned_weights_df = st.session_state['assigned_weights_df']
                weights_info = []
                for index, row in assigned_weights_df.iterrows():
                    weights_info.append(f"{row['player']} - Selection Weight: {row['weight']}")
                weights_info_str = "\n".join(weights_info)
                player_input_str += "\n\nPlayer Weights:\n" + weights_info_str
            else:
                st.warning("Weights data not found. Proceeding without weights information.")

            st.write("Processing your team selection...")
            raw_response = get_optimal_team_llm(player_input_str)

            if raw_response:
                st.success("Optimal Team Generated Successfully!")
                st.subheader("Optimal Team")
                st.text(raw_response)
            else:
                st.error("Error generating the optimal team.")

            

st.markdown("---")
st.caption("Powered by OpenAI")
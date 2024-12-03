import streamlit as st
import openai
import json
import os
from dotenv import load_dotenv
import plotly.graph_objects as go
import re
import plotly.express as px
from stqdm import stqdm
from llm_inference import analyze_team_selection
from heuristic_solver import (
    load_player_fantasy_points_for_optimization,
    compute_player_stats,
    compute_covariance_matrix,
    optimize_team_sharpe,
    optimize_team_advanced,
    optimize_team_advanced_test
)
import datetime
from utils import get_past_match_performance, extract_date_from_match_key, plot_team_distribution, calculate_team_metrics
from get_snapshot import get_team_selection_snapshot
import pandas as pd
import numpy as np
import scipy.stats as stats


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

def filter_match_keys(match_keys, format_selected):
    filtered_keys = []
    for match in match_keys:
        # Extract the format from match key
        if format_selected == 'T20' and match.endswith('T20'):
            filtered_keys.append(match)
        elif format_selected == 'ODI' and (match.endswith('ODI') or match.endswith('ODM')):
            filtered_keys.append(match)
        elif format_selected == 'Test' and (match.endswith('Test') or match.endswith('MDM')):
            filtered_keys.append(match)
    return filtered_keys

st.title("Dream11-Fantasy Cricket Team Model Analytics")
st.markdown("""
    - Load data from scheduled matches or manually input details.
    - Evaluate the generated the best team of 11 players using AI.
""")

st.sidebar.image("logo-model-ui.png")
st.sidebar.header("OPTIONS")
format_selected = st.sidebar.selectbox("Select Format", ['T20', 'ODI', 'Test'])
# upload_sample = st.sidebar.checkbox("Load Sample Players from JSON")
# manual_input = st.sidebar.checkbox("Add Players Manually")
squad_info = st.sidebar.checkbox("Load squads from scheduled matches")
get_team_snapshot = st.sidebar.checkbox("Get Selection CSV")
# assess_players = st.sidebar.checkbox("Assess Players from the squads")
# optimize_team_option = st.sidebar.checkbox("Optimize Team Selection")
with st.sidebar.expander("📊 Optimization Framework", expanded=True):
    st.markdown("""                
    **PuLP Optimizer**
    $$
    \\begin{align*}
    & \\text{maximize} && \\sum_{i=1}^{n} \\mu_i x_i - \\lambda \\sum_{i=1}^{n} \\sigma_i x_i \\\\
    & \\text{subject to:} && \\\\
    & \\text{1. Team Size} && \\sum_{i=1}^{n} x_i = 11 \\\\
    & \\text{2. Consistency} && \\sum_{i=1}^{n} \\frac{\\mu_i}{\\sigma_i} x_i \\geq \\alpha_1 \\cdot \\mathbb{E}[\\frac{\\mu}{\\sigma}] \\\\
    & \\text{3. Diversity} && \\sum_{i=1}^{n} H(\\frac{\\mu_i}{\\sum_j \\mu_j}) x_i \\geq \\alpha_2 \\cdot H(\\mathbf{\\mu}) \\\\
    & \\text{4. Form} && \\sum_{i: \\mu_i \\geq Q_{q}(\\mu)} x_i \\geq \\alpha_3 \\cdot 11 \\\\
    & \\text{5. Team Coverage} && \\sum_{i \\in T_k} x_i \\geq 1 \\quad \\forall k \\in \\text{Teams} \\\\
    & \\text{where:} && x_i \\in \\{0,1\\} \\text{ for all } i \\\\
    &&& T_k \\text{ players from team } k \\\\
    &&& \\lambda \\text{ is the risk aversion factor} \\\\
    &&& \\alpha_1 \\text{ is the consistency threshold} \\\\
    &&& \\alpha_2 \\text{ is the diversity threshold} \\\\
    &&& \\alpha_3 \\text{ is the form threshold} \\\\
    &&& q \\text{ is the form quantile threshold}
    \\end{align*}
    $$
    """)

# Add Technical Guidelines in Sidebar
with st.sidebar.expander("🎯 Technical Guidelines", expanded=True):
    st.markdown("""
    ### Key Parameters
    
    **1. Risk Aversion (λ)**
    $$\\lambda \\in [0.01, 0.3], \\text{ default} = 0.1$$
    - Balances expected points vs. risk
    - Higher λ: Lesser deviation in performance ratio
    
    **2. Historical Window**
    $$M_{matches} \\in [20, 500], \\text{ default} = 65$$
    - Number of past matches to analyze
    - Affects statistical estimations
    
    **3. Consistency Threshold**
    $$\\alpha_c \\in [0.1, 1.0], \\text{ default} = 0.5$$
    - Minimum required Sharpe ratio
    - Controls reliability of selections
    
    **4. Diversity Threshold**
    $$\\alpha_d \\in [0.1, 1.0], \\text{ default} = 0.5$$
    - Enforces point distribution entropy
    - Prevents over-reliance on few players
    
    **5. Form Threshold**
    $$\\alpha_f \\in [0.1, 1.0], \\text{ default} = 0.333$$
    - Proportion of in-form players
    - Based on form quantile cutoff
    
    **6. Form Quantile (q)**
    $$q \\in [40, 90], \\text{ default} = 40$$
    - Percentile cutoff for form consideration
    - Higher q: More selective on recent performance
    
    **7. Team Coverage**
    - Minimum one player per team
    - Ensures balanced representation
    """)

format_lower = format_selected.lower().replace('-', '').replace(' ', '')
fantasy_points_path = f"../data/processed/player_fantasy_points_{format_lower}.json"
json_file_path = f"../data/processed/combined_squad.json"
aggregate_stats_path = f"../data/processed/aggregate_cricket_stats_{format_lower}.json"

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

# try:
#     aggregate_stats = load_sample_players(aggregate_stats_path)
# except FileNotFoundError:
#     st.error(f"Aggregate stats JSON file for {format_selected} not found.")
#     st.stop()



# Cache the main computation function using st.cache_data

@st.cache_data(ttl=3600)
def format_display_dataframe(df):
    """Cache the display formatting of the dataframe"""
    if df is None or df.empty:
        return None
    display_df = df.copy()
    numeric_cols = ['optimal_score', 'predicted_std', 'actual_score']
    for col in numeric_cols:
        display_df[col] = display_df[col].round(2)
    return display_df

@st.cache_data(ttl=3600)
def create_performance_plots(df):
    """Create both line plot and distribution plot for performance analysis"""
    if df is None or df.empty:
        return None, None
    # Create distribution plot for performance ratio
    dist_fig = go.Figure()
    dist_fig.add_trace(go.Histogram(
        x=df['performance_ratio'],
        nbinsx=100,
        name='Distribution',
        histnorm='probability'
    ))
    
    # Add KDE plot
    # kde_points = np.linspace(df['performance_ratio'].min(), df['performance_ratio'].max(), 100)
    # kde = stats.gaussian_kde(df['performance_ratio'].dropna())
    # kde_values = kde(kde_points)
    
    # dist_fig.add_trace(go.Scatter(
    #     x=kde_points,
    #     y=kde_values,
    #     mode='lines',
    #     name='KDE',
    #     line=dict(color='red')
    # ))
    
    # Add mean and median lines
    mean_ratio = df['performance_ratio'].mean()
    median_ratio = df['performance_ratio'].median()
    
    dist_fig.add_vline(
        x=mean_ratio,
        line_dash="dash",
        line_color="green",
        annotation_text=f"Mean: {mean_ratio:.2f}",
        annotation_position="top"
    )
    
    dist_fig.add_vline(
        x=median_ratio,
        line_dash="dash",
        line_color="blue",
        annotation_text=f"Median: {median_ratio:.2f}",
        annotation_position="bottom"
    )
    
    dist_fig.update_layout(
        title="Distribution of Performance Ratio (Actual/Optimal Score)",
        xaxis_title="Performance Ratio",
        yaxis_title="Density",
        template="plotly_white",
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99
        ),
        annotations=[
            dict(
                x=0.01,
                y=0.95,
                xref="paper",
                yref="paper",
                text=f"Standard Deviation: {df['performance_ratio'].std():.3f}",
                showarrow=False
            )
        ]
    )
    
    return None, dist_fig

if get_team_snapshot:
    st.markdown("## TEAM SELECTION SNAPSHOT")
    
    # Initialize session state
    if 'snapshot_df' not in st.session_state:
        st.session_state.snapshot_df = None
    if 'last_date_filter' not in st.session_state:
        st.session_state.last_date_filter = None
    if 'analysis_generated' not in st.session_state:
        st.session_state.analysis_generated = False
    
    # Set default date to July 6th, 2024
    default_date = datetime.date(2020, 7, 1)
    date_filter = default_date
    
    st.write("Analysis will include matches from July 6th, 2024 onward")

    # Add a button to trigger the analysis
    if st.button("Generate Team Selection Analysis", key="generate_analysis") or st.session_state.analysis_generated:
        st.session_state.analysis_generated = True
        all_paths = [f"../data/processed/player_fantasy_points_{format_lower}.json" for format_lower in ["t20", "odi", "test"]]
        
        # Show loading message while processing
        if date_filter != st.session_state.last_date_filter:
            with st.spinner('Analyzing team selections... This may take a few moments.'):
                st.session_state.snapshot_df = get_team_selection_snapshot(
                    match_keys,
                    match_data,
                    fantasy_points,
                    get_optim_file(all_paths[0]),
                    get_optim_file(all_paths[1]),
                    get_optim_file(all_paths[2]),
                    input_date=date_filter,
                    quantile_form=40,
                    num_matches=65
                )
                st.session_state.last_date_filter = date_filter

        snapshot_df = st.session_state.snapshot_df

        if snapshot_df is not None and not snapshot_df.empty:
            st.success(f"Generated snapshot for {len(snapshot_df)} matches")
            
            # Display snapshot with formatted columns
            display_df = format_display_dataframe(snapshot_df)
            st.dataframe(display_df)
            
            # Calculate metrics
            map_actual_optimal = np.mean(np.abs(snapshot_df['actual_score'] - snapshot_df['optimal_score']))
            mape_actual_optimal = np.mean(np.abs((snapshot_df['actual_score'] - snapshot_df['optimal_score']) / snapshot_df['optimal_score'])) * 100
            map_actual_predicted = np.mean(np.abs(snapshot_df['actual_score'] - snapshot_df['predicted_score']))
            mape_actual_predicted = np.mean(np.abs((snapshot_df['actual_score'] - snapshot_df['predicted_score']) / snapshot_df['predicted_score'])) * 100

            # Display metrics in columns
            st.markdown("### Performance Metrics")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "MAP (Actual vs Optimal)",
                    f"{map_actual_optimal:.2f}",
                    help="Mean Absolute Performance difference between Actual and Optimal points"
                )
            
            with col2:
                st.metric(
                    "MAPE (Actual vs Optimal)",
                    f"{mape_actual_optimal:.2f}%",
                    help="Mean Absolute Percentage Error between Actual and Optimal points"
                )
            
            with col3:
                st.metric(
                    "MAP (Actual vs Predicted)",
                    f"{map_actual_predicted:.2f}",
                    help="Mean Absolute Performance difference between Actual and Predicted points"
                )
            
            with col4:
                st.metric(
                    "MAPE (Actual vs Predicted)",
                    f"{mape_actual_predicted:.2f}%",
                    help="Mean Absolute Percentage Error between Actual and Predicted points"
                )

            # Download button
            csv = snapshot_df.to_csv(index=False)
            st.download_button(
                "Download CSV",
                csv,
                "team_selections.csv",
                "text/csv",
                key='download-csv'
            )
            # Visualization section
            show_viz = st.checkbox("Show Performance Visualizations", key='show_viz')
            if show_viz:
                with st.spinner('Generating performance visualizations...'):
                    trend_fig, dist_fig = create_performance_plots(snapshot_df)
                    
                    if dist_fig:
                        st.plotly_chart(dist_fig)
                        
                        # First row of metrics - Summary statistics
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric(
                                "Mean Performance",
                                f"{snapshot_df['performance_ratio'].mean():.2%}"
                            )
                        with col2:
                            st.metric(
                                "Median Performance",
                                f"{snapshot_df['performance_ratio'].median():.2%}"
                            )
                        with col3:
                            st.metric(
                                "Best Performance",
                                f"{snapshot_df['performance_ratio'].max():.2%}"
                            )
                        with col4:
                            st.metric(
                                "Worst Performance",
                                f"{snapshot_df['performance_ratio'].min():.2%}"
                            )
                        
                        # Second row of metrics - Quantile analysis
                        st.markdown("### Quantile Analysis")
                        col5, col6, col7, col8 = st.columns(4)
                        with col5:
                            st.metric(
                                "25th Percentile",
                                f"{snapshot_df['performance_ratio'].quantile(0.25):.2%}",
                                help="Bottom 25% of performances were below this value"
                            )
                        with col6:
                            st.metric(
                                "50th Percentile",
                                f"{snapshot_df['performance_ratio'].quantile(0.5):.2%}",
                                help="50% of performances were below this value"
                            )
                        with col7:
                            st.metric(
                                "75th Percentile",
                                f"{snapshot_df['performance_ratio'].quantile(0.75):.2%}",
                                help="75% of performances were below this value"
                            )
                        with col8:
                            st.metric(
                                "100th Percentile",
                                f"{snapshot_df['performance_ratio'].quantile(1.0):.2%}",
                                help="Maximum performance value"
                            )
                            
        else:
            st.warning("No matches found after the specified date.")


if squad_info:
    if 'assigned_weights_df' not in st.session_state:
        st.session_state['assigned_weights_df'] = None
    if 'stats_df' not in st.session_state:
        st.session_state['stats_df'] = None

    filtered_match_keys = filter_match_keys(match_keys, format_selected)

    # Use filtered keys in selectbox
    if filtered_match_keys:
        selected_match = st.selectbox("Select a Match", filtered_match_keys)
    else:
        st.warning(f"No matches found for format: {format_selected}")

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
                with st.expander(team_name, expanded=False):
                    st.write("Players:")
                    for player in players:
                        st.markdown(f"- **{player}**")
                        player_info[team_name].append(f"{player} : {team_name}")

# if assess_players:
    st.markdown("## ASSESS PLAYERS")

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
        value=65,
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
                
                # First get the matches and points for total_points to establish base matches
                base_matches, base_points = get_past_match_performance(
                    player_name,
                    fantasy_points,
                    num_matches=num_matches_assess,
                    key='total_points',
                    date_of_match=date_of_match
                )
                data['total_points'] = (base_matches, base_points)
                
                # Use the same match sequence for other metrics
                unique_matches = []
                seen = set()
                for match in base_matches:
                    if match not in seen:
                        seen.add(match)
                        unique_matches.append(match)
                
                # Get points for other metrics using the same match sequence
                for key in keys[1:]:  # Skip total_points as we already have it
                    matches, points = get_past_match_performance(
                        player_name,
                        fantasy_points,
                        num_matches=len(unique_matches),  # Use length of unique matches
                        key=key,
                        date_of_match=date_of_match
                    )
                    
                    # Ensure we use the same match sequence
                    aligned_points = []
                    for match in unique_matches:
                        try:
                            idx = matches.index(match)
                            aligned_points.append(points[idx])
                        except ValueError:
                            aligned_points.append(0)  # Use 0 if match not found
                    
                    data[key] = (unique_matches, aligned_points)

            if any(data[key][0] and data[key][1] for key in keys):
                df_list = []
                for key in keys:
                    matches, points = data[key]
                    df_temp = pd.DataFrame({
                        'match': matches,
                        key: points
                    })
                    df_list.append(df_temp)
                
                # Merge all dataframes on the match column
                df_combined = df_list[0]  # Start with total_points
                for df in df_list[1:]:    # Merge the rest one by one
                    df_combined = df_combined.merge(df, on='match', how='outer')
                
                # Reorder columns to put total_points at the end
                columns_order = ['match', 'batting_points', 'bowling_points', 'fielding_points', 'total_points']
                df_combined = df_combined[columns_order]
                
                st.markdown(f"### Past scores for {selected_player}")
                st.write(df_combined)
                    
            else:
                st.error(f"No data available for {player_name} before {date_of_match}.")
                
# if optimize_team_option:
    st.markdown("## SOLVER AND OPTIMIZER CONFIG")
    all_players = [player.split(":")[0].strip() for team in player_info.values() for player in team]
    all_players = list(set(all_players))
    # st.write(all_players)

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
    # risk_tolerance = st.slider("Set Risk Tolerance- (For CVPXY only)", 
    #                          min_value=0.01, 
    #                          max_value=10.0, 
    #                          value=st.session_state.risk_tolerance, 
    #                          step=0.01,
    #                          key='risk_tolerance_slider')
    
    num_matches = st.slider("Number of past matches to consider", 
                       min_value=20, 
                       max_value=500, 
                       value=65, 
                       step=1,
                       key='num_matches_slider')

# Add sliders for optimizer parameters
    st.markdown("### Optimizer Parameters")
    col1, col2 = st.columns(2)

    with col1:
        risk_aversion = st.slider(
            "Risk Aversion",
            min_value=0.01,
            max_value=0.3,
            value=0.1,
            step=0.01,
            help="Controls the trade-off between expected returns and risk",
            key='risk_aversion_slider'
        )

        form_threshold = st.slider(
            "Form Threshold",
            min_value=0.1,
            max_value=1.0,
            value=0.5,
            step=0.1,
            help="Minimum threshold for recent performance consideration",
            key='form_threshold_slider'
        )

    with col2:
        diversity_threshold = st.slider(
            "Diversity Threshold",
            min_value=0.1,
            max_value=1.0,
            value=0.3,
            step=0.1,
            help="Threshold for team composition diversity",
            key='diversity_threshold_slider'
        )

        quantile_form = st.slider(
            "Form Quantile",
            min_value=50,
            max_value=90,
            value=40,
            step=5,
            help="Percentile threshold for considering player form",
            key='quantile_form_slider'
        )

    # Solver selection before optimization
    solver = 'pulp'

    date_of_match = extract_date_from_match_key(selected_match)
    if date_of_match is None:
        st.error(f"Could not extract date from match key: {selected_match}")
        date_of_match = None

    if st.button("Optimize Team"):
        st.session_state.optimization_done = True
        st.session_state.solver = solver
        st.session_state.risk_tolerance = risk_aversion
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
            # st.write(player_info)
            for team_name, players in player_info.items():
                for player in players:
                    player_name = player.split(" : ")[0].strip()
                    player_team_mapping[player_name] = team_name

            stats_df['team'] = stats_df['player'].map(player_team_mapping)

            # optimizer = optimize_team_sharpe if solver == 'cvpxy' else optimize_team_advanced
            optimizer = optimize_team_sharpe if solver == 'cvpxy' else optimize_team_advanced_test

            selected_players, weights_df = optimizer(
                stats_df, 
                cov_matrix, 
                risk_aversion=risk_aversion, 
                boolean=True,
                form_threshold=form_threshold,
                diversity_threshold=diversity_threshold,
                quantile_form=quantile_form
            )
            
            
            team_metrics = calculate_team_metrics(stats_df, weights_df, cov_matrix)

            # Display metrics
            col11, col21, col31, col41 = st.columns(4)

            with col11:
                st.metric(
                    label="Expected Points",
                    value=f"{team_metrics['trend_score']:.1f}",
                    help="Total expected points for the selected team"
                )

            with col21:
                st.metric(
                    label="Consistency",
                    value=f"{team_metrics['consistency_score']:.2f}",
                    # delta=f"{(team_metrics['consistency_score'] - 1) * 100:.1f}%",
                    help="Ratio of team's Sharpe ratio sum to required threshold. Should be ≥ 1"
                )

            with col31:
                st.metric(
                    label="Diversity",
                    value=f"{team_metrics['diversity_score']:.2f}",
                    # delta=f"{(team_metrics['diversity_score'] - 1) * 100:.1f}%",
                    help="Ratio of team's point distribution entropy to required threshold. Should be ≥ 1"
                )

            with col41:
                st.metric(
                    label="Form",
                    value=f"{team_metrics['form_score']:.2f}",
                    # delta=f"{(team_metrics['form_score'] - 1) * 100:.1f}%",
                    help="Ratio of top performers count to required minimum (11/3). Should be ≥ 1"
                )


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
# st.write(stats_df)

                with col1:
                    st.metric(
                        label="(Predicted) Score",
                        value=f"{total_expected_score:.2f}",
                        delta=f"{total_expected_score - total_actual_points:.2f}"
                    )

                with col2:
                    performance_ratio = total_actual_points / top_11_total
                    st.metric(
                        label="Performance Ratio",
                        value=f"{performance_ratio:.2f}",
                        delta=f"{(performance_ratio - 1) * 100:.1f}%" if performance_ratio != 1 else None
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
                with st.expander("Compare Selected vs Actual Top Players", expanded=True):
                    # Create two columns
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("Top 11 by Actual Points")
                        st.dataframe(
                            top_11_by_actual.style.format({
                                'actual_points': '{:.2f}'
                            })
                        )
                    
                    with col2:
                        st.subheader("Model Selected Players")
                        # Get selected players (where weight = 1)
                        selected_players_df = weights_df_display[weights_df_display['weight'] == 1][
                            ['player', 'match_fantasy_points']
                        ].rename(columns={'match_fantasy_points': 'actual_points'})
                        
                        # Sort by actual points for better comparison
                        selected_players_df = selected_players_df.sort_values(
                            by='actual_points', 
                            ascending=False
                        )
                        
                        st.dataframe(
                            selected_players_df.style.format({
                                'actual_points': '{:.2f}'
                            })
                        )

                st.success("Optimal Weights assigned:")
                st.write(weights_df_display)
                score_dist_fig = plot_team_distribution(
                mu=total_expected_score,
                sigma=team_std,
                actual_score=total_actual_points,
                optimal_score=top_11_total
            )

                st.plotly_chart(score_dist_fig, use_container_width=False)
               
            else:
                st.error("Failed to select an optimal team.")


    # if st.button("Get Team Analytics"):
    #     if ('stats_df' not in st.session_state) or ('assigned_weights_df' not in st.session_state):
    #         st.error("Please run team optimization first!")
    #     elif st.session_state.stats_df is None or st.session_state.assigned_weights_df is None:
    #         st.error("No optimization data found. Please run team optimization first!")
    #     else:
    #         try:
    #             weights_df = st.session_state.assigned_weights_df
    #             if weights_df.empty:
    #                 st.error("No player weights found. Please run optimization again.")
                    
    #             selected_players = weights_df[weights_df['weight'] == 1]['player'].tolist()
    #             if not selected_players:
    #                 st.error("No players were selected in the optimization.")
                    
                    
    #             stats_df = st.session_state.stats_df
    #             if stats_df.empty:
    #                 st.error("No player statistics found. Please run optimization again.")
                    
                    
    #             st.write("### Team Analysis Report")
    #             with st.spinner("Generating comprehensive team analysis using AI..."):
    #                 format_type = st.session_state.get('format_type', 'odi').lower() 
    #                 analysis = analyze_team_selection(
    #                     stats_df=stats_df,
    #                     selected_players=selected_players,
    #                     format_lower=format_type
    #                 )
    #                 if analysis:
    #                     st.markdown("## Analysis Results")
    #                     st.write(analysis)
    #                 else:
    #                     st.warning("No analysis was generated. Please check the data and try again.")
    #         except Exception as e:
    #             st.error(f"An error occurred during analysis: {str(e)}")
    #             st.error("Please check the data and try again.")

    st.markdown("---")
    st.caption("Team-62")
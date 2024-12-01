import streamlit as st
import openai
import json
import os
from dotenv import load_dotenv
import plotly.graph_objects as go
import datetime
import re
import numpy as np
import scipy.stats as stats

# from heuristic_solver import compute_player_stats, compute_covariance_matrix, optimize_team_advanced
import pandas as pd


def extract_date_from_match_key(match_key):
    date_pattern = r"(\d{4}-\d{2}-\d{2})"
    match = re.search(date_pattern, match_key)
    if match:
        return match.group(1)
    else:
        return None


def get_optimal_team_llm(player_data, client):
    """
    Uses GPT-4 to select an optimal fantasy cricket team based on player data.

    Args:
        player_data (str): String containing player information and scores
        client: OpenAI client instance

    Returns:
        str: LLM response containing selected team with player attributes and analysis
    """
    prompt = f"""
    You are an expert fantasy cricket selector. Create the best team of 11 players from the following 22 players based on their expected fantasy scores. Make sure to include at least one player from each team. 

    Players and their scores:
    {player_data}

    Return the team as a list of player names. For each player, output the most important attribute for the player's selection FROM AGGREGATE STATISTICS PROVIDED TO YOU. The only constraint is that at least one player from each team be selected ALSO MAKE SURE YOU GIVE AN OUTPUT WHICH IS READABLE BY A LAYMAN. MENTION AGGREGATE DATA AS WELL ASN THE CONSISTENCY PROVIDED BY THE VARIANCE.
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a fantasy cricket expert. Suggest the best 11 players out of the ones given. Ensure one player from each team is selected.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.9,
    )

    return response.choices[0].message.content


def best_team_button():
    """
    Streamlit UI component for generating the optimal team using LLM.
    Validates input data and displays the generated team.
    """
    if st.button("Generate Best Team LLM"):
        if len(player_data) < 22:
            st.error("Please ensure data for at least 22 players is provided.")
        else:
            player_input = "\n".join(
                [f"{p['name']} ({p['role']}): {p['score']}" for p in player_data]
            )
            st.write("Processing your team selection...")
            raw_response = get_optimal_team_llm(player_input)

            if raw_response:
                st.success("Optimal Team Generated Successfully!")
                st.subheader("Optimal Team")
                st.text(raw_response)
            else:
                st.error("Error generating the optimal team.")


def get_past_match_performance(
    player_name, fantasy_points, num_matches=50, key="total_points", date_of_match=None
):
    """
    Retrieves and processes historical match performance data for a player.
    If fewer matches than requested are available, extends using the last available match's data.

    Args:
        player_name (str): Name of the player
        fantasy_points (dict): Historical fantasy points data
        num_matches (int): Number of past matches to consider
        key (str): Key for points data in match info
        date_of_match (str): Date to filter matches before (YYYY-MM-DD format)

    Returns:
        tuple: Lists of match identifiers and corresponding points.
              If N matches requested but M < N available (M > 0),
              returns M actual matches plus (N-M) copies of the last match.
              If no matches available, returns lists filled with 'No Match' and 0.
    """
    # Get player data
    player_data = fantasy_points.get(player_name)
    if not player_data:
        return ["No Match"] * num_matches, [0] * num_matches

    # Convert to list of matches
    matches_data = (
        list(player_data.items()) if isinstance(player_data, dict) else player_data
    )

    # Filter by date if specified
    if date_of_match:
        try:
            date_of_match_dt = datetime.datetime.strptime(date_of_match, "%Y-%m-%d")
            filtered_player_data = []
            for match_data in matches_data:
                match_key = (
                    match_data[0] if isinstance(match_data, tuple) else match_data
                )
                date_match = re.search(r"\d{4}-\d{2}-\d{2}", str(match_key))
                if date_match:
                    match_date = datetime.datetime.strptime(
                        date_match.group(), "%Y-%m-%d"
                    )
                    if match_date < date_of_match_dt:
                        filtered_player_data.append(match_data)
        except ValueError:
            return ["No Match"] * num_matches, [0] * num_matches
    else:
        filtered_player_data = matches_data

    # Return zeros if no matches available
    if not filtered_player_data:
        return ["No Match"] * num_matches, [0] * num_matches

    # Get the last available matches
    last_matches_data = filtered_player_data[-num_matches:]

    # Process available matches
    last_matches, last_points = [], []
    for match_data in last_matches_data:
        if isinstance(match_data, tuple):
            match_key, match_info = match_data
            last_matches.append(match_key)
            last_points.append(match_info.get(key, 0))
        else:
            last_matches.append(match_data[0])
            last_points.append(match_data[1].get(key, 0))

    # If we have some matches but fewer than requested,
    # extend using the last available match's data
    if last_points and len(last_points) < num_matches:
        # Get the last available match data
        last_match = last_matches[-1]
        last_point = last_points[-1]

        # Extend both lists with copies of the last match
        extension_length = num_matches - len(last_points)
        last_matches.extend([last_match] * extension_length)
        last_points.extend([last_point] * extension_length)

    return last_matches, last_points


def plot_team_distribution(mu, sigma, actual_score, optimal_score):
    """
    Creates a Plotly visualization of team score distribution with key metrics.

    Args:
        mu (float): Mean of the distribution
        sigma (float): Standard deviation of the distribution
        actual_score (float): Actual team score
        optimal_score (float): Optimal team score

    Returns:
        plotly.graph_objects.Figure: Interactive plot of score distribution
    """
    x = np.linspace(mu - 4 * sigma, mu + 4 * sigma, 1000)
    y = stats.norm.pdf(x, mu, sigma)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="lines",
            name="Expected Distribution",
            line=dict(color="blue", width=2),
            fill="tozeroy",
            fillcolor="rgba(0, 0, 255, 0.1)",
        )
    )

    fig.add_vline(
        x=actual_score,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Actual Score: {actual_score:.1f}",
        annotation_position="top right",
        annotation=dict(yshift=10),
    )

    fig.add_vline(
        x=optimal_score,
        line_dash="dash",
        line_color="green",
        annotation_text=f"Optimal Score: {optimal_score:.1f}",
        annotation_position="bottom right",
        annotation=dict(yshift=-10),
    )

    fig.add_vline(
        x=mu,
        line_dash="dot",
        line_color="gray",
        annotation_text=f"Expected Score: {mu:.1f}",
        annotation_position="top left",
        annotation=dict(yshift=20),
    )

    fig.update_layout(
        title="Team Score Distribution",
        xaxis_title="Total Points",
        yaxis_title="Probability Density",
        showlegend=True,
        template="plotly_white",
        height=400,
        margin=dict(t=50, l=50, r=50, b=50),
    )

    return fig


def calculate_team_metrics(stats_df, weights_df, cov_matrix):
    """
    Calculates comprehensive performance metrics for a selected team.

    Args:
        stats_df (pd.DataFrame): Player statistics including mean_points and variance
        weights_df (pd.DataFrame): Selected players with weight=1 for selected
        cov_matrix (np.array): Covariance matrix of player performances

    Returns:
        dict: Dictionary containing:
            - trend_score: Expected total points
            - consistency_score: Average Sharpe ratio
            - diversity_score: Entropy of point distribution
            - form_score: Number of top performers
    """
    try:
        selected_players = weights_df[weights_df["weight"] == 1]["player"].tolist()
        if not selected_players:
            raise ValueError("No players selected in weights_df")

        selected_df = stats_df[stats_df["player"].isin(selected_players)].copy()
        if selected_df.empty:
            raise ValueError("No stats found for selected players")

        trend_score = selected_df["mean_points"].sum()
        consistency_score = (
            selected_df["mean_points"] / np.sqrt(selected_df["variance"])
        ).mean()

        if selected_df["mean_points"].sum() > 0:
            point_shares = selected_df["mean_points"] / selected_df["mean_points"].sum()
            diversity_score = (
                -(np.sum(point_shares * np.log(point_shares + 1e-10))) / 11
            )
        else:
            diversity_score = 0

        points_75th = stats_df["mean_points"].quantile(0.75)
        top_performers = selected_df[selected_df["mean_points"] >= points_75th]
        form_score = len(top_performers)

        return {
            "trend_score": round(trend_score, 2),
            "consistency_score": round(consistency_score, 2),
            "diversity_score": round(diversity_score, 2),
            "form_score": round(form_score, 2),
        }

    except Exception as e:
        print(f"Error calculating team metrics: {str(e)}")
        return {
            "trend_score": 0,
            "consistency_score": 0,
            "diversity_score": 0,
            "form_score": 0,
        }


def load_player_fantasy_points(json_file):
    """
    Loads and sorts player fantasy points data from a JSON file.

    Args:
        json_file (str): Path to JSON file containing player data

    Returns:
        dict: Sorted player fantasy points data
    """
    with open(json_file, "r") as file:
        data = json.load(file)
        sorted_data = {}
        for player, matches in data.items():
            match_list = list(matches.items())
            match_list_sorted = sorted(
                match_list,
                key=lambda x: (
                    datetime.datetime.strptime(
                        re.search(r"(\d{4}-\d{2}-\d{2})", x[0]).group(1), "%Y-%m-%d"
                    )
                    if re.search(r"(\d{4}-\d{2}-\d{2})", x[0])
                    else datetime.datetime.min
                ),
            )
            sorted_data[player] = match_list_sorted
        return sorted_data


# Initialize OpenAI client
load_dotenv()
KEY = os.getenv("OPENAI_KEY")
client = openai.OpenAI(api_key=KEY)

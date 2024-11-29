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




load_dotenv()
KEY = os.getenv('OPENAI_KEY')

# Initialize OpenAI API client
client = openai.OpenAI(api_key=KEY)



def get_optimal_team_llm(player_data, client= client):
    prompt = f"""
    You are an expert fantasy cricket selector. Create the best team of 11 players from the following 22 players based on their expected fantasy scores. Make sure to include at least one player from each team. 

    Players and their scores:
    {player_data}

    Return the team as a list of player names. For each player, output the most important attribute for the player's selection FROM AGGREGATE STATISTICS PROVIDED TO YOU. The only constraint is that at least one player from each team be selected ALSO MAKE SURE YOU GIVE AN OUTPUT WHICH IS READABLE BY A LAYMAN. MENTION AGGREGATE DATA AS WELL ASN THE CONSISTENCY PROVIDED BY THE VARIANCE.
    """

    # Call the chat completion API
    response = client.chat.completions.create(
        model="gpt-4", 
        messages=[
            {"role": "system", "content": "You are a fantasy cricket expert. Suggest the best 11 players out of the ones given. Ensure one player from each team is selected."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.9
    )

    return response.choices[0].message.content

def best_team_button():
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


# def get_past_match_performance(player_name, fantasy_points, num_matches=100, key ='total_points'):
#   player_data = fantasy_points.get(player_name)
#   if player_data is None:
#       print(f"Warning: Player not found in data: {player_name}")
#       return [], []  # Return empty lists if player data is not found

#   # Since player_data is a list of tuples (match_key, match_data)
#   # Get the last 'num_matches' matches
#   last_matches_data = player_data[-num_matches:]

#   # Extract match names and total points
#   last_matches = [match_key for match_key, _ in last_matches_data]
#   last_points = [match_data[key] for _, match_data in last_matches_data]

#   return last_matches, last_points

def extract_date_from_match_key(match_key):
  date_pattern = r'(\d{4}-\d{2}-\d{2})'
  match = re.search(date_pattern, match_key)
  if match:
      return match.group(1)
  else:
      return None

def get_past_match_performance(player_name, fantasy_points, num_matches=100, key='total_points', date_of_match=None):
    player_data = fantasy_points.get(player_name)
    if player_data is None:
        print(f"Warning: Player not found in data: {player_name}")
        # Return lists filled with zeros instead of empty lists
        return ['No Match'] * num_matches, [0] * num_matches

    # Handle data structure - check if it's a list or dictionary
    if isinstance(player_data, dict):
        matches_data = list(player_data.items())
    elif isinstance(player_data, list):
        matches_data = player_data
    else:
        print(f"Unexpected data format for player {player_name}")
        return ['No Match'] * num_matches, [0] * num_matches

    if date_of_match:
        try:
            date_of_match_dt = datetime.datetime.strptime(date_of_match, '%Y-%m-%d')
        except ValueError:
            print(f"Invalid date_of_match format: {date_of_match}. Expected YYYY-MM-DD.")
            return ['No Match'] * num_matches, [0] * num_matches
        
        # Filter matches before date_of_match
        filtered_player_data = []
        for match_data in matches_data:
            match_key = match_data[0] if isinstance(match_data, tuple) else match_data
            date_match = re.search(r'\d{4}-\d{2}-\d{2}', str(match_key))
            if date_match:
                match_date_str = date_match.group()
                match_date = datetime.datetime.strptime(match_date_str, '%Y-%m-%d')
                if match_date < date_of_match_dt:
                    filtered_player_data.append(match_data)
    else:
        filtered_player_data = matches_data

    if not filtered_player_data:
        print(f"No matches found for {player_name} before {date_of_match}- IMPUTED WITH ZERO.")
        return ['No Match'] * num_matches, [0] * num_matches

    # Get the last 'num_matches' matches
    last_matches_data = filtered_player_data[-num_matches:]

    # If fewer matches are available, duplicate the last match
    num_matches_needed = num_matches - len(last_matches_data)
    if num_matches_needed > 0 and last_matches_data:
        last_match = last_matches_data[-1]
        last_matches_data.extend([last_match] * num_matches_needed)

    # Extract match names and points based on data structure
    last_matches = []
    last_points = []
    
    for match_data in last_matches_data:
        if isinstance(match_data, tuple):
            match_key, match_info = match_data
            last_matches.append(match_key)
            last_points.append(match_info.get(key, 0))
        else:
            # Handle list format
            last_matches.append(match_data[0])
            last_points.append(match_data[1].get(key, 0))

    # If we still don't have enough matches (shouldn't happen with duplication above, but just in case)
    if len(last_matches) < num_matches:
        remaining_matches = num_matches - len(last_matches)
        last_matches.extend(['No Match'] * remaining_matches)
        last_points.extend([0] * remaining_matches)

    return last_matches, last_points


# After the metrics display section
def plot_team_distribution(mu, sigma, actual_score, optimal_score):
    # Generate points for the normal distribution curve
    x = np.linspace(mu - 4*sigma, mu + 4*sigma, 1000)
    y = stats.norm.pdf(x, mu, sigma)
    
    # Create the plot
    fig = go.Figure()
    
    # Add the normal distribution curve with fill
    fig.add_trace(go.Scatter(
        x=x, 
        y=y,
        mode='lines',
        name='Expected Distribution',
        line=dict(color='blue', width=2),
        fill='tozeroy',  # Fill area under the curve
        fillcolor='rgba(0, 0, 255, 0.1)'  # Light blue fill
    ))
    
    # Add vertical lines with staggered annotations
    fig.add_vline(
        x=actual_score, 
        line_dash="dash",
        line_color="red",
        annotation_text=f"Actual Score: {actual_score:.1f}",
        annotation_position="top right",
        annotation=dict(yshift=10)
    )
    
    fig.add_vline(
        x=optimal_score,
        line_dash="dash",
        line_color="green",
        annotation_text=f"Optimal Score: {optimal_score:.1f}",
        annotation_position="bottom right",
        annotation=dict(yshift=-10)
    )
    
    # Add mean line
    fig.add_vline(
        x=mu,
        line_dash="dot",
        line_color="gray",
        annotation_text=f"Expected Score: {mu:.1f}",
        annotation_position="top left",
        annotation=dict(yshift=20)
    )
    
    # Update layout
    fig.update_layout(
        title="Team Score Distribution",
        xaxis_title="Total Points",
        yaxis_title="Probability Density",
        showlegend=True,
        template="plotly_white",
        height=400,
        margin=dict(t=50, l=50, r=50, b=50)  # Adjust margins
    )
    
    return fig

# Call the function with your values

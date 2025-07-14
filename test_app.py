import streamlit as st
import pandas as pd

teams = pd.read_csv('teams.csv')
games = pd.read_csv('games.csv')

st.title("College Football Matchup Explorer")

teamA = st.selectbox("Select Team A", teams['school'].unique())
teamB = st.selectbox("Select Team B", teams['school'].unique())

if st.button("Show Matchup"):
    matchup = games[
        ((games['home_team'] == teamA) & (games['away_team'] == teamB)) |
        ((games['home_team'] == teamB) & (games['away_team'] == teamA))
    ]
    if matchup.empty:
        st.write("No games found between these teams.")
    else:
        st.dataframe(matchup[['start_date', 'season', 'home_team', 'away_team', 'home_points', 'away_points']])

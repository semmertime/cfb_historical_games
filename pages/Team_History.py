import streamlit as st
import random
import pandas as pd

def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url('https://i.imgur.com/rpIfeFF.png');
                background-size: 250px 250px;
                background-repeat: no-repeat;
                background-position: center -40px;
                padding-top: 175px;
            }
            [data-testid="stSidebarNav"]::before {
                content: "Explore College Football History!";
                display: block;
                margin-left: 20px;
                margin-top: 10px;
                background-position: center;
                font-size: 20px;
                color: #7BAFD4;
                font-weight: bold;
                position: relative;
                top: 10px;
                margin-top: 5px;
                margin-bottom: 20px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
add_logo()

facts = [
    "Did you know? Yale and Harvard first played in 1875.",
    "The longest winning streak in FBS history is Oklahoma's 47-game run (1953–1957).",
    "The Army–Navy Game began in 1890 and is one of college football’s oldest rivalries.",
    "Notre Dame’s “Four Horsemen” backfield gained fame in 1924.",
    "The Rose Bowl, first played in 1902, is the oldest bowl game.",
    "The University of Michigan has the most all-time wins in FBS history.",
    "In 2007, Appalachian State shocked Michigan in one of the biggest upsets ever.",
    "The 1916 Georgia Tech vs. Cumberland game ended 222–0, the largest margin ever.",
    "Before 1968, college football used a one-platoon system—players played both offense and defense.",
    "The Heisman Trophy, awarded to the top player, has been given out since 1935."
]
st.sidebar.info(random.choice(facts))
st.sidebar.markdown("---")
st.sidebar.markdown("**Gridiron Archives** lets you explore the complete history of college football games and rivalries.")
st.sidebar.markdown("Data powered by [CollegeFootballData.com](https://collegefootballdata.com/).")
st.sidebar.markdown("Created by Will Semmer.")
st.sidebar.markdown("Questions? Email: [will.semmer@gmail.com](mailto:will.semmer@gmail.com)")


teams = pd.read_csv('teams.csv')
games = pd.read_csv('games.csv')

st.title("Team Year History")

all_teams = sorted(teams['school'].unique())
team = st.selectbox("Select a Team", all_teams, key="historyTeam")

team_games = games[(games['home_team'] == team) | (games['away_team'] == team)]
st.write(team_games)

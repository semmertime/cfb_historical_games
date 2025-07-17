import streamlit as st
import random
import pandas as pd

st.markdown(
    """
    <style>
    /* Widen the main app content area to 100% of the viewport (minus sidebar) */
    .block-container {
        max-width: 1600px !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
    @media (min-width: 1600px) {
        .block-container {
            max-width: 1700px !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

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
    "The 1916 Georgia Tech vs. Cumberland game ended 222–0, the largest winning margin ever.",
    "Before 1968, college football used a one-platoon system — players played both offense and defense.",
    "The Heisman Trophy, awarded annually to the country's top player, has been given out since 1935."
]
st.sidebar.info(random.choice(facts))
st.sidebar.markdown("---")
st.sidebar.markdown("**Gridiron Archives** lets you explore the complete history of college football games and rivalries.")
st.sidebar.markdown("Data powered by [CollegeFootballData.com](https://collegefootballdata.com/).")
st.sidebar.markdown("Created by Will Semmer.")
st.sidebar.markdown("Questions? Email: [will.semmer@gmail.com](mailto:will.semmer@gmail.com)")











teams = pd.read_csv('teams.csv')
games = pd.read_csv('games.csv')

st.write("Session state:", dict(st.session_state))
st.title("Matchup In-Depth")

# Prepare selectors
all_classifications = sorted(teams['classification'].dropna().str.upper().unique())
all_conferences = {
    c: sorted(teams[teams['classification'].str.upper() == c]['conference'].dropna().unique())
    for c in all_classifications
}
all_teams = {
    (c, conf): sorted(teams[(teams['classification'].str.upper() == c) & (teams['conference'] == conf)]['school'].unique())
    for c in all_classifications for conf in all_conferences[c]
}
min_year = int(games['season'].min())
max_year = int(games['season'].max())

# Get previous selections if present
default_class1 = st.session_state.get('class1', all_classifications[0])
default_conf1  = st.session_state.get('conf1', all_conferences[default_class1][0])
default_team1  = st.session_state.get('team1', all_teams[(default_class1, default_conf1)][0])

default_class2 = st.session_state.get('class2', all_classifications[0])
default_conf2  = st.session_state.get('conf2', all_conferences[default_class2][0])
default_team2  = st.session_state.get('team2', all_teams[(default_class2, default_conf2)][0])

default_year = st.session_state.get('year_range', (max_year, max_year))[1]  # pick last year if available

selectors, pad, controls = st.columns([2, 0.01, 1])

with selectors:
    # Team 1 selectors
    col1, col2, col3 = st.columns(3, gap="small")
    with col1:
        class_1 = st.selectbox("Classification", all_classifications, index=all_classifications.index(default_class1), key="class1")
    with col2:
        conf_1 = st.selectbox("Conference", all_conferences[class_1], index=all_conferences[class_1].index(default_conf1), key="conf1")
    with col3:
        teams1 = all_teams[(class_1, conf_1)]
        idx1 = teams1.index(default_team1) if default_team1 in teams1 else 0
        team_1 = st.selectbox("Team", teams1, index=idx1, key="team1")

    # Team 2 selectors
    col4, col5, col6 = st.columns(3, gap="small")
    with col4:
        class_2 = st.selectbox("Classification ", all_classifications, index=all_classifications.index(default_class2), key="class2")
    with col5:
        conf_2 = st.selectbox("Conference ", all_conferences[class_2], index=all_conferences[class_2].index(default_conf2), key="conf2")
    with col6:
        teams2 = all_teams[(class_2, conf_2)]
        idx2 = teams2.index(default_team2) if default_team2 in teams2 else 0
        team_2 = st.selectbox("Team ", teams2, index=idx2, key="team2")

with controls:
    # Year selector (single value)
    year_options = list(range(min_year, max_year + 1))
    year_idx = year_options.index(default_year) if default_year in year_options else len(year_options) - 1
    year = st.selectbox("Select Year", year_options, index=year_idx)
    go = st.button("Show Game Details", use_container_width=True)

# --- Filter for games on button click ---
if go:
    filtered_games = games[
        (((games['home_team'] == team_1) & (games['away_team'] == team_2)) |
         ((games['home_team'] == team_2) & (games['away_team'] == team_1))) &
        (games['season'] == year)
    ].copy()

    # Only include games that have been played
    played_mask = (
        filtered_games['home_points'].notna() & filtered_games['away_points'].notna() &
        ~((filtered_games['home_points'] == 0) & (filtered_games['away_points'] == 0))
    )
    filtered_games = filtered_games[played_mask]

    if filtered_games.empty:
        st.warning("No games found between these teams in the selected year.")
    else:
        # Always parse the date before using it!
        filtered_games['parsed_date'] = pd.to_datetime(filtered_games['start_date'], errors='coerce')
    
        # If only one game, select it automatically. If more, let user choose.
        if len(filtered_games) == 1:
            selected_game = filtered_games.iloc[0]
        else:
            filtered_games['Game_Label'] = (
                filtered_games['parsed_date'].dt.strftime('%a, %b. %d, %Y') + " | " +
                filtered_games['home_team'] + " " + filtered_games['home_points'].astype(int).astype(str) +
                " - " +
                filtered_games['away_team'] + " " + filtered_games['away_points'].astype(int).astype(str)
            )
            sel = st.selectbox("Choose specific game", filtered_games['Game_Label'], index=0)
            selected_game = filtered_games[filtered_games['Game_Label'] == sel].iloc[0]
    
        # --- Display details ---
        date_str = selected_game['parsed_date'].strftime('%A, %B %d, %Y') if pd.notnull(selected_game['parsed_date']) else selected_game['start_date']
        st.markdown(f"**Date:** {date_str}")
        st.markdown(f"**Location:** {selected_game['venue_id']}")
        st.markdown(f"**Final Score:** {selected_game['home_team']} {selected_game['home_points']} — {selected_game['away_team']} {selected_game['away_points']}")
        st.markdown(f"**Attendance:** {int(selected_game['attendance']) if pd.notnull(selected_game['attendance']) else 'N/A'}")
        st.markdown(f"**Conference Game:** {'Yes' if selected_game['conference_game'] else 'No'}")
        if pd.notnull(selected_game['notes']) and selected_game['notes']:
            st.markdown(f"**Notes:** {selected_game['notes']}")
        st.markdown("---")












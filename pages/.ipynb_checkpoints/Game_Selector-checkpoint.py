import streamlit as st
import random
import pandas as pd
import os
import numpy as np

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












# Define the range of years you have data for
years = list(range(2004, 2025))  # Update upper bound for new seasons as needed

# --- Load all game_stats ---
game_stats_list = []
for year in years:
    file_path = f"game_stats/{year}.csv"
    if os.path.exists(file_path):
        game_stats_list.append(pd.read_csv(file_path))
game_stats = pd.concat(game_stats_list, ignore_index=True)

# --- Load all advanced_game_stats ---
adv_stats_list = []
for year in years:
    file_path = f"advanced_game_stats/{year}.csv"
    if os.path.exists(file_path):
        adv_stats_list.append(pd.read_csv(file_path))
advanced_stats = pd.concat(adv_stats_list, ignore_index=True)

teams = pd.read_csv('teams.csv')
games = pd.read_csv('games.csv')



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

st.markdown(
    "<h1 style='margin-top: 0; margin-bottom: 0;'>Compare Any Two Teams:</h1>",
    unsafe_allow_html=True
)

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

selectors, pad, controls = st.columns([2, 0.01, 1])

with selectors:
    # Top row - Team 1
    col1, col2, col3 = st.columns(3, gap="small")
    with col1:
        class_1 = st.selectbox("Classification", all_classifications, key="class1")
    with col2:
        conf_1 = st.selectbox("Conference", all_conferences[class_1], key="conf1")
    with col3:
        team_1 = st.selectbox("Team", all_teams[(class_1, conf_1)], key="team1")

    # Bottom row - Team 2
    col4, col5, col6 = st.columns(3, gap="small")
    with col4:
        class_2 = st.selectbox("Classification ", all_classifications, key="class2")
    with col5:
        conf_2 = st.selectbox("Conference ", all_conferences[class_2], key="conf2")
    with col6:
        team_2 = st.selectbox("Team ", all_teams[(class_2, conf_2)], key="team2")

with controls:
    year_range = st.slider(
        "Select Year Range",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        step=1
    )
    go = st.button("Go!", use_container_width=True)

if go:
    st.info("Switch to the 'Matchup In-Depth' tab to explore any specific game between your selected teams!")
    # Filter for games between these two teams within the selected years
    mask = (
        (((games['home_team'] == team_1) & (games['away_team'] == team_2)) |
         ((games['home_team'] == team_2) & (games['away_team'] == team_1)))
        & (games['season'] >= year_range[0]) & (games['season'] <= year_range[1])
    )
    # Remove games with 0-0 or missing scores (future/unplayed games)
    matchup_games = games[mask].copy()
    played_mask = (matchup_games['home_points'].notna()) & (matchup_games['away_points'].notna()) \
        & ~((matchup_games['home_points'] == 0) & (matchup_games['away_points'] == 0))
    matchup_games = matchup_games[played_mask]

    # Parse date if needed, then sort descending by date (newest first)
    if 'start_date' in matchup_games.columns:
        matchup_games['parsed_date'] = pd.to_datetime(matchup_games['start_date'], errors='coerce')
        matchup_games = matchup_games.sort_values('parsed_date', ascending=False)
    else:
        matchup_games = matchup_games.sort_values('season', ascending=False)
    
    # LEFT COLUMN: Table of all games
    col1, col2 = st.columns([1.1,0.9], gap="large")
    st.markdown(
        """
        <style>
        .summary-table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            background: #f6f7f8;
            border-radius: 9px;              /* LESS ROUNDED */
            border: 2px solid #20315B;       /* ADD NAVY BORDER */
            margin-bottom: 1.1em;
            font-size: 1.13em;
            overflow: hidden;
        }
        .summary-table th {
            background: #1B253C;             /* CREAM/IVORY HEADER */
            color: #FAF7F1;                  /* DARK NAVY TEXT */
            font-weight: bold;
            padding: 0.4em 0.8em;
            text-align: center;
            font-size: 1.08em;
            border-bottom: 2px solid #eaeaea;
            white-space: nowrap;             /* NO WRAPPING */
        }
        .summary-table td {
            padding: 0.2em 1em;
            text-align: center;
            border-bottom: 1px solid #eee;
            font-weight: 500;
            color: #283046;
            white-space: nowrap;             /* PREVENT CELL WRAP */
            overflow: hidden;
            text-overflow: ellipsis;
            max-width: 180px;
        }
        .summary-table tr:last-child td {
            border-bottom: none;
        }
        .summary-table tbody tr:hover {
            background: #e7ecf6;
        }
        .summary-table td:first-child {
            font-weight: bold;
            color: #112047;
        }
        .summary-table td:nth-child(2) {
            color: #324973;
            font-weight: bold;
        }
        .summary-table td:nth-child(3), .summary-table td:nth-child(4) {
            color: #4C5973;
        }
        .summary-table b {
            font-weight: 900 !important;
            color: #20315B;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    with col1:
        st.markdown(f"### {team_1} vs. {team_2} Games")
        
        # Calculate win stats
        t1_wins = (
            ((matchup_games['home_team'] == team_1) & (matchup_games['home_points'] > matchup_games['away_points'])) |
            ((matchup_games['away_team'] == team_1) & (matchup_games['away_points'] > matchup_games['home_points']))
        ).sum()
        t2_wins = (
            ((matchup_games['home_team'] == team_2) & (matchup_games['home_points'] > matchup_games['away_points'])) |
            ((matchup_games['away_team'] == team_2) & (matchup_games['away_points'] > matchup_games['home_points']))
        ).sum()
        ties = (matchup_games['home_points'] == matchup_games['away_points']).sum()
        total_games = len(matchup_games)
        
        # Most recent win for each team
        def most_recent_win(df, team):
            for _, row in df.iterrows():
                if ((row['home_team'] == team) and (row['home_points'] > row['away_points'])) or \
                   ((row['away_team'] == team) and (row['away_points'] > row['home_points'])):
                    winner_score = int(row['home_points'] if row['home_team'] == team else row['away_points'])
                    loser_score = int(row['away_points'] if row['home_team'] == team else row['home_points'])
                    year = int(row['season'])
                    return f"{year}: {winner_score} - {loser_score}"
            return "-"
    
        # Longest win streak for each team
        def longest_streak(df, team):
            streak = max_streak = 0
            start_year = end_year = None
            for _, row in df.sort_values('parsed_date').iterrows():
                win = ((row['home_team'] == team) and (row['home_points'] > row['away_points'])) or \
                      ((row['away_team'] == team) and (row['away_points'] > row['home_points']))
                if win:
                    if streak == 0:
                        streak_start_year = row['season']
                    streak += 1
                    last_year = row['season']
                    if streak > max_streak:
                        max_streak = streak
                        start_year = streak_start_year
                        end_year = last_year
                else:
                    streak = 0
            if max_streak == 0:
                return "-"
            return f"{max_streak} ({start_year}–{end_year})"
        
        t1_recent = most_recent_win(matchup_games, team_1)
        t2_recent = most_recent_win(matchup_games, team_2)
        t1_streak = longest_streak(matchup_games, team_1)
        t2_streak = longest_streak(matchup_games, team_2)
    
        # --- Build HTML Table ---
        summary_table = f"""
        <table class='summary-table'>
            <thead>
                <tr>
                    <th>Team</th>
                    <th>Wins</th>
                    <th>Most Recent Win</th>
                    <th>Longest Win Streak</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>{team_1}</td>
                    <td>{t1_wins}</td>
                    <td>{t1_recent}</td>
                    <td>{t1_streak}</td>
                </tr>
                <tr>
                    <td>{team_2}</td>
                    <td>{t2_wins}</td>
                    <td>{t2_recent}</td>
                    <td>{t2_streak}</td>
                </tr>
            </tbody>
        </table>
        """
        st.markdown(summary_table, unsafe_allow_html=True)






        

        if not matchup_games.empty:
            # Date formatting
            matchup_games['parsed_date'] = pd.to_datetime(matchup_games['start_date'], errors='coerce')
            matchup_games['Date'] = matchup_games['parsed_date'].dt.strftime('%a, %b. %d, %Y')
    
            # Venue mapping
            venue_pairs = teams[["home_venue_id", "home_venue"]].drop_duplicates()
            venue_map = dict(zip(venue_pairs['home_venue_id'], venue_pairs['home_venue']))
            matchup_games['Venue'] = matchup_games['venue_id'].map(venue_map)
            matchup_games['Venue'] = matchup_games['Venue'].replace({None: 'Unknown', '': 'Unknown'}).fillna('Unknown')
    
            # Clean integer scores
            matchup_games['home_points'] = matchup_games['home_points'].fillna(0).astype(int)
            matchup_games['away_points'] = matchup_games['away_points'].fillna(0).astype(int)
    
            # Build HTML table rows
            rows = ""
            for _, row in matchup_games.iterrows():
                home = f"{row['home_team']} - {row['home_points']}"
                away = f"{row['away_team']} - {row['away_points']}"
                # Bold winner
                if row['home_points'] > row['away_points']:
                    home = f"<b>{home}</b>"
                elif row['away_points'] > row['home_points']:
                    away = f"<b>{away}</b>"
                rows += f"<tr>" \
                        f"<td>{row['Date']}</td>" \
                        f"<td>{home}</td>" \
                        f"<td>{away}</td>" \
                        f"<td>{row['Venue'] or ''}</td>" \
                        f"</tr>"
    
            # Display the HTML table
            st.markdown(
                f"""
                <table class='summary-table'>
                    <thead>
                        <tr>
                            <th style='text-align:center; '>Date</th>
                            <th style='text-align:center; '>Home</th>
                            <th style='text-align:center; '>Away</th>
                            <th style='text-align:center; '>Venue</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows}
                    </tbody>
                </table>
                """, unsafe_allow_html=True
            )
        else:
            st.info("No games found for this matchup in that year range.")

    # RIGHT COLUMN: Summary stats
    with col2:
        n_games = len(matchup_games)
        st.markdown(f"### Total Games Played ({year_range[0]}–{year_range[1]}): {n_games}")
            # ---- Advanced/Classics Stats Table ----
        stats_earliest_year = 2004
        if year_range[0] < stats_earliest_year:
            st.info(
                f"Advanced and box score stats are only available for seasons **2004 and later**. "
                f"Please select a year range starting in 2004 or later to see detailed stat comparisons."
            )
        else:
            stats_games = game_stats[
                ((game_stats['team'] == team_1) & (game_stats['opponent'] == team_2) |
                 (game_stats['team'] == team_2) & (game_stats['opponent'] == team_1))
                & (game_stats['season'] >= year_range[0])
                & (game_stats['season'] <= year_range[1])
            ].copy()
            
            advanced_games = advanced_stats[
                ((advanced_stats['team'] == team_1) & (advanced_stats['opponent'] == team_2) |
                 (advanced_stats['team'] == team_2) & (advanced_stats['opponent'] == team_1))
                & (advanced_stats['season'] >= year_range[0])
                & (advanced_stats['season'] <= year_range[1])
            ].copy()

            # First, create a tidy "team_points" column for each row in game_stats:
            # We'll merge in both home and away, and then pick the right value for each row.
            games_sub = games[['id', 'home_team', 'home_points', 'away_team', 'away_points']]
            
            # Merge so each row gets home and away info for the correct game
            merged = game_stats.merge(
                games_sub,
                left_on='game_id',
                right_on='id',
                how='left'
            )
            
            # Now, create a column 'points' that is home_points if team == home_team, else away_points if team == away_team
            def get_points(row):
                if row['team'] == row['home_team']:
                    return row['home_points']
                elif row['team'] == row['away_team']:
                    return row['away_points']
                else:
                    return np.nan
            
            merged['points'] = merged.apply(get_points, axis=1)

            def get_attempts(s):
                # Handle missing or invalid data
                try:
                    return int(str(s).split('-')[1])
                except:
                    return 0

            def get_completions(s):
                try:
                    return int(str(s).split('-')[0])
                except:
                    return 0
                    
            merged['attempts'] = merged['completionAttempts'].apply(get_attempts)
            merged['completions'] = merged['completionAttempts'].apply(get_completions)

                        
            def agg_side(df, team):
                d = df[df['team'] == team]
                out = {}
                out['Avg Points/Game']   = round(d['points'].mean(), 1) if len(d) else 0
                out['Total TDs']  = int(d['passingTDs'].sum() + d['rushingTDs'].sum() + d['defensiveTDs'].sum() + d['kickReturnTDs'].sum() + d['puntReturnTDs'].sum())
                out['Total Pass Yards']  = f"{d['netPassingYards'].sum():,}"
                out['Total Rush Yards']  = f"{d['rushingYards'].sum():,}"
                out['Avg Pass Yards/G']  = round(d['netPassingYards'].mean(), 1) if len(d) else 0
                out['Avg Rush Yards/G']  = round(d['rushingYards'].mean(), 1) if len(d) else 0
                out['Avg Yards/Pass']    = round(d['netPassingYards'].sum() / max(1, d['attempts'].sum()), 2)
                out['Completion %']      = f"{round(100 * d['completions'].sum() / max(1, d['attempts'].sum()), 1)}%"
                out['Avg Yards/Rush']    = round(d['rushingYards'].sum() / max(1, d['rushingAttempts'].sum()), 2)
                out['Turnovers Allowed'] = d['turnovers'].sum() if 'turnovers' in d else d['fumblesLost'].sum() + d['passesIntercepted'].sum()
                out['Sacks Forced']             = int(d['sacks'].sum())
                return out
            
            mask = (
                (((merged['team'] == team_1) & (merged['opponent'] == team_2)) |
                 ((merged['team'] == team_2) & (merged['opponent'] == team_1)))
                & (merged['season'] >= year_range[0]) & (merged['season'] <= year_range[1])
            )
            matchup_stats = merged[mask].copy()
                   
            team1_stats = agg_side(matchup_stats, team_1)
            team2_stats = agg_side(matchup_stats, team_2)

            def bold_better(t1, t2, flip=False):
                try:
                    v1 = float(str(t1).replace(',', '').replace('%', '').strip())
                    v2 = float(str(t2).replace(',', '').replace('%', '').strip())
                except:
                    return (t1, t2)
                if flip:
                    if v1 < v2:
                        return (f"<b>{t1}</b>", t2)
                    elif v2 < v1:
                        return (t1, f"<b>{t2}</b>")
                    else:
                        return (t1, t2)
                else:
                    if v1 > v2:
                        return (f"<b>{t1}</b>", t2)
                    elif v2 > v1:
                        return (t1, f"<b>{t2}</b>")
                    else:
                        return (t1, t2)
            
            stat_labels = [
                #         (Display Name,         flip?)
                ('Avg Points/Game',         False),
                ('Total TDs',               False),
                ('Total Pass Yards',        False),
                ('Total Rush Yards',        False),
                ('Avg Pass Yards/G',        False),
                ('Avg Rush Yards/G',        False),
                ('Completion %',            False),
                ('Avg Yards/Pass',          False),
                ('Avg Yards/Rush',          False),
                ('Turnovers Allowed',       True),   # Lower is better!
                ('Sacks Forced',            False),
            ]

            rows = ""
            for stat, flip in stat_labels:
                t1_val = team1_stats.get(stat, '-')
                t2_val = team2_stats.get(stat, '-')
                t1_disp, t2_disp = bold_better(t1_val, t2_val, flip=flip)
                rows += f"<tr><td>{stat}</td><td>{t1_disp}</td><td>{t2_disp}</td></tr>"

            
            # Filter advanced stats for these two teams & years
            mask_adv = (
                (((advanced_stats['team'] == team_1) & (advanced_stats['opponent'] == team_2)) |
                 ((advanced_stats['team'] == team_2) & (advanced_stats['opponent'] == team_1)))
                & (advanced_stats['season'] >= year_range[0]) & (advanced_stats['season'] <= year_range[1])
            )
            matchup_advanced = advanced_stats[mask_adv].copy()
            
            def get_adv_means(df, team, cols):
                d = df[df['team'] == team]
                return {col: d[col].mean() for col in cols}
            
            # List: (Label, Column Name, Decimal Places, Is Percent)
            adv_stat_labels = [
                #         (Display Name, Column Name, Decimals, IsPercent, flip?)
                ("Off. Success Rate",           "offense_successRate",         1, True,  False),
                ("Off. Explosiveness",          "offense_explosiveness",       2, False, False),
                ("Passing Success Rate",        "offense_passingPlays_successRate", 1, True,  False),
                ("Rushing Success Rate",        "offense_rushingPlays_successRate", 1, True,  False),
                ("Line Yards / Play",           "offense_lineYards",           2, False, False),
                ("Second Level Yards / Play",   "offense_secondLevelYards",    2, False, False),
                ("Def. Stuff Rate",             "defense_stuffRate",           1, True,  False),
            ]

            
            adv_cols = [col for _, col, _, _, _ in adv_stat_labels]
            team1_adv_stats = get_adv_means(matchup_advanced, team_1, adv_cols)
            team2_adv_stats = get_adv_means(matchup_advanced, team_2, adv_cols)
            
            def format_adv(value, is_percent=False, dec=2):
                if pd.isna(value):
                    return "-"
                return f"{value*100:.{dec}f}%" if is_percent else f"{value:.{dec}f}"
            
            rows += f"""
            <tr style="background:#1B253C; color:#FAF7F1;">
                <th>Advanced Stats</th>
                <th>{team_1}</th>
                <th>{team_2}</th>
            </tr>
            """
            
            for label, col, dec, is_percent, flip in adv_stat_labels:
                t1_val = format_adv(team1_adv_stats.get(col), is_percent, dec)
                t2_val = format_adv(team2_adv_stats.get(col), is_percent, dec)
                t1_disp, t2_disp = bold_better(t1_val, t2_val, flip=flip)
                rows += f"<tr><td>{label}</td><td>{t1_disp}</td><td>{t2_disp}</td></tr>"
            
            # --- BUILD FINAL TABLE ---
            table_html = f"""
            <table class='summary-table'>
                <thead>
                    <tr style="background:#1B253C; color:#FAF7F1;">
                        <th>Stat</th>
                        <th>{team_1}</th>
                        <th>{team_2}</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
            """
            st.markdown(table_html, unsafe_allow_html=True)





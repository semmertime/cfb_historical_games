import streamlit as st
import random

# --- Colors to match your sidebar theme ---
SIDEBAR_BG = "#11172B"  # Your sidebar/navy background
HEADING_COLOR = "#7BAFD4"
TEXT_COLOR = "#363636"

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


# Set up columns: empty sides, center with all main content
left, center, right = st.columns([1, 3, 1])

with left:
    # Placeholder, leave blank for now
    pass


with right:
    # Placeholder, leave blank for now
    pass

with center:
    # ---- Logo in a centered card ----
    st.markdown(
        f"""
        <div style='
            background-color: {SIDEBAR_BG};
            border-radius: 25px;
            padding: 0 0 0 0;
            text-align: center;
            box-shadow: 0 2px 16px rgba(0,0,0,0.2);
        '>
            <img src='https://i.imgur.com/rpIfeFF.png' width='250' style='display:block; margin:auto;'>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # ---- Headline and Short Description ----
    st.markdown(
        f"<h1 style='color:{HEADING_COLOR};text-align:center;font-size: 50px;'>Gridiron Archives</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<h4 style='color:{TEXT_COLOR};text-align:center;font-weight:400;margin-top:-15px;'>A Modern, Searchable Database of College Football History.</h4>",
        unsafe_allow_html=True,
    )
    
    # ---- Main Description Section ----
    st.markdown(
        f"""
        <div style='
            background-color: #F4F7FA;
            border-radius: 15px;
            padding: 20px 32px;
            margin-bottom: 20px;
            color: {TEXT_COLOR};
            text-align:center;
            font-size: 17px;
            margin-left:auto;
            margin-right:auto;
            line-height:1.6;
        '>
        <p>
        <b>Gridiron Archives</b> is a fan-built project to make the full scope of college football history accessible to everyone. With clean, up-to-date data, you can search for any matchup, trace the complete history of your team, and soon, generate custom newsletters and recaps.
        """,
        unsafe_allow_html=True,
    )
    
    # ---- Section Overview at the Bottom ----
    st.markdown(
        """
        <div style='
            display: flex;
            justify-content: space-between;
            gap: 20px;
            margin: 0 auto;
        '>
            <div style='flex:1;background:#F0F0F5;border-radius:10px;padding:16px 18px;margin-bottom:16px;'>
                <b>🔗 Matchup Selector</b><br>
                Search for every game ever played between two teams. See results, dates, and scores.
            </div>
            <div style='flex:1;background:#F0F0F5;border-radius:10px;padding:16px 18px;margin-bottom:16px;'>
                <b>📅 Team History</b><br>
                Dive into a team’s year-by-year performance, including record, rivals, and memorable seasons.
            </div>
            <div style='flex:1;background:#F0F0F5;border-radius:10px;padding:16px 18px;margin-bottom:16px;'>
                <b>📰 Newsletter</b><br>
                (Coming soon!) Generate custom recaps, summaries, and insights to share.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    st.sidebar.markdown("**Gridiron Archives** lets you explore the complete history of college football games and rivalries.")
    st.sidebar.markdown("Data powered by [CollegeFootballData.com](https://collegefootballdata.com/).")
    st.sidebar.markdown("Created by Will Semmer.")
    st.sidebar.markdown("Questions? Email: [will.semmer@gmail.com](mailto:will.semmer@gmail.com)")



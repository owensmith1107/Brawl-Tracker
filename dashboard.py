import streamlit as st
import plotly.express as px
import requests

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="BrawlTracker",
    page_icon="🎮",
    layout="wide"
)

st.title("🎮 BrawlTracker")
st.caption("Personal Brawl Stars stats dashboard")

# Sidebar filters
st.sidebar.header("Filters")
game_type = st.sidebar.selectbox(
    "Game Type",
    options=["All", "trophy_road", "ranked_solo", "ranked_team", "friendly"],
    index=0
)
game_type_param = None if game_type == "All" else game_type


# ── Helper ──────────────────────────────────────────────────────────────────
def fetch(endpoint: str, params: dict = {}) -> list:
    try:
        r = requests.get(f"{API_URL}{endpoint}", params=params)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"API error: {e}")
        return []


# ── Brawler Stats ────────────────────────────────────────────────────────────
st.header("Brawler Performance")

brawler_data = fetch("/stats/brawlers", {"game_type": game_type_param})

if brawler_data:
    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(
            brawler_data,
            x="brawler_name",
            y="win_rate_pct",
            color="win_rate_pct",
            color_continuous_scale="RdYlGn",
            range_color=[0, 100],
            title="Win Rate by Brawler (%)",
            labels={"brawler_name": "Brawler", "win_rate_pct": "Win Rate %"}
        )
        fig.add_hline(y=50, line_dash="dash", line_color="white", opacity=0.4)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.scatter(
            brawler_data,
            x="games_played",
            y="win_rate_pct",
            text="brawler_name",
            color="win_rate_pct",
            color_continuous_scale="RdYlGn",
            range_color=[0, 100],
            title="Win Rate vs Games Played",
            labels={"games_played": "Games Played", "win_rate_pct": "Win Rate %"}
        )
        fig2.add_hline(y=50, line_dash="dash", line_color="white", opacity=0.4)
        fig2.update_traces(textposition="top center")
        st.plotly_chart(fig2, use_container_width=True)

    # Summary metrics
    total_games = sum(b["games_played"] for b in brawler_data)
    total_wins = sum(b["wins"] for b in brawler_data)
    overall_wr = round(total_wins * 100 / total_games, 1) if total_games else 0
    best_brawler = max(brawler_data, key=lambda x: x["win_rate_pct"])
    most_played = max(brawler_data, key=lambda x: x["games_played"])

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Games", total_games)
    m2.metric("Overall Win Rate", f"{overall_wr}%")
    m3.metric("Best Brawler", f"{best_brawler['brawler_name']} ({best_brawler['win_rate_pct']}%)")
    m4.metric("Most Played", f"{most_played['brawler_name']} ({most_played['games_played']} games)")

else:
    st.info("No brawler data found.")


# ── Map Stats ────────────────────────────────────────────────────────────────
st.header("Map Performance")

map_data = fetch("/stats/maps", {"game_type": game_type_param})

if map_data:
    col3, col4 = st.columns(2)

    with col3:
        fig3 = px.bar(
            map_data,
            x="map_name",
            y="win_rate_pct",
            color="win_rate_pct",
            color_continuous_scale="RdYlGn",
            range_color=[0, 100],
            title="Win Rate by Map (%)",
            labels={"map_name": "Map", "win_rate_pct": "Win Rate %"}
        )
        fig3.add_hline(y=50, line_dash="dash", line_color="white", opacity=0.4)
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        fig4 = px.scatter(
            map_data,
            x="games_played",
            y="win_rate_pct",
            text="map_name",
            color="event_mode",
            title="Win Rate vs Games Played by Map",
            labels={"games_played": "Games Played", "win_rate_pct": "Win Rate %"}
        )
        fig4.add_hline(y=50, line_dash="dash", line_color="white", opacity=0.4)
        fig4.update_traces(textposition="top center")
        st.plotly_chart(fig4, use_container_width=True)
else:
    st.info("No map data found.")


# ── Teammate Stats ───────────────────────────────────────────────────────────
st.header("Teammate Performance")

min_games = st.slider("Minimum games together", 1, 10, 1)
teammate_data = fetch("/stats/teammates", {"min_games": min_games})

if teammate_data:
    fig5 = px.bar(
        teammate_data,
        x="teammate_name",
        y="win_rate_pct",
        color="win_rate_pct",
        color_continuous_scale="RdYlGn",
        range_color=[0, 100],
        hover_data=["games_together"],
        title="Win Rate by Teammate (%)",
        labels={"teammate_name": "Teammate", "win_rate_pct": "Win Rate %"}
    )
    fig5.add_hline(y=50, line_dash="dash", line_color="white", opacity=0.4)
    st.plotly_chart(fig5, use_container_width=True)
else:
    st.info("No teammate data found.")


# ── Recent Battles ───────────────────────────────────────────────────────────
st.header("Recent Battles")

battle_data = fetch("/battles", {"game_type": game_type_param, "limit": 25})

if battle_data:
    st.dataframe(
        battle_data,
        use_container_width=True,
        column_order=["battle_time", "map_name", "event_mode", "game_type", 
                      "result", "duration", "trophy_change"]
    )
else:
    st.info("No battle data found.")
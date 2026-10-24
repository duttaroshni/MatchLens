import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="MatchLens",
    page_icon="⚽",
    layout="wide"
)

df = pd.read_csv("data/epl_player_stats_24_25.csv")

st.sidebar.title("Filters")

clubs = sorted(df["Club"].unique())

selected_club = st.sidebar.selectbox(
    "Select Club",
    ["All Clubs"] + clubs
)

filtered_df = df

if selected_club != "All Clubs":
    filtered_df = df[df["Club"] == selected_club]

st.title("⚽ MatchLens")

st.subheader("Premier League 2024/25 Overview")

total_players = filtered_df.shape[0]
total_clubs = filtered_df["Club"].nunique()
total_goals = filtered_df["Goals"].sum()
total_assists = filtered_df["Assists"].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("👥 Players", total_players)
col2.metric("🏟️ Clubs", total_clubs)
col3.metric("⚽ Goals", total_goals)
col4.metric("🎯 Assists", total_assists)

st.divider()

display_df = filtered_df.reset_index(drop=True)

display_df.index = display_df.index+1

st.subheader("📋 Player Statistics")
st.dataframe(display_df)

st.divider()

left, right = st.columns(2)

with left: 
    st.subheader("🏆 Top Scorers")

    top_scorers = (
        filtered_df
        .sort_values(by="Goals", ascending=False)
        [["Player Name", "Club", "Goals", "Assists"]]
        .head(10)
        .reset_index(drop=True)
    )

    top_scorers.index += 1

    st.dataframe(top_scorers)

st.divider()


with right:
    st.subheader("🎯 Top Assists")

    top_assists = (
        filtered_df
        .sort_values(by="Assists", ascending=False)
        [["Player Name", "Club", "Assists", "Goals"]]
        .head(10)
        .reset_index(drop=True)
    )

    top_assists.index += 1

    st.dataframe(top_assists)

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("🏟️ Goals by Club")

    club_goals = (
        df
        .groupby("Club")["Goals"]
        .sum()
        .reset_index()
        .sort_values(by="Goals", ascending=False)
    )

    club_fig = px.bar(
        club_goals,
        x="Goals",
        y="Club",
        orientation="h",
    )

    club_fig.update_layout(
        xaxis_title=None,
        yaxis_title=None,
        height = 500,
        margin=dict(t=5)
    )

    club_fig.update_yaxes(autorange="reversed")

    st.plotly_chart(club_fig, 
                    use_container_width=True,
                    config={"displayModeBar":False}
    )

with right:
    st.subheader("⚽ Top 10 Goal Scorers")

    scorer_fig = px.bar(
        top_scorers,
        x="Goals",
        y="Player Name",
        orientation="h",
        text="Goals"
    )

    scorer_fig.update_yaxes(autorange="reversed")

    scorer_fig.update_traces(
        textposition="outside"
    )

    scorer_fig.update_layout(
        xaxis_title=None,
        yaxis_title=None,
        showlegend=False,
        height = 500,
        margin=dict(t=1)
    )

    st.plotly_chart(scorer_fig, use_container_width=True,
                    config={"displayModeBar":False}
    )
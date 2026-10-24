import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Team Comparison",
    page_icon="⚔️",
    layout="wide"
)

df = pd.read_csv("data/epl_player_stats_24_25.csv")

clubs = sorted(df["Club"].unique())

st.title("⚔️ Team Comparison")

st.markdown(
    "Compare two Premier League clubs across attacking statistics."
)

st.divider()

col1, col2 = st.columns(2)

with col1:
    club1 = st.selectbox(
        "🏟️ Club A",
        clubs,
        index=0
    )

with col2:
    club2 = st.selectbox(
        "🏟️ Club B",
        clubs,
        index=1
    )

team1 = df[df["Club"] == club1]
team2 = df[df["Club"] == club2]

# -----------------------------
# Team Comparison Overview
# -----------------------------
st.subheader("📊 Team Comparison Overview")

accuracy1 = (
    team1["Shots On Target"].sum() /
    team1["Shots"].sum() * 100
) if team1["Shots"].sum() > 0 else 0

accuracy2 = (
    team2["Shots On Target"].sum() /
    team2["Shots"].sum() * 100
) if team2["Shots"].sum() > 0 else 0

left, right = st.columns(2)

with left:

    st.markdown(f"## 🔵 {club1}")

    c1, c2 = st.columns(2)

    with c1:
        st.metric("⚽ Goals", int(team1["Goals"].sum()))
        st.metric("🥅 Shots", int(team1["Shots"].sum()))

    with c2:
        st.metric("🎯 Assists", int(team1["Assists"].sum()))
        st.metric("🎯 Accuracy", f"{accuracy1:.1f}%")

with right:

    st.markdown(f"## 🔴 {club2}")

    c3, c4 = st.columns(2)

    with c3:
        st.metric("⚽ Goals", int(team2["Goals"].sum()))
        st.metric("🥅 Shots", int(team2["Shots"].sum()))

    with c4:
        st.metric("🎯 Assists", int(team2["Assists"].sum()))
        st.metric("🎯 Accuracy", f"{accuracy2:.1f}%")

st.divider()

fig = go.Figure()

st.subheader("📊 Team Radar")
st.caption("Normalized comparison across key attacking metrics.")

# -----------------------------
# Team Radar
# -----------------------------
st.subheader("📊 Team Radar")
st.caption("Normalized comparison across key attacking metrics.")

metrics = [
    "Goals",
    "Assists",
    "Shots",
    "Shots On Target"
]

team1_totals = [
    team1["Goals"].sum(),
    team1["Assists"].sum(),
    team1["Shots"].sum(),
    team1["Shots On Target"].sum()
]

team2_totals = [
    team2["Goals"].sum(),
    team2["Assists"].sum(),
    team2["Shots"].sum(),
    team2["Shots On Target"].sum()
]

# Normalize values
max_values = [
    max(team1_totals[i], team2_totals[i])
    for i in range(len(metrics))
]

team1_values = [
    team1_totals[i] / max_values[i] if max_values[i] != 0 else 0
    for i in range(len(metrics))
]

team2_values = [
    team2_totals[i] / max_values[i] if max_values[i] != 0 else 0
    for i in range(len(metrics))
]

# Close the radar
radar_metrics = metrics + [metrics[0]]
team1_radar = team1_values + [team1_values[0]]
team2_radar = team2_values + [team2_values[0]]

fig = go.Figure()

fig.add_trace(
    go.Scatterpolar(
        r=team1_radar,
        theta=radar_metrics,
        fill="toself",
        fillcolor="rgba(30,99,182,0.25)",
        line=dict(
            color="#1E63B6",
            width=3
        ),
        name=club1
    )
)

fig.add_trace(
    go.Scatterpolar(
        r=team2_radar,
        theta=radar_metrics,
        fill="toself",
        fillcolor="rgba(211,47,47,0.25)",
        line=dict(
            color="#D32F2F",
            width=3
        ),
        name=club2
    )
)

fig.update_layout(
    template="plotly_dark",
    height=650,
    title=None,
    polar=dict(
        bgcolor="#111318",
        radialaxis=dict(
            visible=True,
            range=[0, 1],
            showticklabels=False
        )
    ),
    margin=dict(
        l=40,
        r=40,
        t=30,
        b=30
    )
)

st.plotly_chart(
    fig,
    width="stretch",
    theme=None,
    config={"displayModeBar": False}
)
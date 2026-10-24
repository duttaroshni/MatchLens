import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Team Analysis",
    page_icon="🏟️",
    layout="wide"
)

# -----------------------------
# Load Data
# -----------------------------
df = pd.read_csv("data/epl_player_stats_24_25.csv")

# -----------------------------
# Sidebar
# -----------------------------
clubs = sorted(df["Club"].unique())

selected_club = st.sidebar.selectbox(
    "Select Club",
    clubs
)

# -----------------------------
# Filter Club
# -----------------------------
club_df = df[df["Club"] == selected_club]

# Team totals
team = (
    club_df
    .agg({
        "Goals": "sum",
        "Assists": "sum",
        "Shots": "sum",
        "Shots On Target": "sum",
        "Minutes": "sum",
        "Appearances": "sum"
    })
)

# -----------------------------
# Page
# -----------------------------
st.title("🏟️ Team Analysis")

st.markdown(
    "Explore team performance through aggregated player statistics."
)

st.divider()

# -----------------------------
# Team KPIs
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("⚽ Goals", int(team["Goals"]))

with col2:
    st.metric("🎯 Assists", int(team["Assists"]))

with col3:
    st.metric("🥅 Shots", int(team["Shots"]))

with col4:
    st.metric(
        "👥 Players",
        club_df["Player Name"].nunique()
    )

st.divider()

# -----------------------------
# Club Highlights
# -----------------------------
st.subheader("🏆 Club Highlights")

top_scorer = club_df.loc[club_df["Goals"].idxmax()]
top_creator = club_df.loc[club_df["Assists"].idxmax()]
most_shots = club_df.loc[club_df["Shots"].idxmax()]

accuracy_df = club_df[club_df["Shots"] > 0].copy()
accuracy_df["Shot Accuracy"] = (
    accuracy_df["Shots On Target"] /
    accuracy_df["Shots"]
) * 100

best_accuracy = accuracy_df.loc[
    accuracy_df["Shot Accuracy"].idxmax()
]

c1, c2 = st.columns(2)

with c1:
    with st.container(border=True):
        st.markdown("### ⚽ Top Scorer")
        st.markdown(
            f"## {top_scorer['Player Name']}"
        )
        st.write(f"Goals: **{int(top_scorer['Goals'])}**")

    with st.container(border=True):
        st.markdown("### 🥅 Most Shots")
        st.markdown(
            f"## {most_shots['Player Name']}"
        )
        st.write(f"Shots: **{int(most_shots['Shots'])}**")

with c2:
    with st.container(border=True):
        st.markdown("### 🎯 Top Creator")
        st.markdown(
            f"## {top_creator['Player Name']}"
        )
        st.write(f"Assists: **{int(top_creator['Assists'])}**")

    with st.container(border=True):
        st.markdown("### 🎯 Best Shot Accuracy")
        st.markdown(
            f"## {best_accuracy['Player Name']}"
        )
        st.write(
            f"Accuracy: **{best_accuracy['Shot Accuracy']:.1f}%**"
        )

st.divider()

# -----------------------------
# Goals by Player
# -----------------------------
st.subheader("⚽ Goals by Player")

goals_df = (
    club_df.sort_values("Goals", ascending=True)
)

fig = px.bar(
    goals_df,
    x="Goals",
    y="Player Name",
    orientation="h",
    color="Goals",
    template="plotly_dark"
)

fig.update_layout(
    title=None,
    yaxis_title=None,
    xaxis_title="Goals"
)

st.plotly_chart(
    fig,
    width="stretch",
    theme=None,
    config={"displayModeBar": False}
)

st.divider()

# -----------------------------
# Assists by Player
# -----------------------------
st.subheader("🎯 Assists by Player")

assists_df = (
    club_df.sort_values("Assists", ascending=True)
)

fig = px.bar(
    assists_df,
    x="Assists",
    y="Player Name",
    orientation="h",
    color="Assists",
    template="plotly_dark"
)

fig.update_layout(
    title=None,
    yaxis_title=None,
    xaxis_title="Assists"
)

st.plotly_chart(
    fig,
    width="stretch",
    theme=None,
    config={"displayModeBar": False}
)

st.divider()

# -----------------------------
# Shot Distribution
# -----------------------------
st.subheader("🥅 Shot Distribution")

shot_df = club_df[club_df["Shots"] >= 5]

fig = px.pie(
    shot_df,
    names="Player Name",
    values="Shots",
    template="plotly_dark"
)

fig.update_layout(title=None)

fig.update_traces(
    textposition="inside",
    textinfo="percent",
    hovertemplate="<b>%{label}</b><br>Shots: %{value}<extra></extra>"
)

st.plotly_chart(
    fig,
    width="stretch",
    theme=None,
    config={"displayModeBar": False}
)

st.divider()

# -----------------------------
# Goal Contributions
# -----------------------------
st.subheader("🤝 Goal Contributions")

gc_df = club_df.copy()

gc_df["Goal Contributions"] = (
    gc_df["Goals"] + gc_df["Assists"]
)

gc_df = gc_df.sort_values(
    "Goal Contributions",
    ascending=True
)

fig = px.bar(
    gc_df,
    x="Goal Contributions",
    y="Player Name",
    orientation="h",
    color="Goal Contributions",
    template="plotly_dark"
)

fig.update_layout(
    title=None,
    yaxis_title=None,
    xaxis_title="Goal Contributions"
)

st.plotly_chart(
    fig,
    width="stretch",
    theme=None,
    config={"displayModeBar": False}
)
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def per90(value, minutes):
    if minutes == 0:
        return 0
    return (value / minutes) * 90


def safe_divide(a, b):
    if b == 0:
        return 0
    return a / b

st.set_page_config(
    page_title="Player Analysis",
    page_icon="👤",
    layout="wide"
)

df = pd.read_csv("data/epl_player_stats_24_25.csv")

clubs = sorted(df["Club"].unique())

selected_club = st.sidebar.selectbox(
    "Select Club",
    ["All Clubs"] + clubs
)

filtered_df = df

if selected_club != "All Clubs":
    filtered_df = df[df["Club"] == selected_club]

positions = sorted(df["Position"].unique())

selected_position = st.sidebar.selectbox(
    "Select Position",
    ["All Positions"] + positions
)

if selected_position != "All Positions":
    filtered_df = filtered_df[filtered_df["Position"] == selected_position]

minimum_minutes = st.sidebar.slider(
    "Minimum Minutes Played",
    0,
    df["Minutes"].max(),
    0
)

filtered_df = filtered_df[filtered_df["Minutes"] >= minimum_minutes]

st.title("👤 Player Analysis")

st.markdown(
    "Explore player performance through interactive visualizations and advanced statistics."
)

st.divider()

players = sorted(filtered_df["Player Name"].unique())

selected_player = st.selectbox(
    "🔍 Search for a Player",
    players
)

player_data = filtered_df[
    filtered_df["Player Name"] == selected_player
]

player = player_data.iloc[0]

st.subheader(player["Player Name"])

position_map = {
    "FWD": "Forward",
    "MID": "Midfielder",
    "DEF": "Defender",
    "GKP": "Goalkeeper"
}

position = position_map[player["Position"]]

st.caption(
    f'{player["Club"]} • {position} • {player["Nationality"]}'
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("⚽ Goals", player["Goals"])

with col2:
    st.metric("🎯 Assists", player["Assists"])

with col3:
    st.metric("⏱ Minutes", player["Minutes"])

with col4:
    st.metric("👕 Appearances", player["Appearances"])

st.divider()

st.subheader("📈 Goals vs Assists")

position_colors = {
    "DEF": "#6FA8DC",
    "MID": "#1E63B6",
    "GKP": "#D09A9A",
    "FWD": "#D32F2F"
}

player_fig = px.scatter(
    filtered_df,
    x="Goals",
    y="Assists",
    color="Position",
    template="plotly_dark",
    hover_name="Player Name",
    hover_data={
        "Club": True,
        "Minutes": True,
        "Goals": True,
        "Assists": True,
        "Position": True
    },
    color_discrete_map=position_colors
)

player_fig.update_traces(
    marker=dict(
        size=10,
        opacity=0.55
    )
)

player_fig.add_trace(
    go.Scatter(
        x=[player["Goals"]],
        y=[player["Assists"]],
        mode="markers",
        showlegend=False,
        hovertemplate=(
            f"<b>{player['Player Name']}</b><br>"
            f"Club: {player['Club']}<br>"
            f"Goals: {player['Goals']}<br>"
            f"Assists: {player['Assists']}<extra></extra>"
        ),
        marker=dict(
            size=22,
            color=position_colors[player["Position"]],
            line=dict(
                color="white",
                width=2.5
            ),
            opacity=1
        )
    )
)

player_fig.add_annotation(
    x=player["Goals"],
    y=player["Assists"],
    text=player["Player Name"],
    showarrow=True,
    arrowhead=2,
    yshift=20,
    font=dict(size=11)
)

player_fig.update_layout(
    title=None,
    xaxis_title="Goals",
    yaxis_title="Assists",
    margin=dict(t=10, l=20, r=20, b=20),
    showlegend=True
)

st.plotly_chart(
    player_fig,
    width="stretch",
    theme=None,
    config={"displayModeBar": False}
)

st.divider()

st.subheader("🆚 Player Comparison")

# ==========================
# Radar Chart
# ==========================

# Calculate derived metrics for every player
radar_df = filtered_df.copy()

radar_df["Goals / 90"] = radar_df.apply(
    lambda x: per90(x["Goals"], x["Minutes"]), axis=1
)

radar_df["Assists / 90"] = radar_df.apply(
    lambda x: per90(x["Assists"], x["Minutes"]), axis=1
)

radar_df["Shots / 90"] = radar_df.apply(
    lambda x: per90(x["Shots"], x["Minutes"]), axis=1
)

radar_df["Shots OT / 90"] = radar_df.apply(
    lambda x: per90(x["Shots On Target"], x["Minutes"]), axis=1
)

radar_df["Goal Contributions / 90"] = radar_df.apply(
    lambda x: per90(x["Goals"] + x["Assists"], x["Minutes"]), axis=1
)

radar_df["Shot Accuracy"] = radar_df.apply(
    lambda x: safe_divide(x["Shots On Target"], x["Shots"]),
    axis=1
)

stats = [
    "Goals / 90",
    "Assists / 90",
    "Shots / 90",
    "Shots OT / 90",
    "Goal Contributions / 90",
    "Shot Accuracy"
]

# Close radar
categories = stats + [stats[0]]

col1, col2 = st.columns(2)

with col1:
    player1 = st.selectbox(
        "👤 Compare Player A",
        players,
        index=players.index(selected_player)
    )

with col2:
    player2 = st.selectbox(
        "👤 Compare Player B",
        players,
        index=0 if players.index(selected_player) != 0 else 1
    )

p1 = radar_df[
    radar_df["Player Name"] == player1
].iloc[0]

p2 = radar_df[
    radar_df["Player Name"] == player2
].iloc[0]

player1_values = []
player2_values = []

for stat in stats:

    maximum = radar_df[stat].max()

    player1_values.append(p1[stat] / maximum)
    player2_values.append(p2[stat] / maximum)

st.subheader("📊 Radar Comparison")
st.caption("Comparison based on normalized per-90 statistics.")

fig = go.Figure()

fig.add_trace(
    go.Scatterpolar(
        r=player1_values,
        theta=categories,
        fill="toself",
        fillcolor="rgba(30,99,182,0.25)",
        name=player1,
        line=dict(
            color="#1E63B6",
            width=3
        )
    )
)

fig.add_trace(
    go.Scatterpolar(
        r=player2_values,
        theta=categories,
        fill="toself",
        fillcolor="rgba(211,47,47,0.25)",
        name=player2,
        line=dict(
            color="#D32F2F",
            width=3
        )
    )
)

fig.update_layout(

    template="plotly_dark",

    title=None,

    height=650,

    showlegend=True,

    polar=dict(

        bgcolor="#111318",

        radialaxis=dict(
            visible=True,
            range=[0, 1],
            showticklabels=False,
            ticks=""
        ),

        angularaxis=dict(
            tickfont=dict(size=13)
        )

    ),

    margin=dict(
        l=50,
        r=50,
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

# Calculate metrics
g90_p1 = per90(p1["Goals"], p1["Minutes"])
g90_p2 = per90(p2["Goals"], p2["Minutes"])

a90_p1 = per90(p1["Assists"], p1["Minutes"])
a90_p2 = per90(p2["Assists"], p2["Minutes"])

shots90_p1 = per90(p1["Shots"], p1["Minutes"])
shots90_p2 = per90(p2["Shots"], p2["Minutes"])

acc_p1 = safe_divide(p1["Shots On Target"], p1["Shots"]) * 100
acc_p2 = safe_divide(p2["Shots On Target"], p2["Shots"]) * 100

ga90_p1 = per90(p1["Goals"] + p1["Assists"], p1["Minutes"])
ga90_p2 = per90(p2["Goals"] + p2["Assists"], p2["Minutes"])

st.divider()
st.header("📌 MatchLens Insights")

# Goal Scoring
with st.container(border=True):
    st.markdown("### ⚽ Goal Scoring")

    if g90_p1 > g90_p2:
        st.write(
            f"**{player1}** scores **{g90_p1:.2f} goals/90**, compared to **{g90_p2:.2f} goals/90** for **{player2}**."
        )
    elif g90_p2 > g90_p1:
        st.write(
            f"**{player2}** scores **{g90_p2:.2f} goals/90**, compared to **{g90_p1:.2f} goals/90** for **{player1}**."
        )
    else:
        st.write("Both players average the same number of goals per 90.")

# Assists
with st.container(border=True):
    st.markdown("### 🎯 Creativity")

    if a90_p1 > a90_p2:
        st.write(
            f"**{player1}** creates **{a90_p1:.2f} assists/90**, while **{player2}** averages **{a90_p2:.2f} assists/90**."
        )
    elif a90_p2 > a90_p1:
        st.write(
            f"**{player2}** creates **{a90_p2:.2f} assists/90**, while **{player1}** averages **{a90_p1:.2f} assists/90**."
        )
    else:
        st.write("Both players average the same assists per 90.")

# Shooting
with st.container(border=True):
    st.markdown("### 🥅 Shooting Volume")

    if shots90_p1 > shots90_p2:
        st.write(
            f"**{player1}** attempts **{shots90_p1:.2f} shots/90**, compared to **{shots90_p2:.2f}** for **{player2}**."
        )
    elif shots90_p2 > shots90_p1:
        st.write(
            f"**{player2}** attempts **{shots90_p2:.2f} shots/90**, compared to **{shots90_p1:.2f}** for **{player1}**."
        )
    else:
        st.write("Both players attempt the same number of shots per 90.")

# Accuracy
with st.container(border=True):
    st.markdown("### 🎯 Shot Accuracy")

    if acc_p1 > acc_p2:
        st.write(
            f"**{player1}** has a shot accuracy of **{acc_p1:.1f}%**, while **{player2}** records **{acc_p2:.1f}%**."
        )
    elif acc_p2 > acc_p1:
        st.write(
            f"**{player2}** has a shot accuracy of **{acc_p2:.1f}%**, while **{player1}** records **{acc_p1:.1f}%**."
        )
    else:
        st.write("Both players have the same shot accuracy.")

# Overall Contribution
with st.container(border=True):
    st.markdown("### 🤝 Overall Contribution")

    if ga90_p1 > ga90_p2:
        st.write(
            f"**{player1}** averages **{ga90_p1:.2f} goal contributions/90**, compared to **{ga90_p2:.2f}** for **{player2}**."
        )
    elif ga90_p2 > ga90_p1:
        st.write(
            f"**{player2}** averages **{ga90_p2:.2f} goal contributions/90**, compared to **{ga90_p1:.2f}** for **{player1}**."
        )
    else:
        st.write("Both players contribute equally per 90.")
import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import euclidean_distances

st.set_page_config(
    page_title="Advanced Analytics",
    page_icon="📈",
    layout="wide"
)

# -----------------------------
# Load Data
# -----------------------------
df = pd.read_csv("data/epl_player_stats_24_25.csv")

# -----------------------------
# Calculate Advanced Metrics
# -----------------------------
df = df.copy()

df["Goals per 90"] = (
    df["Goals"] / df["Minutes"] * 90
).fillna(0)

df["Assists per 90"] = (
    df["Assists"] / df["Minutes"] * 90
).fillna(0)

df["Goal Contributions"] = (
    df["Goals"] +
    df["Assists"]
)

df["Goal Contributions per 90"] = (
    df["Goal Contributions"] /
    df["Minutes"] * 90
).fillna(0)

df["Shots per 90"] = (
    df["Shots"] /
    df["Minutes"] * 90
).fillna(0)

df["Shot Accuracy"] = (
    df["Shots On Target"] /
    df["Shots"] * 100
).fillna(0)

df["Goals per Shot"] = (
    df["Goals"] /
    df["Shots"]
).fillna(0)

# -----------------------------
# Page
# -----------------------------
st.title("📈 Advanced Analytics")

st.markdown(
    "League-wide player analytics using advanced performance metrics."
)

st.divider()

# -----------------------------
# Filters
# -----------------------------
col1, col2 = st.columns(2)

with col1:

    min_minutes = st.slider(
        "Minimum Minutes Played",
        0,
        int(df["Minutes"].max()),
        500,
        step=100
    )

with col2:

    metric = st.selectbox(
        "Leaderboard Metric",
        [
            "Goals per 90",
            "Assists per 90",
            "Goal Contributions per 90",
            "Shots per 90",
            "Shot Accuracy"
        ]
    )

filtered_df = (
    df[df["Minutes"] >= min_minutes]
    .sort_values(metric, ascending=False)
)

st.divider()

# -----------------------------
# Leaderboard
# -----------------------------
st.subheader("🏆 League Leaderboard")

leaderboard = filtered_df[
    [
        "Player Name",
        "Club",
        "Minutes",
        "Goals",
        "Assists",
        "Goal Contributions",
        "Goals per 90",
        "Assists per 90",
        "Goal Contributions per 90",
        "Shots per 90",
        "Shot Accuracy"
    ]
]

st.dataframe(
    leaderboard,
    use_container_width=True,
    hide_index=True
)

st.divider()

# -----------------------------
# Scatter Plot
# -----------------------------
st.subheader("📊 Goals vs Shots")

fig = px.scatter(
    filtered_df,
    x="Shots",
    y="Goals",
    color="Club",
    size="Minutes",
    hover_name="Player Name",
    template="plotly_dark"
)

fig.update_layout(
    title=None
)

st.plotly_chart(
    fig,
    width="stretch",
    theme=None,
    config={"displayModeBar": False}
)

st.divider()

# -----------------------------
# Hidden Gems
# -----------------------------
st.subheader("💎 Hidden Gems")

hidden_gems = (
    filtered_df[
        filtered_df["Minutes"] >= min_minutes
    ]
    .sort_values(
        "Goal Contributions per 90",
        ascending=False
    )
    .head(10)
)

st.caption(
    "Players with outstanding attacking output relative to their playing time."
)

st.dataframe(
    hidden_gems[
        [
            "Player Name",
            "Club",
            "Minutes",
            "Goals",
            "Assists",
            "Goal Contributions per 90"
        ]
    ],
    use_container_width=True,
    hide_index=True
)

st.divider()

# -----------------------------
# Most Efficient Finishers
# -----------------------------
st.subheader("🎯 Most Efficient Finishers")

efficient = (
    filtered_df[
        filtered_df["Shots"] >= 20
    ]
    .sort_values(
        "Goals per Shot",
        ascending=False
    )
    .head(10)
)

st.caption(
    "Players who convert the highest percentage of their shots into goals."
)

st.dataframe(
    efficient[
        [
            "Player Name",
            "Club",
            "Goals",
            "Shots",
            "Goals per Shot"
        ]
    ],
    use_container_width=True,
    hide_index=True
)

st.divider()

# -----------------------------
# Similar Players
# -----------------------------
st.subheader("🔍 Similar Players")

player = st.selectbox(
    "Choose a player",
    sorted(filtered_df["Player Name"].unique())
)

comparison_df = filtered_df.copy()

features = [
    "Goals per 90",
    "Assists per 90",
    "Shots per 90",
    "Shot Accuracy"
]

# Remove missing values
comparison_df = comparison_df.dropna(subset=features)

# Standardize features
scaler = StandardScaler()

scaled_features = scaler.fit_transform(
    comparison_df[features]
)

# Calculate distances
distance_matrix = euclidean_distances(
    scaled_features,
    scaled_features
)

comparison_df = comparison_df.reset_index(drop=True)

player_index = comparison_df[
    comparison_df["Player Name"] == player
].index[0]

comparison_df["Similarity Score"] = distance_matrix[player_index]

similar_players = (
    comparison_df
    .drop(index=player_index)
    .sort_values("Similarity Score")
    .head(5)
)

st.caption(
    "Players with the closest statistical profile."
)

st.dataframe(
    similar_players[
        [
            "Player Name",
            "Club",
            "Goals per 90",
            "Assists per 90",
            "Shots per 90",
            "Shot Accuracy"
        ]
    ],
    hide_index=True,
    use_container_width=True
)
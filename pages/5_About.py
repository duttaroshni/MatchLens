import streamlit as st

st.set_page_config(
    page_title="About MatchLens",
    page_icon="ℹ️",
    layout="wide"
)

st.title("ℹ️ About MatchLens")

st.markdown(
    """
    **MatchLens** is an interactive football analytics dashboard built to
    explore and compare Premier League player and team performances through
    data visualization and advanced statistics.

    The application allows users to analyze individual players, compare clubs,
    discover high-performing players using advanced metrics, and gain insights
    through interactive charts and leaderboards.
    """
)

st.divider()

# ------------------------------------------------
# Project Features
# ------------------------------------------------

st.header("🚀 Features")

col1, col2 = st.columns(2)

with col1:

    st.markdown("""
### 👤 Player Analysis

- Player profile
- Performance KPIs
- Goals vs Assists scatter plot
- Radar chart
- Player comparison
- MatchLens Insights
""")

    st.markdown("""
### 🏟️ Team Analysis

- Team overview
- Club highlights
- Goals by player
- Assists by player
- Shot distribution
- Goal contribution analysis
""")

with col2:

    st.markdown("""
### ⚔️ Team Comparison

- Club vs Club comparison
- Performance overview
- Radar visualization
- Comparative insights
""")

    st.markdown("""
### 📈 Advanced Analytics

- League leaderboard
- Per 90 statistics
- Hidden Gems
- Efficient Finishers
- Goals vs Shots scatter plot
- Similar Players
""")

st.divider()

# ------------------------------------------------
# Dataset
# ------------------------------------------------

st.header("📊 Dataset")

st.markdown("""
- **Competition:** English Premier League
- **Season:** 2024–25
- **Data includes:**
    - Goals
    - Assists
    - Shots
    - Shots on Target
    - Minutes Played
    - Appearances
    - Club Information
""")

st.divider()

# ------------------------------------------------
# Technologies
# ------------------------------------------------

st.header("💻 Technologies Used")

tech1, tech2, tech3 = st.columns(3)

with tech1:
    st.info("""
### Programming

- Python
- Pandas
""")

with tech2:
    st.info("""
### Visualization

- Plotly
- Streamlit
""")

with tech3:
    st.info("""
### Development

- VS Code
- Git
- GitHub
""")

st.divider()

# ------------------------------------------------
# Advanced Metrics
# ------------------------------------------------

st.header("📈 Advanced Metrics Used")

st.markdown("""
MatchLens includes several advanced football metrics:

- Goals per 90
- Assists per 90
- Goal Contributions per 90
- Shots per 90
- Shot Accuracy
- Goals per Shot
- Similar Player Analysis using Euclidean Distance
""")

st.divider()

# ------------------------------------------------
# Future Improvements
# ------------------------------------------------

st.header("🔮 Future Improvements")

st.markdown("""
- Expected Goals (xG) integration
- Expected Assists (xA)
- Passing and defensive statistics
- Multi-season comparison
- Position-specific analytics
- Player search
- Team performance trends
""")

st.divider()

# ------------------------------------------------
# Developer
# ------------------------------------------------

st.header("👩‍💻 Developer")

st.markdown("""
**Roshni Dutta**

B.Tech Computer Science Engineering

KIIT University

Developed as a football analytics portfolio project using Python, Streamlit and Plotly.
""")

st.success("⚽ Thank you for exploring MatchLens!")
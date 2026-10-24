# MatchLens ⚽
### Football Analytics & Player Scouting

MatchLens is an interactive football analytics platform built with Python and Streamlit. It explores player and team performance through data analysis, interactive visualisations, and machine learning.

## Features

- **Player Analysis:** Explore individual player performance and statistics.
- **Team Analysis:** Analyse team-level performance and metrics.
- **Team Comparison:** Compare teams using performance statistics.
- **Advanced Analytics:** Explore deeper analytical insights and player similarities.
- **Interactive Dashboard:** Navigate analyses through a multi-page Streamlit application.

## Tech Stack

- **Language:** Python
- **Data Analysis:** Pandas, NumPy
- **Visualisation:** Plotly, Matplotlib, Seaborn
- **Machine Learning:** Scikit-learn
- **Dashboard:** Streamlit
- **Exploratory Analysis:** Jupyter Notebook

## Project Structure

```text
MatchLens/
├── app.py
├── pages/
│   ├── 1_Player_Analysis.py
│   ├── 2_Team_Analysis.py
│   ├── 3_Team_Comparison.py
│   ├── 4_Advanced_Analytics.py
│   └── 5_About.py
├── data/
│   └── epl_player_stats_24_25.csv
├── notebooks/
│   └── 01_data_exploration.ipynb
├── requirements.txt
├── .gitignore
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/duttaroshni/MatchLens.git
cd MatchLens
```

### 2. Create and activate a virtual environment

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run app.py
```

Streamlit will provide a local URL where you can explore the dashboard.

## Project Goals

- Analyse football performance data.
- Compare players and teams using statistical metrics.
- Explore player similarities using machine learning.
- Present analytical findings through an interactive dashboard.

## Future Improvements

- Expand player similarity analysis.
- Add further performance metrics and filters.
- Improve the dashboard with additional analytical insights.
- Explore more advanced player scouting techniques.

---

**MatchLens** — Turning football statistics into meaningful insights.
# Premier League Elo Ratings Dashboard

This project calculates and visualizes **Elo ratings for all Premier League teams** from the 1992–93 season onward. The interactive dashboard allows users to explore team performance trends, match-by-match Elo ratings, and the biggest single-season gains and losses in Premier League history.

---

## Features

- Compute Elo ratings for all Premier League matches from 1992–93 to 2025.
- Interactive **Streamlit dashboard** with multiple views:
  - **Team-wise Elo trends** across multiple seasons.
  - **Match-by-match Elo ratings** for a selected season.
  - **Top/Bottom performers** based on single-season Elo gains and losses.
- Visualizations include line charts, bar charts, and bubble charts for easy trend analysis.
- Key metrics and historical insights for all teams.

---

## Folder Structure

- `App/` : The Streamlit Dashboard code
- `Data/Raw/` : Original Premier League Match Dataset CSV.
- `Data/Processed/` : Processed data including Elo ratings, gains/losses, and summary tables.
- `Notebooks/` : Jupyter notebooks for calculations, plotting, and analysis.
- `requirements.txt` : Python dependencies

---

## How to Run Locally

1. Clone the repository:

```bash
   git clone https://github.com/yourusername/Premier-League_Elo-Ratings.git
```

2. Navigate to the project folder:

```bash
    cd Premier-League_Elo-Ratings
```
    
3. Install dependencies:

```bash
    pip install -r requirements.txt
```

4. Launch the Streamlit dashboard:
```bash
    streamlit run app.py
```

Your browser will open at the URL provided by Streamlit (usually http://localhost:xxxx).

## Access the Dashboard Online
The live dashboard is hosted on Streamlit Cloud:
[Premier League Elo Ratings Dashboard](https://premier-leaguelo-ratings-dashboard.streamlit.app/)


## Requirements
Python 3.8 or higher
All dependencies are listed in requirements.txt.

## Dashboard Overview
- Home: Project description, technical stack, key metrics, and fun facts.
- Summary: Overview of highest and lowest Elo ratings, peak performance by teams, and comparison charts.
- Team-wise Elo over time: Multi-season and single-season trends for selected teams.
- Top/Bottom Performers: Biggest Elo gains and losses per season, visualized using bubble charts.

## How to Use the Dashboard
1. Navigate using the sidebar to select different views:
    - Home
    - Summary
    - Team-wise Elo over time
    - Top/Bottom Performers
2. Use dropdowns and sliders to select teams and season ranges.
3. Hover over charts to see detailed Elo ratings and changes.

## Technical Stack & Learnings
- Python & pandas for data cleaning, manipulation, and calculations.
- Plotly for interactive visualizations including line, bar, and bubble charts.
- Streamlit for building the interactive dashboard with tabs, sliders, and filters.
- Worked with multi-season datasets and applied logic to calculate Elo ratings and single-season gains/losses.
- Learned layout management, interactive widgets, and user-friendly dashboard design.

## Fun Fact
Although Manchester United is considered one of the all-time top Premier League teams, their Elo ratings place them 15th out of 51 teams that have played in the league over the last 32 seasons. Explore the dashboard to discover similar insights for other teams.

## Author
Felix John
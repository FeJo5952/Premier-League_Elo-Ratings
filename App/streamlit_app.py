#Importing necessary libraries
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np

#Reading the necessary CSV files
elo_history_df = pd.read_csv('Data/Processed/Elo-Ratings History.csv')
final_elo_ratings = pd.read_csv('Data/Processed/Updated Elo-Ratings.csv')
elo_gain_df = pd.read_csv('Data/Processed/Elo_gain_per_team.csv')
elo_loss_df = pd.read_csv('Data/Processed/Elo_loss_per_team.csv')
PL_dataframe_processed = pd.read_csv('Data/Processed/Updated PL_Dataframe.csv')


elo_history_df['Date'] = pd.to_datetime(elo_history_df['Date'])

#Creating the visualization tools
def plotly_express_chart_maker_elo_across_seasons(*teams, season):
    teams_elo_history = elo_history_df.loc[(elo_history_df['Team'].isin(teams)) & (elo_history_df['Season'].isin(season))]
    fig = px.line(
        teams_elo_history,
        x = 'Date',
        y = 'Elo-rating after match',
        color = 'Team',
        title = f"Elo Rating History of {', '.join(teams)} for {len(season)} seasons",
        color_discrete_sequence=px.colors.qualitative.Pastel
        )
    return fig

def plotly_line_chart_matchBYmatch(*teams, season):
    required_df = elo_history_df.loc[
        (elo_history_df['Team'].isin(teams)) & (elo_history_df['Season'] == season)].sort_values( by = 'Date')
    fig = px.line(
        required_df,
        x = 'Date',
        y = 'Elo-rating after match',
        title = f"Elo-Ratings of {', '.join(teams)} across the {season} season",
        color = 'Team',
        hover_data = ['Date', 'Elo-rating before match'],
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    return fig

def plotly_bar_chart_max_rating(*teams, season):
    filtered_df = elo_history_df.loc[(elo_history_df['Team'].isin(teams)) & (elo_history_df['Season'] == season)]
    required_df_index_values = filtered_df.groupby(['Season','Team'])['Elo-rating after match'].idxmax()
    required_df = filtered_df.loc[required_df_index_values]
    required_df.sort_values(by = 'Elo-rating after match', ascending = False, inplace = True)
    required_df['Date'] = required_df['Date'].dt.date   

    fig = px.bar(
       required_df,
       x = "Team",
       y = 'Elo-rating after match',
       title = f'Highest Elo-Ratings achieved for {', '.join(teams)} in the {season} season',
       color = 'Team',
       color_discrete_sequence=px.colors.qualitative.Pastel,
       hover_data = ['Date','Season'],
       text = 'Elo-rating after match'
)
    fig.update_yaxes(range = [required_df['Elo-rating after match'].min() - 100, required_df['Elo-rating after match'].max() + 20 ])
    return fig

def elo_difference_across_seasons(*teams, season):
    required_df = elo_history_df.loc[
        (elo_history_df['Team'].isin(teams)) & (elo_history_df['Season'].isin(season))].sort_values( by = 'Date')
    required_df.drop('Full Time Goals', axis =1, inplace = True)
    
    start_rating = required_df.groupby("Team")["Elo-rating before match"].first()
    end_rating = required_df.groupby("Team")['Elo-rating after match'].last()

    elo_difference_df = pd.DataFrame({
        "Start Elo" : start_rating,
        "End Elo" : end_rating
    })
    elo_difference_df['Elo Difference'] = round(elo_difference_df['End Elo'] - elo_difference_df['Start Elo'], 1)
    elo_difference_df['Color'] = elo_difference_df['Elo Difference'].apply(lambda x : 'green' if x >=0  else 'red')
    elo_difference_df['Size'] = elo_difference_df['Elo Difference'].abs()*10
    elo_difference_df['hover_text'] = elo_difference_df.index + "<br> Elo Difference: " + elo_difference_df['Elo Difference'].astype(str)
    elo_difference_df.reset_index(inplace = True)
    fig = px.scatter(
        elo_difference_df,
        x = 'Team',
        y = 'Elo Difference',
        size = 'Size',
        color = 'Color',
        text = 'hover_text',
        title = f"Elo Rating Changes Across {len(season)} Seasons for {', '.join(elo_difference_df['Team'])}",
        color_discrete_map={'green':'green','red':'red'},
        size_max = 100,
        hover_data={'Start Elo': True, 'Team' : False, 'hover_text' : False,
        'End Elo': True, 'Elo Difference': True, 'Color': False, 'Size': False}

    )
    fig.update_layout(showlegend = False)
    fig.update_xaxes(title = "")
    fig.update_yaxes(visible = False)

    return fig
#Sets name of the tab and layout of the webpage
st.set_page_config(page_title = 'Elo ratings Dashboard', layout = 'wide')


#Sidebar for navigation
page = st.sidebar.selectbox(
    'Choose a view:', ('Home', 'Summary', 'Team-wise Elo over time', 'Top/Bottom Performers'))
st.sidebar.markdown('---------')
st.sidebar.info('Use the dropdown option to explore multiple visualizations')



#Adding logic to the entire page
if page == 'Home': 
    # --- Project Title ---
    st.markdown("# ⚽ Premier League Elo-Ratings Dashboard")
    
    # --- Project Description ---
    st.markdown("""
    An interactive analysis of **all Premier League teams from 1992 to 2025**, tracking their performance 
    using the **Elo rating system**.  
    Explore team trends, season-by-season changes, and the league’s best and worst performers.
    """)
    
    # --- Project Context / Motivation ---
    st.markdown("""
    ### Why this project? 
The Premier League is one of the most competitive football leagues in the world. Traditional stats like wins/losses or goal difference do not always capture team strength accurately.**Elo ratings** provide a dynamic way to track team performance across seasons, helping uncover trends, over-performing teams, and under-performing teams.
    
### Why Elo Ratings?
Traditional metrics may not fully capture team performance dynamics. Elo ratings are **adaptive**, updating after each match based on opponent strength and match result.  
This allows you to:
- Identify under- or over-performing teams
- Track performance trends over multiple seasons
- Spot breakout seasons or surprising slumps

    """)
    
    # --- How to use the Dashboard ---
    st.markdown("""
    ### How to use this dashboard
    - Use the **sidebar** to navigate between different sections:
        - Summary  
        - Team-wise Elo trends across multiple seasons  
        - Top/Bottom performers based on Elo ratings 
    - Select teams and seasons from the dropdowns to explore detailed charts and trends.
    
    💡 **Tip:** Use the interactive charts to hover, zoom, and select specific teams or seasons for detailed insights.
                
    """)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""### Overview of the Data """)
    # Key metrics dataframes
    col1, col2, col3 = st.columns(3)
    
    col1.write("Seasons Covered")
    seasons = sorted(list(elo_history_df['Season'].unique()))
    seasons_df = pd.DataFrame(seasons, columns = ['Seasons'], index = range(1,len(seasons) + 1))
    col1.dataframe(seasons_df, height = 310)
    col1.metric("Total Number of Seasons", len(seasons))

    col2.write("Teams Analyzed")
    teams = list(elo_history_df['Team'].unique())
    teams_df = pd.DataFrame(teams, index = range(1, len(teams) + 1), columns = ['Teams'])
    col2.dataframe(teams_df, height = 310)
    col2.metric("Total Number of Teams", len(teams))

    col3.write("Key Metrics Used")
    metrics_df = pd.DataFrame(list(PL_dataframe_processed.columns), columns = ['Metrics'],index = range(1, len(list(PL_dataframe_processed.columns))+ 1))
    col3.dataframe(metrics_df, height = 310)
    col3.metric("Total Number of Metrics Used", len(metrics_df))

    # --- Technical Stack / Learnings ---
    st.markdown("""
    ### 🛠 Technical Stack & Learnings
    - Used Python and pandas to clean, aggregate, and process multi-season Premier League data efficiently.  
    - Built interactive visualizations with Plotly, including line, bar, and bubble charts, customizing colors, hover info, and labels.  
    - Developed a Streamlit dashboard with tabs, sliders, and multi-select filters for dynamic exploration of team performances.  
    - Calculated Elo rating changes, peak ratings, and single-season gains/losses to generate actionable insights.  
    - Learned to combine data processing, visualization, and interactivity into a cohesive, user-friendly interface.  
    - Explored team trends over time, highlighting top performers, underperformers, and interesting historical patterns.
    """)
    
    # --- Fun Fact / Engagement ---
    st.markdown("""
### ⚡ Fun Fact
Did you know? Although Manchester United is considered one of the all-time top Premier League teams, their Elo ratings place them **15th out of the 51 teams** that have played in the league over the last 32 seasons.

Explore the dashboard to discover similar insights for other teams and seasons.
        """)


if page == 'Summary':
    st.markdown('# Summary view of the analysis')
    st.markdown("""
### Overview of Premier League Performance
The Premier League has seen **dramatic shifts in team performance** over the last 32 seasons. 
Elo ratings provide a **dynamic, match-by-match measure of team strength**, going beyond simple win-loss stats.

- Teams that consistently appear near the top of the Elo table are historically strong performers.
- Big swings in Elo ratings highlight seasons where teams either **overperformed** or **struggled** unexpectedly.
- This page allows you to **compare peak performances** across teams and seasons quickly.

""")

    #Calculation of overall ratings and summary metrics
    max_team_rating_df= elo_history_df.loc[elo_history_df.groupby('Team')['Elo-rating after match'].idxmax()]
    max_team_rating_df = max_team_rating_df.drop(['Elo-rating before match', 'Full Time Goals'], axis = 1)
    max_team_rating_df['Date'] = max_team_rating_df['Date'].dt.date
    max_team_rating_df_sorted = max_team_rating_df.sort_values(by = 'Elo-rating after match', ascending = False)
    
    min_team_rating_df = elo_history_df.loc[elo_history_df.groupby('Team')['Elo-rating after match'].idxmin()]
    min_team_rating_df = min_team_rating_df.drop(['Elo-rating before match', 'Full Time Goals'], axis = 1)
    min_team_rating_df['Date'] = min_team_rating_df['Date'].dt.date
    min_team_rating_df_sorted = min_team_rating_df.sort_values(by = 'Elo-rating after match', ascending = True)
 

    #Division of page into 4 columns to write key metrics
    col1, col2 = st.columns(2)
    col1.metric("Max Elo-rating ever achieved", max_team_rating_df_sorted.iloc[0]['Elo-rating after match'])

    col2.metric("Lowest Elo-rating ever achieved", min_team_rating_df_sorted.iloc[0]['Elo-rating after match'])


    st.markdown(f"""
        - 🏆 **{max_team_rating_df_sorted.iloc[0]['Team']}** had the highest Elo-rating ever: **{max_team_rating_df_sorted.iloc[0]['Elo-rating after match']}** ({max_team_rating_df_sorted.iloc[0]['Season']} Season)  
        - ↘️ **{min_team_rating_df_sorted.iloc[0]['Team']}** had the lowest Elo-rating ever: **{min_team_rating_df_sorted.iloc[0]['Elo-rating after match']}** ({min_team_rating_df_sorted.iloc[0]['Season']} Season)  
 
                """)

    st.markdown('<br>', unsafe_allow_html= True)


    st.markdown("""
                ### Highest Elo-ratings ever achieved
                This table displays the highest Elo rating ever achieved by each Premier League team from 1992 to 2025. It gives you a snapshot of which teams historically performed the best according to Elo-ratings. Use the filters below to explore specific teams or seasons in detail.
                """)
    

    st.dataframe(max_team_rating_df_sorted, hide_index = True, height = 270)
    st.markdown("-------")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('''
            ### How to Interpret the Charts
            - Use the **team and season selectors** below to generate bar charts of **peak ratings**.
            - Hover over the bars to see the exact Elo score and the date it was recorded.
            - Comparing multiple teams side by side gives insights into **relative dominance** during a season.

            ### Insights You Can Explore
            - Identify which teams have **historically dominated** the Premier League.
            - Spot teams with **surprising peak performances** in a given season.
            - Observe **trends over time**, for example, how newly promoted teams fared against established clubs.
            - Combine this with the “Team-wise Elo over time” tab to see if peak performances align with **multi-season trends**.

            💡 **Tip:** Use this summary view to quickly identify teams with **the most impressive Elo gains or losses** before diving into match-by-match trends.                
            ''')
    st.markdown("""
                Use the controls below to select specific teams and a season. The bar chart will show the peak Elo ratings for your selected teams during that season, enabling quick visual comparison.
                """)
    selected_teams = st.multiselect(
        'Choose upto 7 teams:', final_elo_ratings['Team'].sort_values(), max_selections = 7,
        key = "team_wise_elo_over_time"
    )
    season = st.selectbox(
            "Choose your preferred season :", options = ["Select a season"] + list(np.sort(elo_history_df['Season'].unique())), index = 0
    )

    if selected_teams and season != 'Select a season':
        st.markdown("""
                The bar chart allows you to visualize the peak Elo ratings for your selected teams in a specific season. This makes it easy to compare team performances and see which teams dominated during that period. Hover over the values in the table to see the exact Elo rating and the date it was achieved.
                """)
        st.plotly_chart(plotly_bar_chart_max_rating(*selected_teams, season = season))


if page == 'Team-wise Elo over time':
    st.markdown('# Elo-ratings across seasons')
    st.write("This section visualizes the Elo-ratings of selected Premier League teams across multiple seasons or a singular season according to the user's preference. Use it to track team performance trends over time, compare teams head-to-head, and identify periods of dominance or decline. Adjust the filters to focus on specific teams or season ranges for a clearer view")
    st.markdown("<br>", unsafe_allow_html=True)

    # Making two tabs for this page
    tab1, tab2 = st.tabs(["📈 Multi-season Trends", "📊 Single-season Trends"])

    with tab1:   
        st.markdown("""
        ### Multi-season Trends
        This tab allows you to **track the Elo ratings of Premier League teams across multiple seasons**.

        - **Adjust the season range** using the slider to focus on a specific period, such as the early 2000s or recent seasons.
        - **Select up to 4 teams** to compare their performance trends side by side.

        The resulting line chart shows how each team's **Elo rating has evolved over time**, highlighting:
        - Periods of dominance or decline for each team.
        - Relative performance when teams face similar challenges across seasons.
        - Long-term trends and consistency in team strength.

        💡 **Tip:** Hover over the lines in the chart to see exact Elo ratings at different points in time.
        """)
        season_years = sorted(int(s.split("-")[0]) for s in elo_history_df['Season'].unique())

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<br>", unsafe_allow_html=True)
            st.write("Adjust the slider to focus on specific seasons - ➡️➡️➡️")
        with col2:
            season_min, season_max = st.slider(
                'Choose your season range:',
                min_value = min(season_years),
                max_value = max(season_years),
                value = (min(season_years), max(season_years)),
                help="Drag to filter the range of seasons shown in the chart"
            )

        seasons_in_range = [s for s in elo_history_df['Season'].unique()
                            if season_min <= int(s.split("-")[0]) <= season_max]
        
        
        selected_teams = st.multiselect(
            'Choose upto 4 teams:', final_elo_ratings['Team'].sort_values(), max_selections = 4,
            key = "team_wise_elo_over_time"
        )
        
        if selected_teams:
            st.write("This chart shows how selected teams' Elo ratings have evolved over time. Use the slider to focus on specific seasons and compare multiple teams performance trends.")
            st.plotly_chart(plotly_express_chart_maker_elo_across_seasons(*selected_teams, season = seasons_in_range))
        
        st.markdown("---")

    with tab2:
        st.markdown("""
                ### Single-season Trends
                This tab lets you **analyze match-by-match Elo ratings for a single season**.

                - **Select a season** from the dropdown.
                - **Choose up to 4 teams** to track their performance during that season.

                The line chart displays:
                - **Peaks and dips** in Elo ratings across matches.
                - Which teams dominated or struggled during the season.
                - Detailed insights into match-level performance trends.

                💡 **Tip:** Use this view to compare team performance **within a season** and identify key moments that impacted their Elo rating.
                """)

        season = st.selectbox(
            'Choose your season:', options = ["Select a season"] + list(np.sort(elo_history_df['Season'].unique())), index = 0
        )
        teams_in_season = elo_history_df.loc[elo_history_df['Season'] == season, 'Team'].sort_values().unique()

        selected_teams = st.multiselect(
            'Choose upto 4 teams:', teams_in_season, max_selections = 4,
            key = "team_wise_elo_per_season"
        )
        
        if selected_teams and season != "Select a season":
            st.write( f"Here’s the match-by-match Elo rating progress for the selected teams in the **{season}** season. "
            "Observe peaks, dips, and performance trends across matches to see which teams dominated or struggled.")
            st.plotly_chart(plotly_line_chart_matchBYmatch(*selected_teams, season = season))
                    
        st.markdown("---")
            

if page == 'Top/Bottom Performers':
    st.markdown('# Elo-ratings for Best/Worst performers')
    st.markdown("""
                ### Overview
                This section focuses on **teams that experienced the most dramatic single-season Elo rating changes** in Premier League history.  
                - **Biggest gain**: Teams that significantly overperformed in a season, climbing the rankings quickly.  
                - **Biggest loss**: Teams that struggled, dropping unexpectedly in Elo rating.  

                By examining these extremes, you can spot **breakout seasons**, **dominance shifts**, and surprising performance patterns.""")
    highest_elo_gain = elo_gain_df.iloc[0]
    highest_elo_loss = elo_loss_df.iloc[0]

    col1, col2 = st.columns(2)

    col1.metric("Highest Elo-rating gain in one season",f"{highest_elo_gain['Elo-difference']}" )
    col2.metric("Highest Elo-rating loss in one season", f"{highest_elo_loss['Elo-difference']}" )
    st.markdown(f'''
                - 📈 **{highest_elo_gain['Team']}** had the biggest single-season gain:  **{highest_elo_gain['Elo-difference']}** ({highest_elo_gain['Season']} Season)  
                - 📉 **{highest_elo_loss['Team']}** had the biggest single-season loss: **{highest_elo_loss['Elo-difference']}** ({highest_elo_loss['Season']} Season)
                        ''')

    st.markdown("""
                ### How to Use This Page
                1. **Metrics at the top** show the single-season records for Elo gain and loss across all seasons.  
                2. **Slider** allows you to focus on specific season ranges.  
                3. **Team selection** lets you compare multiple teams’ performance trends side-by-side.  
                4. The **bubble chart** displays Elo rating changes across the selected seasons:  
                - **Green bubbles** = positive Elo changes (gains)  
                - **Red bubbles** = negative Elo changes (losses)  
                - **Bubble size** reflects the magnitude of change  
                """)

    
    season_years = sorted(int(s.split("-")[0]) for s in elo_history_df['Season'].unique())
    st.write("""
### Compare Multiple Teams
Select teams and a range of seasons below to visualize **Elo rating changes** across seasons. 
Positive changes are shown in green, negative changes in red. Bubble size reflects magnitude of gain/loss.
""")
    col1, col2 = st.columns(2)
    with col1:
            st.markdown("<br>", unsafe_allow_html=True)
            st.write("Adjust the sldier to focus on specific seasons - ➡️➡️➡️")
    with col2:
            season_min, season_max = st.slider(
                'Choose your season range:',
                min_value = min(season_years),
                max_value = max(season_years),
                value = (min(season_years), max(season_years)),
                help="Drag to filter the range of seasons shown in the chart"
            )
    
    seasons_in_range = [s for s in elo_history_df['Season'].unique()
                            if season_min <= int(s.split("-")[0]) <= season_max]
    selected_teams = st.multiselect(
            'Choose upto 4 teams:', final_elo_ratings['Team'].sort_values(), max_selections = 7,
            key = "team_wise_elo_change"
        )
        
    if selected_teams:
            st.write("This chart shows how selected teams' Elo ratings have evolved over time. Use the slider to focus on specific seasons and compare multiple teams performance trends.")
            st.plotly_chart(elo_difference_across_seasons(*selected_teams, season = seasons_in_range))
    st.markdown("""
                ### Insights You Can Explore
                - Compare **historically strong teams** versus **new or underperforming teams**.  
                - Identify seasons where a team had **unexpected success or failure**.
                - Track **performance volatility** across multiple seasons.  
                💡 **Tip:** Hover over bubbles in the chart to see the exact Elo difference and start/end ratings for each team. This helps you quickly spot **major shifts in team strength** over time.
                """)

    st.markdown("---")

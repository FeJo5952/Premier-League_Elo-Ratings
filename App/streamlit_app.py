#Importing necessary libraries
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px

#Reading the necessary CSV files
elo_history_df = pd.read_csv('../Data/Processed/Elo-Ratings History.csv')
final_elo_ratings = pd.read_csv('../Data/Processed/Updated Elo-Ratings.csv')
elo_gain_loss_df = pd.read_csv('../Data/Processed/Elo_gain-loss_per_team.csv')

#Creating the visualization tools
def plotly_express_chart_maker_elo_across_seasons(*teams):
    if len(teams) >=5:
        st.error("Too many teams to visualize clearly. Try 4 teams or fewer")
        return

    else:
        teams_elo_history = elo_history_df.loc[elo_history_df['Team'].isin(teams)]
        fig = px.line(
            teams_elo_history,
            x = 'Date',
            y = 'Elo-rating after match',
            color = 'Team',
            title = f"Elo Rating History of {', '.join(teams)}"
        )
        return fig

#Sets name of the tab and layout of the webpage
st.set_page_config(page_title = 'Elo ratings Dashboard', layout = 'wide')

#Basic writing on the webpage
st.title('Elo Ratings Dashboard')
st.write('Welcome to my interactive dashboard for Premier League Ratings')

#Sidebar for navigation
page = st.sidebar.selectbox(
    'Choose a view:', ('Summary', 'Team-wise Elo over time', 'Match by Match Elo Ratings', 'Top/Bottom Performers'))
st.sidebar.markdown('---------')
st.sidebar.info('Use the dropdown option to explore multiple visualizations')

#Adding logic to each page
if page == 'Summary':
    st.subheader('Summary view of the analysis')
    st.write("Basic overview stats and visualizations")
elif page == 'Team-wise Elo over time':
    st.subheader('Elo-ratings across multiple seasons')
    st.write('Below is the progress of Elo-ratings for the specified teams across multiple seasons')

    selected_teams = st.multiselect(
        'Choose upto 4 teams:', final_elo_ratings['Team'].sort_values(), max_selections = 4
    )
    if selected_teams:
        st.plotly_chart(plotly_express_chart_maker_elo_across_seasons(*selected_teams))

elif page == 'Match by Match Elo Ratings':
    st.subheader('Elo-ratings across a single season')
    st.write('Below given are the progress of Elo-ratings for the specified teams across a single seasons')
else:
    st.subheader('Elo-ratings for Best/Worst performers')
    st.write('Below given are the Elo-ratings of the best and worst performing teams')
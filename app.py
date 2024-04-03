# import dependencies

from dash import Dash, html, dcc
from dash.dependencies import Input, Output  # Make sure to import Input and Output
import pandas as pd
import plotly.express as px
messi_goals_df = pd.read_csv('data1.csv')
messi_goals_df.drop('Playing_Position', axis=1, inplace=True)
messi_goals_df.drop('Matchday', axis=1, inplace=True)
messi_goals_df.drop('Date', axis=1, inplace=True)
messi_goals_df.drop('Venue', axis=1, inplace=True)
messi_goals_df.drop('At_score', axis=1, inplace=True)
messi_goals_df.drop('Result', axis=1, inplace=True)
messi_goals_df['Season'] = messi_goals_df['Season'].astype('string')
messi_goals_df['Competition'] = messi_goals_df['Competition'].astype('string')
messi_goals_df['Club'] = messi_goals_df['Club'].astype('string')
messi_goals_df['Type'] = messi_goals_df['Type'].astype('string')
messi_goals_df['Goal_assist'] = messi_goals_df['Goal_assist'].astype('string')
messi_goals_df['Opponent'] = messi_goals_df['Opponent'].astype('string')
messi_goals_df['Minute'] = messi_goals_df['Minute'].astype('string')
messi_goals_df.head()

def count_unique_dates(df, date_column_name):
    df[date_column_name] = pd.to_datetime(df[date_column_name])

    # Count the number of unique dates
    unique_date_count = df[date_column_name].nunique()

    return unique_date_count

def get_goals_by_season(df, season):
    return df[df['Season'] == season]

def get_goals_by_season_dict(df):
    # Initialize an empty dictionary to store the number of goals per season
    goals_per_season = {}

    # List of seasons from "04/05" to "22/23"
    seasons = [f"{y:02d}/{(y+1)%100:02d}" for y in range(4, 23)]

    # Loop through each season, get the goal count, and store it in the dictionary
    for season in seasons:
        goals_per_season[season] = len(df[df['Season'] == season])

    return goals_per_season


def get_goals_by_type(df):
    goals_by_type_series = df['Type'].value_counts()
    
    # Convert the Series to a dictionary
    goals_by_type_dict = goals_by_type_series.to_dict()
    
    # Calculate the total number of goals by summing the values in the dictionary
    total_goals = sum(goals_by_type_dict.values())
    
    # Add the total number of goals to the dictionary
    goals_by_type_dict['total'] = total_goals
    
    return goals_by_type_dict

app = Dash(__name__)
server = app.server  # Expose the server variable for Heroku
goals_by_season = get_goals_by_season_dict(messi_goals_df)
goals_by_type = get_goals_by_type(messi_goals_df)
unique_goal_types = list(goals_by_type.keys())
seasons = [f"{y:02d}/{(y+1)%100:02d}" for y in range(4, 23)]
season_indices = list(range(len(seasons)))
marks = {i: season for i, season in zip(season_indices, seasons)}

app.layout = html.Div(children=[
    html.Img(src='assets/images/messi_smile.png', className='messi-image'),
    html.Img(src='assets/images/BarcaLogo.png', style={'position': 'absolute', 'top': '0', 'left': '0', 'width': '100px', 'height': '100px', 'padding': '30px', 'margin-left':'35   px'}),
    html.H1('The GOAT - Leo Messi in Numbers', className='header'), #html elements to format the app
    html.H3('A statistical analysis of his career club goals', className='subheader'), #html elements to format the app
     html.Div(className='content-container', children=[
             html.Div(className='stats'
             , children=[
                 html.H2('Messi\'s Career Stats', style={'color': 'white'}),
                 html.H3('Total Goals: 854', style={'color': 'white'}),
                 html.H3('Total Assists: 361', style={'color': 'white'}),
                 html.H3('Total Appearances: 1107', style={'color': 'white'}),
                 html.H3('4 Champions Leagues', style={'color': 'white'}),
                 html.H3('10 La Liga Titles', style={'color': 'white'}),
                 html.H3('7 Copa Del Rey', style={'color': 'white'}),
                 html.H3('World Cup Winner', style={'color': 'white'}),
                 html.A('For More information, press me!', href='https://en.wikipedia.org/wiki/Lionel_Messi', style={'color': 'white'},target='_blank',className='last-element'),
                 html.H5('(True to 4/2/24)', style={'color': 'white'}),

             ],     
    ),
 html.Div(className='graph-container', children=[
    dcc.Graph(id='goals-graph', className='graph'),  # Placeholder for the graph
    html.Div(className='controls-container', children=[
        html.Div(className='slider-container', children=[
            html.H4('Select Seasons:', className='slider-text'),
            dcc.RangeSlider(
                className='slider',
                id='season-range-slider',
                min=season_indices[0],
                max=season_indices[-1],
                step=1,
                marks=marks,
                value=[season_indices[0], season_indices[-1]],  # Default to full range
            )
        ]),
        html.Div(className='dropdown-container', children=[
            html.H4('Select Type:', className='dropdown-text'),
            dcc.Dropdown(
                className='dropdown',
                id='goaltype-dropdown',
                options=[{'label': goal_type, 'value': goal_type} for goal_type in unique_goal_types],
                value='total',  # Default value set to 'total'
                multi=True  # Allow multiple selections
            )
        ])
         ])
          ]),
]   
             ),
        html.H5('All data is true to 3/4/23 unless states otherwise.', className='subheader', style={'margin-top': '2px'}),
], style={'background': 'linear-gradient(to bottom, #211d9e, #a83250)'})

@app.callback(
    Output('goals-graph', 'figure'),
    [Input('season-range-slider', 'value'),
     Input('goaltype-dropdown', 'value')]
)
def update_graph(selected_season_range, selected_goal_types):
    # Check if no goal types are selected
    if not selected_goal_types:
        # Return a blank figure
        return px.line(title='Select goal types to view data')

    start_season_index, end_season_index = selected_season_range
    selected_seasons = seasons[start_season_index:end_season_index + 1]
    
    filtered_df = messi_goals_df[messi_goals_df['Season'].isin(selected_seasons)]

    # Initialize an empty DataFrame for the final data
    df_final = pd.DataFrame()

    # Process 'total' separately to ensure it gets included when selected
    if 'total' in selected_goal_types:
        df_agg = filtered_df.groupby('Season').size().reset_index(name='Goals')
        df_agg['Type'] = 'Total'
        df_final = pd.concat([df_final, df_agg])

    # Process other goal types
    for goal_type in selected_goal_types:
        if goal_type != 'total':  # Exclude 'total' since it's already processed
            df_filtered = filtered_df[filtered_df['Type'] == goal_type]
            df_agg = df_filtered.groupby('Season').size().reset_index(name='Goals')
            df_agg['Type'] = goal_type
            df_final = pd.concat([df_final, df_agg])

    # Generate the figure using Plotly Express line chart
    fig = px.line(df_final, x='Season', y='Goals', color='Type', title='Goals for Club by Type and Season', markers=True)
    fig.update_layout(xaxis_title='Season', yaxis_title='Number of Goals', xaxis={'type': 'category'})

    return fig


if __name__ == '__main__': #run the app
    app.run_server(debug=True)

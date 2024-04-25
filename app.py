# import dependencies

from dash import Dash, html, dcc
from dash.dependencies import Input, Output  # Make sure to import Input and Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

barca_staff = pd.read_csv('data/data.csv')
barca_staff=barca_staff.drop_duplicates(subset=['full_name'], keep='first')
country_counts = barca_staff['country'].value_counts().reset_index()
country_counts.columns = ['country', 'count']
unique_positions = barca_staff['position'].unique().tolist()


# New list to hold positions excluding 'Manager'
filtered_positions = []
for position in unique_positions:
    if position != 'Manager' and position != 'Ass. Manager' and position != 'Goalkeeping Coach' and position!='Game Analyst' and position!='Athletic Coach':
        filtered_positions.append(position)

# Assign the filtered list back to unique_positions if necessary
unique_positions = filtered_positions





messi_goals_df = pd.read_csv('data/data1.csv')
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
messi_goals_df['Competition'] = messi_goals_df['Competition'].replace({'Champions League': 'UEFA Champions League'})
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

map_fig = px.choropleth(
    country_counts,
    locations="country",
    locationmode='country names',
    color="count",
    color_continuous_scale=px.colors.sequential.Plasma,
    labels={'count':'Number of Players'}
)

# Update the layout to add more visual context
map_fig.update_layout(
    title_text='Global Distribution of FC Barcelona Players',
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    )
)
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
                ,style={'margin-bottom': '10px'}
            )
        ])
         ])
          ]),
]  
),
    html.Div(className='histogram-container', children=[
    html.H2('Generational Talent - Why are Messi\'s Numbers Superhuman?', className='histogram-header1'),         
    html.H3('Lionel Messi’s career goal distribution reveals the patterns and peaks of a legendary footballer\'s scoring record. Throughout his illustrious career, Messi has shown remarkable consistency, scoring 672 goals in 778 appearances for FC Barcelona alone. See the above graph to check how those goals were spread throughout the years! Analyzing his goal distribution, it’s evident that Messi has a knack for scoring in crucial late-game moments, with a significant number of goals coming in the final 15 minutes of matches. His goal distribution across competitions is equally impressive: he has netted over 120 UEFA Champions League goals, showcasing his prowess on the biggest stage. At the club level, his contributions helped Barcelona secure numerous titles across La Liga, Copa Del Rey, and international tournaments, illustrating his critical role in the team\'s success during his tenure.'
    ,className='histogram-text1'),
         html.H2('Goal Distribution Over Minutes by Club and Competition', className='histogram-header'),
        dcc.Graph(id='goal-distribution-chart' ),  # Placeholder for the histogram
      html.Div(className='histogram-controls-container', children=[
    html.H4('Select Clubs:', className='histogram-text'),
    dcc.Checklist(
        id='club-selector',
        options=[
            {'label': 'FC Barcelona', 'value': 'FC Barcelona'},
            {'label': 'Paris Saint-Germain', 'value': 'Paris Saint-Germain'}
        ],
        value=['FC Barcelona'],  # Default selected value
        labelStyle={'display': 'block'}
    ),
    dcc.Dropdown(
        id='competition-selector',
        className='dropdown',
        options=[{'label': comp, 'value': comp} for comp in messi_goals_df['Competition'].unique()],
        value=messi_goals_df['Competition'].unique()[0],  # Default selected value
    )
])

        ]),
        html.Div(className='map-container', children=[
            
            html.H3('Lionel Messi\'s journey to becoming a football legend began when he moved from his native Argentina to Barcelona at just 13 years old. Joining FC Barcelona\'s famed youth academy, La Masia, he quickly stood out as an extraordinary talent. La Masia is renowned for its rigorous training regime and a strong emphasis on technical skills, which perfectly suited Messi\'s natural abilities and playing style. Unlike many of his peers, Messi\'s progression through the ranks was meteoric, marked by a combination of innate skill and an unyielding dedication to improving his game. What makes Messi\'s rise to the top particularly notable is the context of his success; as a non-Spanish player in a club that has historically been dominated by home-grown talents, Messi\'s ascent within FC Barcelona highlights both his exceptional ability and the inclusive philosophy of the club, which values talent over nationality(See the below graph for the distribution of FC Barcelona players by country). His journey from a young talent at La Masia to becoming one of the greatest players of all time is not just a testament to his individual prowess but also to Barcelona\'s commitment to nurturing diverse talent.', className='map-p'),
               dcc.Graph(id='player-distribution-map', className='map'),
    html.Div(className='map-controls-container', children=[
            html.H4('Select Positions:', className='histogram-text'),
    dcc.Dropdown(
        id='position-dropdown',
        options=[{'label': pos, 'value': pos} for pos in unique_positions],
        value=unique_positions,  # Default to all positions selected
        multi=True,  # Allow multiple selections
        className='map-dropdown'
    ),]),

            
        ])
,
        html.H5('All data is true to 3/4/23 unless stated otherwise.', className='subheader', style={'margin-top': '120px'}),
        html.A('GitHub Link!', href='https://github.com/dorfrechter/final-project-ds4003', style={'color': 'white'},target='_blank',className='last-element'),
        

], style={'background': 'linear-gradient(to bottom, #211d9e, #a83250)'})



# Callback to update the map based on selected positions
@app.callback(
    Output('player-distribution-map', 'figure'),
    [Input('position-dropdown', 'value')]
)
def update_map(selected_positions):
    # Filter the dataframe based on selected positions
    filtered_df = barca_staff[barca_staff['position'].isin(selected_positions)]
    country_counts = filtered_df['country'].value_counts().reset_index()
    country_counts.columns = ['country', 'count']

    # Create the map graph using Plotly Express
    fig = px.choropleth(
        country_counts,
        locations="country",
        locationmode='country names',
        color="count",
        color_continuous_scale=px.colors.sequential.Plasma,
        labels={'count': 'Number of Players'}
    )

    # Update layout to add more visual context
    fig.update_layout(
        title_text='Global Distribution of FC Barcelona Players by Selected Positions',
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular',
        ),
        paper_bgcolor='#F0F2F6',  
        plot_bgcolor='rgba(0,0,0,0)' 
    )
    return fig








@app.callback(
    Output('goal-distribution-chart', 'figure'),
    [Input('club-selector', 'value'),
     Input('competition-selector', 'value')]
)
def update_histogram(selected_clubs, selected_competition):
    # Filter the data for the selected competition and clubs
    df_filtered = messi_goals_df[
        (messi_goals_df['Club'].isin(selected_clubs)) & 
        (messi_goals_df['Competition'] == selected_competition)
    ]

    # Define bins and labels for the minute intervals
    bins = list(range(0, 91, 5))
    labels = [f'{i}-{i+4}' for i in range(0, 90, 5)]
    df_filtered['Minute Group'] = pd.cut(df_filtered['Minute'].astype(int), bins=bins, right=False, labels=labels)

    # Ensure categories (bins) are in the desired order
    category_orders = {'Minute Group': labels}

    # Create the histogram using Plotly Express
    fig = px.histogram(
        df_filtered, 
        x='Minute Group', 
        color='Club',  # Automatically assigns different colors
        barmode='overlay',
        nbins=len(bins)-1,
        category_orders=category_orders  # Ensuring ordered categories
    )
    
    # Update layout
    fig.update_layout(
        xaxis_title="Game Minute",
        yaxis_title="Number of Goals",
        plot_bgcolor='rgba(0,0,0,0)',  
        paper_bgcolor='#F0F2F6',
    )
    
    
    return fig


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

    # Create a mapping for seasons to ensure order
    season_mapping = {season: i for i, season in enumerate(seasons)}

    # Process 'total' separately to ensure it gets included when selected
    if 'total' in selected_goal_types:
        df_agg = filtered_df.groupby('Season').size().reset_index(name='Goals')
        df_agg['Type'] = 'Total'
        # Map the seasons to their respective order
        df_agg['Season_Order'] = df_agg['Season'].map(season_mapping)
        df_final = pd.concat([df_final, df_agg])

    # Process other goal types
    for goal_type in selected_goal_types:
        if goal_type != 'total': 
            df_filtered = filtered_df[filtered_df['Type'] == goal_type]
            df_agg = df_filtered.groupby('Season').size().reset_index(name='Goals')
            df_agg['Type'] = goal_type

            df_agg['Season_Order'] = df_agg['Season'].map(season_mapping)
            df_final = pd.concat([df_final, df_agg])
    df_final = df_final.sort_values(by=['Season_Order', 'Type'])

    # Generate the figure using Plotly Express line chart
    fig = px.line(df_final, x='Season', y='Goals', color='Type', title='Goals for Club by Type and Season', markers=True)

    # Update layout for x-axis and y-axis
    fig.update_layout(
        xaxis_title='Season',
        yaxis_title='Number of Goals',
        xaxis={'type': 'category', 'categoryorder': 'array', 'categoryarray': seasons},
        plot_bgcolor='rgba(0,0,0,0)',  
        paper_bgcolor='#F0F2F6',  
        margin=dict(t=60, b=60, l=60, r=60), 
        template={
            'layout': {
                'paper_bgcolor': '#F0F2F6',
                'plot_bgcolor': 'rgba(0,0,0,0)',
                'autosize': True,
                'font': {'color': '#333'},  
                'margin': {'t': 10, 'r': 10, 'b': 10, 'l': 10}, 
            }
        }
    )
    return fig


if __name__ == '__main__': #run the app
    #app.run_server(debug=True)
    app.run(jupyter_mode='tab', debug=True)

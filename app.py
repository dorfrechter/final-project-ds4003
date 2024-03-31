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


app = Dash(__name__)
server = app.server  # Expose the server variable for Heroku

app.layout = html.Div([
    html.H1('GDP Per Capita Over Time', className='header'), #html elements to format the app
])


if __name__ == '__main__': #run the app
    app.run_server(debug=True)

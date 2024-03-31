# import dependencies

from dash import Dash, html, dcc
from dash.dependencies import Input, Output  # Make sure to import Input and Output
import pandas as pd
import plotly.express as px

#get dataset
df = pd.read_csv('gdp_pcap.csv')
def convert_k_to_number(value):
    if isinstance(value, str) and value.lower().endswith('k'):
        # Remove the 'k' and convert to float, then multiply by 1,000
        return float(value[:-1]) * 1000
    else:
        # If the value doesn't end with 'k', return it as-is (or convert to numeric if necessary)
        return float(value)
    

for column in df.columns[1:]:
    df[column] = df[column].apply(convert_k_to_number)

yearList= []
unique_countries = df['country'].unique()
for i in range(1800,2101): #get a list of all the years
    yearList.append(i)


def getBounds():
    first_row = df.iloc[0]
    counter =0
    min=100000
    max=0
    for value in first_row.items():
        if(counter!=0):
            value= int(value[0])
            if(value > max):
                max = value
            if(value < min):
                min = value
        counter+=1
    return [min,max]


app = Dash(__name__)
server = app.server  # Expose the server variable for Heroku

bounds = getBounds()
app.layout = html.Div([
    html.Link(rel="stylesheet", href='styles/main.css'),
    html.H1('GDP Per Capita Over Time', className='header'), #html elements to format the app
    html.H3('My first Dash app!', className='subheader'),
    html.P('This dash app provides a neat way to represent the change in GDP per capita over the course of many years. The user has the option to select the countries and the years they want to see. The graph will update accordingly. The user can also highlight the sections he is interested in within the graph and the sizing of the graph will adjust accordingly. This is my first dash app and I am excited to see it in work!'),
    html.H4('Select Countries:',className='controls-title'),
    html.H4('Select Years:' ,className='controls-title'),
    html.Div( className='controls-container',
        children = [
        dcc.Dropdown(
            className='dropdown',
            id='country-dropdown',
            options=[{'label': country, 'value': country} for country in unique_countries],
        value=[unique_countries[0]],  # Default value
        multi=True  # Allow multiple selections
            )
    ,
      dcc.RangeSlider(
          className='slider',
        id = 'year-range-slider',
        min = bounds[0], 
        max = bounds[1], 
        step = 1,
        marks=None,
        value = [bounds[0]+100,bounds[1]-100], #default
            tooltip={
        "always_visible": True,
    } #format the slider so we can see the values and it looks clean
      ),
      ]),
    dcc.Graph(id='gdp-percap-graph', className='graph')  # Placeholder for the graph
])

@app.callback(
  Output('gdp-percap-graph', 'figure'),
    [Input('country-dropdown', 'value'), #upate the graph as the output based on the inputs of the id's i specified earlier for the drop down and the range slider.
     Input('year-range-slider', 'value')]
)
def update_graph(selected_countries, selected_years):
    filtered_df = df[df['country'].isin(selected_countries)] #filter the data based on the selected countries 
    selected_columns = ['country'] + [str(year) for year in range(selected_years[0], selected_years[1] + 1)] #select the columns based on the selected years
    filtered_df = filtered_df[selected_columns] #filter the data based on the selected columns

    melted_df = filtered_df.melt(id_vars=['country'], var_name='year', value_name='gdpPercap') #melt the data so we can use it in the graph

    fig = px.line(melted_df, x='year', y='gdpPercap', color='country', title='GDP Per Capita Over Time',
                  labels={'gdpPercap': 'GDP per Capita', 'year': 'Year', 'country': 'Country'}) #create the graph
    
    fig.update_xaxes(
        title="Year",  
        type='linear',  
        nticks=20, 
        range=[str(selected_years[0]), str(selected_years[1])]   # Update x-axis
    )
    # Update y-axis
    fig.update_yaxes(
        title="GDP per Capita", 
        type='linear', 
        tickmode='auto', 
        autorange=True  )
    return fig



if __name__ == '__main__': #run the app
    app.run_server(debug=True)

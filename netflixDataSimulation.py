import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np

# Load your dataset here
file_path = './netflixMostWatchedDataset.csv'
data = pd.read_csv(file_path)
data['votes'] = data['votes'].str.replace(',', '').astype(int)  # Clean and convert votes to int

# Initialize the Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("Netflix \"Shows\" Ratings Visualization"),
    dcc.Graph(id='ratings-bar-chart'),
    html.Label("Select Number of Shows:"),
    dcc.Slider(
        id='number-shows-slider',
        min=0,
        max=len(data),
        value=10,
        step=1,
        marks={i: str(i) for i in range(0, len(data) + 1, 10)},
        tooltip={"placement": "bottom", "always_visible": True}
    ),
    dcc.Interval(
        id='interval-component',
        interval=1*1000,  # 1000 is in milliseconds that is 1 second
        n_intervals=1
    )
])

# Callback to update the graph based on number of shows selected and to simulate real-time data
@app.callback(
    Output('ratings-bar-chart', 'figure'),
    [Input('number-shows-slider', 'value'),
     Input('interval-component', 'n_intervals')]
)
def update_chart(number_of_shows, n_intervals):
    # Simulate 'real-time' votes coming in for the shows
    if n_intervals > 0:
        random_show_index = np.random.randint(0, len(data))
        data.at[random_show_index, 'votes'] += np.random.randint(1, 10)
    
    # Sort data by votes and get the top shows
    sorted_data = data.sort_values('votes', ascending=False).head(number_of_shows)
    
    fig = px.bar(sorted_data, x='lister-item-header', y='votes', title='Top Netflix Shows by Votes')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

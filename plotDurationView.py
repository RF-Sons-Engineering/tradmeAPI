# Import necessary libraries
import dash
from dash import html, dcc, Input, Output, callback
import plotly.express as px
import pandas as pd
import webbrowser

df = pd.read_json('Audi_Q5_2024-01-30.json')
df['ViewsDay'] = df['ViewCount']/df['Duration']

# Create a scatter plot
fig = px.scatter(df, x='Odometer', y='Value', size='ViewsDay', title='Scatter Plot', custom_data='ListingId', color='IsDealer')


# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    dcc.Graph(id='scatter-plot', figure=fig),
    html.Pre(id='click-data')
])

# Define callback for handling click event
@app.callback(
    Output('click-data', 'children'),
    Input('scatter-plot', 'clickData')
)
def display_click_data(clickData):
    if clickData is None:
        return 'Click on a point'
    else:
        url = 'https://www.trademe.co.nz/a/motors/cars/' + str(clickData['points'][0]['customdata'][0])
        webbrowser.open_new_tab(url)


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
# callbacks.py
import dash
from dash.dependencies import Input, Output, State, ALL
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import json
import webbrowser
import pandas as pd
from getCarListings import getCarsJson, manipulate_json
from piecewise_predict import generate_predict_line

def register_callbacks(app, make, model):

    # Search for data
    @app.callback(
        Output('memory', 'data'),
        [Input('get-data-button', 'n_clicks')]
    )
    def search_data(n_clicks):

        search_string = ''
        # Call Trademe API and get data
        cars_json = getCarsJson(make, model, search_string)

        # Manipulate data
        clean_cars_json = manipulate_json(cars_json)

        return clean_cars_json


    # Define slider IDs and properties
    slider_ids = ['year-slider', 'odometer-slider', 'year-slider-2', 'odometer-slider-2']
    properties = ['max', 'min', 'value']

    # Create Output objects using a loop
    outputs = [Output(f'{slider_id}', prop) for slider_id in slider_ids for prop in properties]

    # Callback for setting max and min of sliders
    @app.callback(
        outputs,
        [Input('memory', 'data')]
    )
    def set_slider_ranges(data):

        if len(data) == 0:
            return dash.no_update
    
        df = pd.DataFrame(data)

        max_year = df['Year'].max()
        min_year = df['Year'].min()
        max_odometer = df['Odometer'].max()
        min_odometer = df['Odometer'].min()

        return (
            max_year, min_year, [min_year, max_year], 
            max_odometer, min_odometer, [min_odometer, max_odometer], 
            max_year, min_year, [min_year, max_year], 
            max_odometer, min_odometer, [min_odometer, max_odometer]
        )

    # Callback for updating year-value-graph
    @app.callback(
        Output('year-value-graph', 'figure'),
        [Input('memory', 'data'),
        Input('year-slider', 'value'),
        Input('odometer-slider', 'value'),
        Input({'type': 'year-button', 'index': ALL}, 'n_clicks'),
        Input('submit_button', 'n_clicks')],
        [State('input_year', 'value'),
         State('input_value', 'value')]
    )
    def update_year_graph(data, year_range, odometer_range, n_clicks, submit_n_clicks, input_year, input_value):
        
        if len(data) == 0:
            return dash.no_update
        
        df = pd.DataFrame(data)

        # Drop NA values from Value column
        df = df.dropna(subset=['Value'])

        # Filter based on year, and odometer
        filter_1 = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]
        filtered_df = filter_1[(filter_1['Odometer'] >= odometer_range[0]) & (filter_1['Odometer'] <= odometer_range[1])]


        # Get the latest triggered callbacks
        ctx = dash.callback_context
        
        # Set the main legend
        button_id = 'MainColour'

        # Check which button (if any) has been clicked
        for prop in ctx.triggered:
            if 'n_clicks' in prop['prop_id'] and 'submit_button' not in prop['prop_id']:
                clicked_button = prop['prop_id'].split(".")[0]
                parsed_id = json.loads(clicked_button)['index']
                button_id = parsed_id

        filtered_df[button_id] = filtered_df[button_id].astype(str)

        # Plotting
        fig = px.scatter(filtered_df, x='Year', y='Value', color=button_id, custom_data='ListingId')
        fig.update_xaxes(autorange="reversed")


        # Check if the required inputs are filled
        if input_value and input_year:

            # Calculate values for plotting
            min_value, max_value = min(filtered_df['Value'].min(), input_value), max(filtered_df['Value'].max(), input_value)
            min_year, max_year = min(filtered_df['Year'].min(), input_year), max(filtered_df['Year'].max(), input_year)

            fig.add_trace(go.Scatter(
                x=[input_year, input_year], 
                y=[min_value, max_value], 
                mode='lines', 
                line=dict(color='red', dash='dash'),  # Setting line color to red and dash style
                name='CAR 1'
            ))

            fig.add_trace(go.Scatter(
                x=[min_year, max_year], 
                y=[input_value, input_value], 
                mode='lines', 
                line=dict(color='red', dash='dash'),  # Setting line color to red and dash style
                showlegend=False
            ))

        return fig

    # Callback for updating odometer-value-graph
    @app.callback(
        Output('odometer-value-graph', 'figure'),
        [Input('memory', 'data'),
        Input('year-slider-2', 'value'),
        Input('odometer-slider-2', 'value'),
        Input({'type': 'odometer-button', 'index': ALL}, 'n_clicks'),
        Input('submit_button', 'n_clicks')],
        [State('input_odometer', 'value'),
         State('input_value', 'value')]
    )
    def update_odometer_graph(data, year, odometer, n_clicks, submit_n_clicks, input_odometer, input_value):

        if len(data) == 0:
            return dash.no_update

        df = pd.DataFrame(data)

        # Drop NA values from Value column
        df = df.dropna(subset=['Value'])

        # Filter based on make, model, year, and odometer
        filter_1 = df[(df['Year'] >= year[0]) & (df['Year'] <= year[1])]
        filtered_df = filter_1[(filter_1['Odometer'] >= odometer[0]) & (filter_1['Odometer'] <= odometer[1])]

        # Calculate prediction line
        filtered_df = generate_predict_line(filtered_df)

        # Get the latest triggered callbacks
        ctx = dash.callback_context

        # Set the main legend
        button_id = 'MainColour'

        # Check which button (if any) has been clicked
        for prop in ctx.triggered:
            if 'n_clicks' in prop['prop_id'] and 'submit_button' not in prop['prop_id']:
                clicked_button = prop['prop_id'].split(".")[0]
                parsed_id = json.loads(clicked_button)['index']
                button_id = parsed_id

        filtered_df[button_id] = filtered_df[button_id].astype(str)

        # Plotting
        fig1 = px.scatter(filtered_df, x='Odometer', y='Value', color=button_id, custom_data='ListingId')

       # Check if the required inputs are filled
        if input_value and input_odometer:

            # Calculate values for plotting
            min_value, max_value = min(filtered_df['Value'].min(), input_value), max(filtered_df['Value'].max(), input_value)
            min_odometer, max_odometer = min(filtered_df['Odometer'].min(), input_odometer), max(filtered_df['Odometer'].max(), input_odometer)

            fig1.add_trace(go.Scatter(
                x=[input_odometer, input_odometer], 
                y=[min_value, max_value], 
                mode='lines', 
                line=dict(color='red', dash='dash'),  # Setting line color to red and dash style
                name='CAR 1'
            ))

            fig1.add_trace(go.Scatter(
                x=[min_odometer, max_odometer], 
                y=[input_value, input_value], 
                mode='lines', 
                line=dict(color='red', dash='dash'),  # Setting line color to red and dash style
                showlegend=False
            ))


        # Calculate line of best fit
        fig1.add_trace(go.Scatter(x=filtered_df['Odometer'], y=filtered_df['Predicted'], mode='lines', name='Piecewise Model'))

        return fig1
    
    # Open new tab on year-graph
    @app.callback(
        Output('year-link', 'href'),
        [Input('year-value-graph', 'clickData')],
        prevent_initial_call=True
    )
    def open_link(clickData):
        if clickData is None:
            raise dash.exceptions.PreventUpdate

        url = 'https://www.trademe.co.nz/a/motors/cars/' + str(clickData['points'][0]['customdata'][0])

        webbrowser.open_new_tab(url)

        return None
        

    # Open new tab on odometer graph
    @app.callback(
        Output('odometer-link', 'href'),
        [Input('odometer-value-graph', 'clickData')],
        prevent_initial_call=True
    )
    def open_link(clickData):
        if clickData is None:
            raise dash.exceptions.PreventUpdate

        url = 'https://www.trademe.co.nz/a/motors/cars/' + str(clickData['points'][0]['customdata'][0])

        webbrowser.open_new_tab(url)

        return None
    
        
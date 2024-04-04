# callbacks.py
import dash
from dash.dependencies import Input, Output, State, ALL
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import json
import webbrowser
import requests
import pandas as pd
from getCarListings import getCarsJson, manipulate_json
from piecewise_predict import generate_predict_line
from loess_predict import generate_loess_predictions
# from calculateOutliers import calculateOutliers

def register_callbacks(app, makes_models):

    # Set the dropdown menus
    @app.callback(
        Output('model-dropdown', 'options'),
        Input('make-dropdown', 'value')
    )
    def set_model_options(selected_make):
        if selected_make is not None:
            return [{'label': model, 'value': model} for model in makes_models[selected_make]]
        return []
    
    # Search for data
    @app.callback(
        Output('memory', 'data'),
        [Input('get-data-button', 'n_clicks'),
         State('model-dropdown', 'value'),
         State('make-dropdown', 'value'),
         State('keywords', 'value')]
    )
    def search_data(n_clicks, model, make, search_string):

        if make is not None and model is not None:

            # Call Trademe API and get data
            cars_json = getCarsJson(make, model, search_string)

            # Manipulate data
            clean_cars_json = manipulate_json(cars_json)

            # with open('test.json', 'w') as json_file:
            #     json.dump(clean_cars_json, json_file, indent=4)

            return clean_cars_json
        
        return []


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
        [State('odometer-value-graph', 'relayoutData'),
         State('input_odometer', 'value'),
         State('input_value', 'value')]
    )
    def update_odometer_graph(data, year, odometer, n_clicks, submit_n_clicks, relayoutData, input_odometer, input_value):

        if len(data) == 0:
            return dash.no_update

        df = pd.DataFrame(data)

        # Drop NA values from Value column
        df = df.dropna(subset=['Value'])

        # Filter based on make, model, year, and odometer
        filter_1 = df[(df['Year'] >= year[0]) & (df['Year'] <= year[1])]
        filtered_df = filter_1[(filter_1['Odometer'] >= odometer[0]) & (filter_1['Odometer'] <= odometer[1])]

        # Calculate prediction line
        # filtered_df = generate_predict_line(filtered_df)
        filtered_df = generate_loess_predictions(filtered_df, 0.6)

        # Calculate normalised residuals
        filtered_df['Norm_Residuals'] = (filtered_df['Predicted'] - filtered_df['Value']) / filtered_df['Predicted']
        filtered_df['Top_Residual'] = False
        top_residuals_indices = filtered_df['Norm_Residuals'].nlargest(8).index
        filtered_df.loc[top_residuals_indices, 'Top_Residual'] = True

        # Calculate outliers
        # outliers = calculateOutliers(filtered_df)
        # print(outliers[['Odometer', 'Value', 'Year']])

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

        fig1 = go.Figure()
        
        # Assign colors manually (you can use any color palette you prefer)
        unique_button_ids = filtered_df[button_id].unique()

        # Choose a continuous color scale from Plotly
        color_scale = px.colors.qualitative.Set1
        n_colors = len(unique_button_ids)
        color_indices = [i / (n_colors - 1) for i in range(n_colors)]
        colors = [px.colors.sample_colorscale(color_scale, x) for x in color_indices]    
        color_dict = dict(zip(unique_button_ids, colors))

        filtered_df['MarkerSize'] = filtered_df['Duration']
        filtered_df.loc[filtered_df['Duration'] > 30, 'MarkerSize'] = 30
        filtered_df['MarkerSize'] = filtered_df['MarkerSize']/30*15

        # Group the DataFrame by the color-coding variable and create a trace for each group
        for button_id_value, group_df in filtered_df.groupby(button_id):
            fig1.add_trace(go.Scatter(
                x=group_df['Odometer'],
                y=group_df['Value'],
                mode='markers',
                marker=dict(
                    color=color_dict[button_id_value][0],  # Use the color assigned to this button_id_value
                    symbol=['cross' if idx in top_residuals_indices else 'circle' for idx in group_df.index],
                    line=dict(
                        width=0,
                    ),
                    size=group_df['MarkerSize'],
                    sizeref=1
                ),
                customdata=group_df['ListingId'],
                name=button_id_value,  # Use button_id_value as the trace name for the legend
                
            ))



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
        fig1.add_trace(go.Scatter(x=filtered_df['Odometer'], y=filtered_df['Predicted'], mode='lines', name='Prediction'))

        # Before returning the figure, apply the current zoom level from relayoutData if present
        if relayoutData and 'xaxis.range[0]' in relayoutData and 'xaxis.range[1]' in relayoutData:
            fig1.update_xaxes(range=[relayoutData['xaxis.range[0]'], relayoutData['xaxis.range[1]']])
        if relayoutData and 'yaxis.range[0]' in relayoutData and 'yaxis.range[1]' in relayoutData:
            fig1.update_yaxes(range=[relayoutData['yaxis.range[0]'], relayoutData['yaxis.range[1]']])
        
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

        url = 'https://www.trademe.co.nz/a/motors/cars/' + str(clickData['points'][0]['customdata'])

        webbrowser.open_new_tab(url)

        return None
    

       
# # Change replot button data
#     @app.callback(
#         Output('replot-data-button', 'style'),
#         [Input('replot-data-button', 'n_clicks'),
#          Input('scrape-data-button', 'style')],
#         [State('replot-data-button', 'style')],
#         prevent_initial_call=True
#     )
#     def replot_button(replot_n_clicks, scrape_n_clicks, replot_style):
        
#         # Process and return the scraped data to update your Dash app
#         if replot_style['display'] == 'none':
#             replot_style = {'display': 'block'}
#         else:
#             replot_style = {'display': 'none'}

#         return  replot_style
    

#   # Refresh data
#     @app.callback(
#         Output('scrape-data-button', 'style'),
#         [Input('scrape-data-button', 'n_clicks')],
#         [State('model-dropdown', 'value'),
#          State('make-dropdown', 'value')],
#         prevent_initial_call=True
#     )
#     def refresh_data(scrape_n_clicks, model, make):
        
#         file_path = 'trademe_car_listings_20240108.csv'
#         df = pd.read_csv(file_path)

#         # Make a request to the Node.js server
#         response = requests.get(f'http://localhost:3000/scrape', params={'make': make, 'model': model})
#         data_json = response.json()

#         new_data = cleanData(data_json, "", 'trademe_car_listings_20240108.csv')
#         print(new_data)

#         # Create a mask to identify rows that don't match the specific make and model
#         try:
#             mask = ~((df['make'] == make) & (df['model'] == model))
#         except Exception as e:
#             print(e)

#         # Apply the mask to filter out the specified rows
#         df_remove_make_model = df[mask]

#         # Step 2: Concatenate the filtered original DataFrame with the new DataFrame
#         df = pd.concat([df_remove_make_model, new_data], ignore_index=True)
        
#         return {'display': 'block'}
    
        
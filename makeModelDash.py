# app.py
import dash
from dash import Dash
import dash_bootstrap_components as dbc
import makeModelDash_layout
from makeModelDash_callbacks import register_callbacks
from getCarListings import getCarsJson, manipulate_json
import pandas as pd


def runMakeModelDash(make, model):
    
    # No need for search_string so passing it an uempty value
    search_string = ''

    # Initialize the Dash app with Bootstrap
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

    # Call Trademe API and get data
    cars_json = getCarsJson(make, model, search_string)

    # Manipulate data
    clean_cars_json = manipulate_json(cars_json)

    app.layout = makeModelDash_layout.create_layout(app, clean_cars_json)

    register_callbacks(app, make, model)

    if __name__ == '__main__':
        app.run_server(debug=True)
    

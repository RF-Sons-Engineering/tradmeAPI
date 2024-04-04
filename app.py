# app.py
import dash
from dash import Dash
import dash_bootstrap_components as dbc
import layout
import pandas as pd
import json
from callbacks import register_callbacks
from flask import Flask


# Path to your JSON file
file_path = 'makes_models.json'

# Open the file and load the JSON data
with open(file_path, 'r') as file:
    makes_models = json.load(file)

# Initialize the Dash app with Bootstrap
# flask_server = Flask(__name__)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])
# server = app.server

app.layout = layout.create_layout(app, makes_models)

register_callbacks(app, makes_models)

if __name__ == '__main__':
    app.run_server(debug=True)
    

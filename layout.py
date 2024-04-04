# layout.py
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import json

def create_layout(app, makes_models):

    # Define the app layout with Bootstrap components
    layout = dbc.Container(fluid=True, children=[
        dbc.Row([
            dbc.Col(
                # Top Section: Dropdowns for Make and Model
                dbc.Row([
                    dbc.Row(dbc.Select(
                        id='make-dropdown',
                        options=[{'label': make, 'value': make} for make in sorted(list(makes_models.keys()))],
                        placeholder='Select Make'
                    )),
                    dbc.Row(dbc.Select(
                        id='model-dropdown',
                        options=[],
                        placeholder='Select Model'
                    )),
                    dbc.Row(dcc.Input(
                        id='keywords',
                        placeholder='Keywords...',
                        type='text',
                        value=''
                    )),
                    dbc.Row(dbc.Button(
                        "Get Data",
                        id='get-data-button',
                        n_clicks=0,
                        color="primary",
                        className="me-1"
                    ))
                ], className="mb-3", justify="center"), 
                width=4
            ),
            dbc.Col([
                # Bottom Section: Input boxes and submit button
                dbc.Row([
                    dbc.Col(dbc.Input(placeholder="Value", id="input_value", type="number")),
                    dbc.Col(dbc.Input(placeholder="Year", id="input_year", type="number")),
                    dbc.Col(dbc.Input(placeholder="Odometer", id="input_odometer", type="number"))]),
                dbc.Row([
                    dbc.Col(dbc.Input(placeholder="Main Colour", id='mainColour', type="text")),
                    dbc.Col(dbc.Input(placeholder="Seats", id='seats', type="number")),
                    dbc.Col(dbc.Input(placeholder="Engine Size", id='engineSize', type="text"))]),
                dbc.Row([
                    dbc.Col(dbc.Input(placeholder="Fuel", id='fuel', type="text")),
                    dbc.Col(dbc.Input(placeholder="Is 4WD", id='is4WD', type="text")),
                    dbc.Col(dbc.Input(placeholder="Transmission", id='transmission', type="text"))]),
                dbc.Row([
                    dbc.Col(dbc.Input(placeholder="Doors", id='doors', type="number")),
                    dbc.Col(dbc.Button("Submit", id="submit_button", color="primary", className="me-1"))
                ]), 
        ],
        width=6),
            ]),
        html.Div(id='output-div'),

        dcc.Store(id='memory'),


        # Middle Section 2 (similar to Middle Section 1)
        dbc.Row([
            # Left Column: Graph for Odometer vs Value
            dbc.Col(dcc.Graph(id='odometer-value-graph'), width=6),

            # Right Column: Filters and Sliders (similar to above)
            dbc.Col([
                # Top Part: Buttons for filters with unique IDs for Middle Section 2
            html.Div([
                dbc.Button('Main Colour', id={'type': 'odometer-button', 'index': 'MainColour'}, color="primary", className="me-1"),
                dbc.Button('Seats', id={'type': 'odometer-button', 'index': 'Seats'}, color="secondary", className="me-1"),
                dbc.Button('Engine Size', id={'type': 'odometer-button', 'index': 'EngineSize'}, color="success", className="me-1"),
                dbc.Button('Fuel', id={'type': 'odometer-button', 'index': 'Fuel'}, color="danger", className="me-1"),
                dbc.Button('Is 4WD', id={'type': 'odometer-button', 'index': 'Is4WD'}, color="warning", className="me-1"),
                dbc.Button('Transmission', id={'type': 'odometer-button', 'index': 'Transmission'}, color="info", className="me-1"),
                dbc.Button('Body Style', id={'type': 'odometer-button', 'index': 'BodyStyle'}, color="dark", className="me-1")
            ], className="d-grid gap-2 d-md-flex justify-content-md-start"),

            # Add this line to include the html.A component
            html.A(id='odometer-link', href='https://trademe.co.nz'),

                # Bottom Part: Sliders with unique IDs for Middle Section 2
                html.Div([
                    dcc.RangeSlider(
                        id='year-slider-2',
                        min=2000,  # Set minimum year
                        max=2024,  # Set maximum year
                        step=1,
                        allowCross=False,
                        tooltip={"placement": "bottom", "always_visible": True},
                        value=[2010, 2015],
                        marks={i: str(i) for i in range(1900, 2025, 2)}
                    ),
                    dcc.RangeSlider(
                        id='odometer-slider-2',
                        min=0,
                        max=200000,
                        step=None,
                        allowCross=False,
                        tooltip={"placement": "bottom", "always_visible": True},
                        value=[50000, 150000]
                        # marks={i: f'{i//1000}k' for i in range(0, 200001, 20000)}
                    )
                ], className="mt-auto mb-auto")
            ], width=6, className="d-flex flex-column justify-content-center")
        ], className="mb-3 h-50"),


        # Middle Section 1
        dbc.Row([
            # Left Column: Graph for Year vs Value
            dbc.Col(dcc.Graph(id='year-value-graph'), width=6),

            # Add this line to include the html.A component
            html.A(id='year-link', href='', target='_blank', style={'display': 'none'}),

            # Right Column: Filters and Sliders
            dbc.Col([
                # Top Part: Buttons for filters
            html.Div([
                dbc.Button('Main Colour', id={'type': 'year-button', 'index': 'MainColour'}, color="primary", className="me-1"),
                dbc.Button('Seats', id={'type': 'year-button', 'index': 'Seats'}, color="secondary", className="me-1"),
                dbc.Button('Engine Size', id={'type': 'year-button', 'index': 'EngineSize'}, color="success", className="me-1"),
                dbc.Button('Fuel', id={'type': 'year-button', 'index': 'Fuel'}, color="danger", className="me-1"),
                dbc.Button('Is 4WD', id={'type': 'year-button', 'index': 'Is4WD'}, color="warning", className="me-1"),
                dbc.Button('Transmission', id={'type': 'year-button', 'index': 'Transmission'}, color="info", className="me-1"),
                dbc.Button('Body Style', id={'type': 'year-button', 'index': 'BodyStyle'}, color="dark", className="me-1")
            ], className="d-grid gap-2 d-md-flex justify-content-md-start mb-3"),


                # Bottom Part: Sliders
                html.Div([
                    dcc.RangeSlider(
                        id='year-slider',
                        min=2000,  # Set minimum year
                        max=2024,  # Set maximum year
                        step=1,
                        allowCross=False,
                        tooltip={"placement": "bottom", "always_visible": True},
                        value=[2010, 2020],
                        marks={i: str(i) for i in range(1900, 2025, 2)}
                    ),
                    dcc.RangeSlider(
                        id='odometer-slider',
                        min=1000,
                        max=200000,
                        step=None,
                        allowCross=False,
                        tooltip={"placement": "bottom", "always_visible": True},
                        value=[50000,150000]
                        # marks={i: f'{i//1000}k' for i in range(0, 200001, 20000)}
                    )
                ], className="mt-auto mb-auto")
            ], width=6, className="d-flex flex-column justify-content-center")
        ], className="mb-3 h-50"),
        
 
    ])

    return layout
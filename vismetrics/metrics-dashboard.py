# importing Pandas libary
import pandas as pd
from dash import Dash, dcc, Output, Input, html  # pip install dash
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components

# Build your components
app = Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])
myinput = dcc.Markdown(children="# Simulation results")

# Create switches
switches = html.Div(
    [
        dbc.Checklist(
            options=[
                {"label": "Single run", "value": 1},
            ],
            value=[1],
            id="switches-input",
            switch=True,
        ),
    ]
)
# Customize your own Layout
app.layout = dbc.Container(
    [myinput,switches]
)

# Run app
if __name__=='__main__':
    app.run_server(port=8052)

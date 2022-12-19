import pandas as pd
from dash import Dash, dcc, Output, Input, html  # pip install dash
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components

# -------------------------------
# Building components
# -------------------------------
app = Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])
title = dcc.Markdown(children="# Simulation results")

# Create switches
run_switch = html.Div(
    [
        html.P(
            "All runs",
            style={"display": "inline-block"}
        ),
        dbc.Checklist(
            options=[
                {"label": "Single run", "value": "single"},
            ],
            value=["single"],
            id="run-switch",
            switch=True,
            style={"display": "inline-block", "margin-left": "10px"}
        ),

    ]
)

# All runs div
all_runs = html.Div(
    [
        html.P("ALL RUNS")
    ],
    id="all-runs-components",
    style={"display": "block"} # This line is changed by single_or_all function
)

# Single run div
single_run = html.Div(
    [
        html.P("Hello this is for a single run")
    ],
    id="single-run-components",
    style={"display": "none"} # This line is changed by single_or_all function
)

# -------------------------------
# Customise layout
# -------------------------------
app.layout = dbc.Container(
    [title, run_switch, single_run, all_runs]
)

# -------------------------------
# Call back functions
# -------------------------------
@app.callback(
    [
        Output(component_id="single-run-components", component_property="style"),
        Output(component_id="all-runs-components", component_property="style")
    ],
    Input(component_id="run-switch", component_property="value")
)
def single_or_all_run_display(run_type):
    if run_type == ["single"]:
        return {"display": "block"}, {"display": "none"}
    else:
        return {"display": "none"}, {"display": "block"}




# Run app
if __name__=='__main__':
    app.run_server(port=8052, debug=True)

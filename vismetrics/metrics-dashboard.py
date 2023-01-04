import pandas as pd
import dash
from dash import Dash, dcc, Output, Input, html  # pip install dash
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components
import plotly.express as px

# Import graphs
from timeline_vis import timeline_fig, ddg_killed, hvu_killed, time_to_kill_bar_chart

# -------------------------------
# Building components
# -------------------------------
# TODO: this will need to change to local reference
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])
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

# -------------------------------
# Create single run components
# -------------------------------

# Timeline graph
timeline_graph_component = html.Div(
    [
        dcc.Markdown(children="### Timeline"),
        dcc.Graph(figure=timeline_fig)
    ],
    id="timeline-graph-and-title",
    style={"display": "inline-block", "width": "100%"}
)

# Alerts for main platforms
# Alert text based on ddg_killed and hvu_killed
alert_text = {
    True: {
        "color": "success",
        "className": "bi bi-check-circle-fill me-2",
        "text": "killed"
    },
    False: {
        "color": "danger",
        "className": "bi bi-x-octagon-fill me-2",
        "text": "not killed"
    }
}
alerts = html.Div(
    [
        dbc.Alert(
            [
                html.I(className=alert_text[hvu_killed]["className"]),
                "Red HVU " + alert_text[hvu_killed]["text"],
            ],
            color=alert_text[hvu_killed]["color"],
            className="d-flex align-items-center",
        ),
        dbc.Alert(
            [
                html.I(className=alert_text[ddg_killed]["className"]),
                "Red DDG " + alert_text[ddg_killed]["text"],
            ],
            color=alert_text[ddg_killed]["color"],
            className="d-flex align-items-center",
        )
    ],
    style={"display": "inline-block"}
)
alert_container = html.Div(
    [
        alerts,
        dcc.Graph(figure=time_to_kill_bar_chart, style={"display": "inline-block", "height": "20vh"})
    ],
    style={"display": "flex"}
)

# Number of blue platforms killed
blue_killed_container = html.Div(
    [
        html.Span("3", style={"font-size": "25px", "font-weight": "bold", "color": "blue", "display": "inline-block"}),
        html.Span("/8 blue platforms killed", style={"font-size": "25px", "display": "inline-block"}),
    ],
    style={"display": "flex"}
)


# Chord diagram (test)
chord_diagram_container = html.Div(
    [
        html.Iframe(src="assets/chord-diagram.html", style={"height": "650px", "width": "650px", "display": "inline-block"})
    ],
    style={"display": "inline-block"}
)

# Chord diagram and timeline together in one div
chord_and_timeline_container = html.Div(
    [
        chord_diagram_container,
        timeline_graph_component
    ],
    style={"display": "flex"}
)

# SINGLE DIV COMPONENTS TOGETHER
single_run = html.Div(
    [
        alert_container,
        blue_killed_container,
        html.Br(),
        chord_and_timeline_container
        # chord_diagram_container,
        # html.Br(),
        # timeline_graph_component
    ],
    id="single-run-components",
    style={"display": "none"}  # This line is changed by single_or_all function
)
# -------------------------------
# Create all runs components
# -------------------------------

# All runs div
all_runs = html.Div(
    [
        html.P("ALL RUNS")
    ],
    id="all-runs-components",
    style={"display": "block"}  # This line is changed by single_or_all function
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

# Displays and hides single run and all runs div
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
if __name__ == "__main__":
    app.run_server(port=8052, debug=True)

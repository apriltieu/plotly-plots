"""
This script creates a basic scatterplot diagram
"""

import plotly.graph_objects as go
import pandas as pd

filename = "scatter/data/scatter_data.xlsx"

# Read excel file
xlsx_df = pd.read_excel(filename)

# Change colour based on another column
xlsx_df["colours"] = xlsx_df["event"].apply(lambda x: 1 if x=="event_one" else (2 if x=="event_two" else (3 if x=="event_three" else 4)))

print(xlsx_df)
fig = go.Figure(data=go.Scatter(
    x=xlsx_df["time"], y=xlsx_df["name"], mode='markers',
    marker=dict(
        color=xlsx_df["colours"]
    )
))
fig.show()
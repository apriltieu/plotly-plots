"""
This script creates a sankey diagram
"""

import plotly.graph_objects as go
from to_sankey_data import sankey_dict

fig = go.Figure(data=[go.Sankey(
    valueformat = ".0f",
    valuesuffix = "TWh",
    # Define nodes
    node=dict(
      pad=15,
      thickness = 15,
      line = dict(color = "black", width = 0.5),
      label = sankey_dict['data']['node']['label']
    ),
    # Add links
    link = dict(
      source = sankey_dict['data']['link']['source'],
      target = sankey_dict['data']['link']['target'],
      value = sankey_dict['data']['link']['value']
))])

fig.show()



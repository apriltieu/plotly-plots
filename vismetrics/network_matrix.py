import pandas as pd
import numpy as np
import networkx as nx
import plotly.graph_objects as go
import json

# Import data
killchain_output_raw = pd.read_csv("vismetrics/example_data/example.csv")
start_time = 0
end_time = killchain_output_raw["time"].max()
killchain_output_raw = killchain_output_raw[(killchain_output_raw["time"]>start_time) & (killchain_output_raw["time"]<end_time)]
unique_node_links = killchain_output_raw[["platform_name", "engaging_platform_name"]].value_counts().reset_index(name='count')

# Get unique source and target nodes
source_nodes = unique_node_links["engaging_platform_name"].to_list()
target_nodes = unique_node_links["platform_name"].to_list()

# Create an empty graph
G = nx.Graph()
# Add edges
edge_list = list(zip(source_nodes, target_nodes))
G.add_edges_from(edge_list)
pos = nx.random_layout(G)
edge_x = []
edge_y = []
node_x = []
node_y = []

for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.append(x0)
    edge_x.append(x1)
    edge_x.append(None)
    edge_y.append(y0)
    edge_y.append(y1)
    edge_y.append(None)

edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=0.5, color="#888"),
    hoverinfo="none",
    mode="lines"
)

for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)
node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode="markers",
    hoverinfo="text",
    marker=dict(
        showscale=True,
        colorscale="Greys",
        reversescale=True,
        color=[],
        size=10)
)
node_adjacencies = []
node_text = []
for node, adjacencies in enumerate(G.adjacency()):
    node_adjacencies.append(len(adjacencies[1]))
    node_text.append("# connections: " + str(len(adjacencies[1])))
node_trace.marker.color = node_adjacencies
node_trace.text = node_text

fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    hovermode="closest"
                )
                )
print(json.dumps(nx.to_numpy_matrix(G, nodelist=sorted(G.nodes())).tolist()))
# fig.show()
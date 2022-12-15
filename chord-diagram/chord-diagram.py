import pandas as pd
import holoviews as hv
from holoviews import opts, dim
from bokeh.sampledata.les_mis import data
from bokeh.plotting import show
# Example: https://holoviews.org/reference/elements/bokeh/Chord.html

hv.extension('bokeh')
hv.output(size=200)
#
# links_dict = {
#     "source": [1, 2, 3],
#     "target": [0, 0, 0],
#     "value": [1, 1, 1]
# }
# links = pd.DataFrame.from_dict(links_dict)
# nodes_dict = {
#     "index": [0, 1, 2, 3],
#     "name": ["one", "two", "three", "four"],
#     "group": [1, 1, 2, 2]
# }
# nodes_df = pd.DataFrame.from_dict(nodes_dict)
# nodes = hv.Dataset(nodes_df["name"], 'index')
# print(nodes_df)
# chord = hv.Chord((links, nodes)).select(value=(5, None))
# chord.opts(
#     opts.Chord(cmap='Category20', edge_cmap='Category20', edge_color=dim('source').str(),
#                labels='name', node_color=dim('index').str()))
#
#
# show(hv.render(chord))

links = pd.read_csv("chord-diagram/data/links.csv")
nodes_data = pd.read_csv("chord-diagram/data/nodes.csv")
print(links)
print(nodes_data)
#add node labels
nodes = hv.Dataset(pd.DataFrame(nodes_data), 'index')
#create chord object
chord = hv.Chord((links, nodes)).select(value=(5, None))
#customization of chart
chord.opts(
           opts.Chord(cmap='Category20',
                      edge_cmap='Category20',
                      edge_color='group',
                      labels='nodes',
                      node_color='group'))

show(hv.render(chord))


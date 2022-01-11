"""
Converts data into required plotly format (only 2D)
"""


import pandas as pd

# Ask for location
# print("Enter the filepath:")
# filename = input()
# Example data at:
filename = 'data/sankey_data.xlsx'

# Read excel file
xlsx_df = pd.read_excel(filename, index_col=0)

# Initialise final plotly data format
sankey_dict = {
    "data":
        {
            "node": {
                "label": []
            },
            "link": {
                "source": [],
                "target": [],
                "value": []
            }
        }
}

# Create labels
sankey_dict["data"]["node"]["label"] = list(xlsx_df.columns) + list(xlsx_df.index)

# Iterate through df and add to sankey_dict
for ci in xlsx_df.columns:
    for ri in xlsx_df.index:
        source = sankey_dict["data"]["node"]["label"].index(ci)
        target = sankey_dict["data"]["node"]["label"].index(ri)
        value = xlsx_df[ci][ri]

        # Change sankey_dict data
        sankey_dict["data"]["link"]["source"] += [source]
        sankey_dict["data"]["link"]["target"] += [target]
        sankey_dict["data"]["link"]["value"] += [value]




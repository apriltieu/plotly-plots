import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import timedelta


# --------------------------------------------
# Timeline graph
# --------------------------------------------
# Change data


def finish_time(row, df):
    if row["event"] == "Track_Started":
        # Find all elements
        next_tracks_dropped = df[(df["platform_name"] == row["platform_name"]) &
                                 (df["engaging_platform_name"] == row["engaging_platform_name"]) &
                                 (df["event"] == "Track_Dropped") &
                                 (df["time"] > row["time"])]
        # If no next
        if next_tracks_dropped.empty:
            # Remove
            finish_datetime = None
        else:
            # Get first element
            next_track_dropped = next_tracks_dropped.head(1)
            # Get finish time
            finish_time = next_track_dropped["time"].values[0]
            finish_datetime = "2022-12-19 " + str(timedelta(seconds=finish_time))
    else:
        finish_time = row["time"] + 2
        finish_datetime = "2022-12-19 " + str(timedelta(seconds=finish_time))
    # px.timeline only takes in date time format
    return finish_datetime


colors_timeline = {
    "Detected": "#86B049",
    "Tracked": "#476930",
    "Attacked": "yellow",
    "Hit": "orange",
    "Killed": "red",
    "Missed": "grey",
}
raw_output = pd.read_csv("vismetrics/example_data/example.csv")
df = raw_output.copy()

# Change finish column to different time
df["finish"] = df.apply(lambda row: finish_time(row, df), axis=1)
df = df.dropna()
# Change start time to date time format
df["time"] = df.apply(lambda row: "2022-12-19 " + str(timedelta(seconds=row["time"])), axis=1)

# Rename events and remove Track_Dropped
df = df.replace("Track_Started", "Tracked")
df = df.replace("Attack_Initiated", "Attacked")
df = df[df["event"] != "Track_Dropped"]

# Change name of time column to "start"
df.rename(columns={"time": "start"}, inplace=True)

# Create figure
timeline_fig = px.timeline(df,
                           x_start="start",
                           x_end="finish",
                           y="platform_name",
                           color="event",
                           color_discrete_map=colors_timeline,
                           hover_name="platform_name",
                           hover_data=["engaging_platform_name", "event", "start", "finish"])
# fig = px.timeline(df[df["platform_name"]=="red_ffg_1"], x_start="start", x_end="finish", y="platform_name", color="event")

# https://stackoverflow.com/questions/71896691/add-go-scatter-plots-and-gantt-plot-to-the-same-plotly-subplot
timeline_fig.add_traces(
    px.scatter(df[df["event"] == "Killed"], x="finish", y="platform_name", color_discrete_sequence=["red"]).data
)
timeline_fig.update_layout(xaxis=dict(
    title='Timestamp',
    tickformat='%H:%M:%S',
    range=[df["start"].min(), df["finish"].max()]
))
timeline_fig.update_xaxes(minor=dict(ticks="inside", showgrid=True), rangeslider_visible=True)

# --------------------------------------------
# HVU and DDG killed metric (test)
# --------------------------------------------
if not df[(df["event"] == "Killed") & (df["platform_name"] == "red_ddg_1")].empty:
    ddg_killed = True
else:
    ddg_killed = False

if not df[(df["event"] == "Killed") & (df["platform_name"] == "red_supply_1")].empty:
    hvu_killed = True
else:
    hvu_killed = False

# Plot of time taken
ddg_and_hvu = raw_output[(raw_output["platform_name"] == "red_ddg_1") | (raw_output["platform_name"] == "red_supply_1")]
time_to_kill_df = ddg_and_hvu[ddg_and_hvu["event"] == "Killed"]

#TODO: add row for platforms if they do not exist
time_to_kill_bar_chart = px.bar(
    time_to_kill_df,
    x="time",
    y="platform_name",
    orientation="h",
    hover_data=["engaging_platform_name"],
    color_discrete_sequence=["lightgrey"]
)
time_to_kill_bar_chart.add_traces(
    px.scatter(time_to_kill_df, x="time", y="platform_name", color_discrete_sequence=["red"]).data
)
time_to_kill_bar_chart.update_yaxes(title=None)
time_to_kill_bar_chart.update_xaxes(title="time to kill (s)")
time_to_kill_bar_chart.update_layout(
    margin=dict(l=20, r=20, t=20, b=20),
)
# --------------------------------------------
# HVU and DDG killed metric (test)
# --------------------------------------------
# Find number of blue lost



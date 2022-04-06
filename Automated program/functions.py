import numpy as np
import pandas as pd

def generateFeatures(df, interval=0.5): 
  stop = False
  time = interval
  final_time = float(df.tail(1)["frame.time_relative"])
  rows = []

  while stop == False:
    sub_df = df[(df["frame.time_relative"] >= time - interval) & (df["frame.time_relative"] < time)]

    packet_count = sub_df.shape[0]
    no_sources = sub_df["ip.src"].nunique()
    no_dests = sub_df["ip.dst"].nunique()
    pack_length = round(sub_df["frame.len"].mean())
    min_length = sub_df["frame.len"].min()
    max_length = sub_df["frame.len"].max()
    packet_types = sub_df["ip.proto"].nunique()
    s7_packs = sub_df[sub_df["ip.proto"] == "S7COMM"].count()[0]
    row = [time, int(packet_count), no_sources, no_dests, pack_length,
	 min_length, max_length, packet_types, s7_packs]
    rows.append(row)

    time += interval
    if final_time - time < - interval:
      stop = True
  
  features = pd.DataFrame(rows, columns=["Time","No Packets", "No Sources",
   "No Destinations", "Avg Pack Length", "Minimum Length", "Maximum Length", "No Packet Types", "No S7 packs"])
  features = features.set_index("Time")

  return(features)


import json 
from datetime import datetime, timedelta
import utilities
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

data_path = utilities.get_data_path(tree_level=2)
basename_btc = f"btc"
basename_eth = f"eth"

filename_btc = os.path.join(data_path, "datasets", f"{basename_btc}_stats.csv")
filename_eth = os.path.join(data_path, "datasets", f"{basename_eth}_stats.csv")

def convert_times(filename):
	df = pd.read_csv(filename)
	df["time"] = pd.to_datetime(df["time"], format="b'%Y-%m-%dT%H:%M:%S.%fZ'")
	return df

df_btc = convert_times(filename_btc)
df_eth = convert_times(filename_eth)

min_time_btc = df_btc["time"].min()
min_time_eth = df_eth["time"].min()
min_time = min(min_time_btc, min_time_eth)
if min_time_eth < min_time_btc:
	min_time_product = "ETH"
elif min_time_eth > min_time_btc:
	min_time_product = "BTC"
else:
	# Not gonna happen but stil...
	min_time_product = "BTC+ETH SAME TIME"

with open(os.path.join(data_path, "master_date.txt"), 'w') as md_f:
	md_f.write(f"{min_time_product} {min_time}")

def convert_datetimes_to_floats(df, min_datetime):
	df["time"] = df["time"].apply(lambda dt: dt - min_datetime)
	df["time"] = df["time"].apply(lambda dt: dt.seconds + dt.microseconds / 1e6)
	return df
	
df_btc = convert_datetimes_to_floats(df_btc, min_time)
df_eth = convert_datetimes_to_floats(df_eth, min_time)

df_btc.to_csv(os.path.join(data_path, "datasets", f"{basename_btc}_times_transformed.csv"), index=False)
df_eth.to_csv(os.path.join(data_path, "datasets", f"{basename_eth}_times_transformed.csv"), index=False)

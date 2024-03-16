import utilities
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

### PARAMETERS
# Nothing :O
###


def align_datasets(dataset1_file, dataset2_file):
	"""
	Aligns two datasets with potentially different timestamps by filling missing entries with duplicates.

	Args:
		dataset1_file: Path to the file containing the first dataset.
		dataset2_file: Path to the file containing the second dataset.
	
	Returns: 
		df1_new: aligned dataset1_file in form of dataframe
		df2_new: aligned dataset2_file in form of dataframe
	"""
	df1 = pd.read_csv(dataset1_file)
	df2 = pd.read_csv(dataset2_file)
	# Set the timestamp column
	df1.set_index('time', inplace=True)
	df2.set_index('time', inplace=True)

	df1_idxs = df1.index
	df2_idxs = df2.index
	fill_first_backward = True
	if df1_idxs[0] < df2_idxs[0]:
		fill_first_backward = False

	combined_idxs = df1_idxs.union(df2_idxs)
	if len(combined_idxs) != len(df1_idxs) + len(df2_idxs):
		print("WARNING: Duplicates found!")
		raise Exception("DUPLICATES!?")

	df1_new = df1.reindex(df1_idxs.append(df2_idxs)).sort_index().ffill()
	df2_new = df2.reindex(df2_idxs.append(df1_idxs)).sort_index().ffill()

	# Forward fill will leave one row empty for the dataset which time is second from the beginning
	# For test1.csv and test2.csv it appears as:
	# test1.csv			test2.csv
	# time, value		time,value
	# 0.0,11.0			0.0,
	# 0.028059,11.0		0.028059,21.0
	if fill_first_backward:
		df1_new.bfill(inplace=True)
		print("Filled NaN in first dataset!")
	else:
		df2_new.bfill(inplace=True)
		print("Filled NaN in second dataset!")

	return df1_new, df2_new
	

data_path = utilities.get_data_path(tree_level=2)
# BTC+ETH
filename_btc = os.path.join(data_path, "datasets", f"btc_times_transformed.csv")
filename_eth = os.path.join(data_path, "datasets", f"eth_times_transformed.csv")
filename_btc_aligned = os.path.join(data_path, "datasets", f"btc_stats_aligned.csv")
filename_eth_aligned = os.path.join(data_path, "datasets", f"eth_stats_aligned.csv")
# Test
filename_test1 = os.path.join(data_path, "datasets", f"test1_times_transformed.csv")
filename_test2 = os.path.join(data_path, "datasets", f"test2_times_transformed.csv")
filename_test1_aligned = os.path.join(data_path, "datasets", f"test1_aligned.csv")
filename_test2_aligned = os.path.join(data_path, "datasets", f"test2_aligned.csv")

df1_aligned, df2_aligned = align_datasets(filename_btc, filename_eth)
df1_aligned.to_csv(filename_btc_aligned)
df2_aligned.to_csv(filename_eth_aligned)

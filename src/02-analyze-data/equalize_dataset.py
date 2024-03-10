import utilities
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

### PARAMETERS

###

data_path = utilities.get_data_path(tree_level=2)
filename_btc = os.path.join(data_path, "datasets", f"btc_stats.csv")
filename_eth = os.path.join(data_path, "datasets", f"eth_stats.csv")
filename_btc_aligned = os.path.join(data_path, "datasets", f"btc_stats_aligned.csv")
filename_eth_aligned = os.path.join(data_path, "datasets", f"eth_stats_aligned.csv")

# times = [line.get("time") for line in lines][1:]
# times = [datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ") for time in times][:100]

def align_datasets(dataset1_file, dataset2_file, aligned_dataset1_file, aligned_dataset2_file):
	"""
	Aligns two datasets with potentially different timestamps by filling missing entries with duplicates, writing results to files.

	Args:
		dataset1_file: Path to the file containing the first dataset.
		dataset2_file: Path to the file containing the second dataset.
		aligned_dataset1_file: Path to write the aligned first dataset.
		aligned_dataset2_file: Path to write the aligned second dataset.
	"""
	df1 = pd.read_csv(dataset1_file)
	df2 = pd.read_csv(dataset2_file)
	# Set the timestamp column
	df1.set_index('time', inplace=True)
	df2.set_index('time', inplace=True)

	df1_idxs= df1.index
	df2_idxs= df2.index

	combined_idxs = df1_idxs.union(df2_idxs)
	if len(combined_idxs) != len(df1_idxs) + len(df2_idxs):
		print("WARNING: Duplicates found!")
		raise Exception("DUPLICATES!?")

	df1_new = df1.reindex(df1_idxs.append(df2_idxs)).sort_index().ffill()
	df2_new = df2.reindex(df2_idxs.append(df1_idxs)).sort_index().ffill()

	print(np.all(df1_new.index == df2_new.index))
	

	

def ai_align_datasets(dataset1_file, dataset2_file, aligned_dataset1_file, aligned_dataset2_file):
	"""
	Aligns two datasets with potentially different timestamps by filling missing entries with duplicates using pandas.
	"""
	df1 = pd.read_csv(dataset1_file)
	df2 = pd.read_csv(dataset2_file)

	# Set the timestamp column
	df1.set_index('time', inplace=True)
	df2.set_index('time', inplace=True)

	# Set the timestamp column for merging (assuming 'time' is the timestamp column)
	df_merged = pd.merge(df1, df2, how='outer', on='time')

	# Forward fill missing values in df1 columns (duplicate previous row for df1)
	df_merged.loc[df1.index, df1.columns] = df_merged.loc[df1.index, df1.columns].fillna(method='ffill')

	# Drop rows with all NaN values (empty rows after ffill)
	df_merged.dropna(how='all', inplace=True)

	# Separate aligned DataFrames (df1 with duplicates and df2 with originals)
	df_aligned1 = df_merged[df_merged.columns.intersection(set(df1.columns))]
	df_aligned2 = df_merged[df_merged.columns.intersection(set(df2.columns))]

	# Write aligned datasets to CSV files
	df_aligned1.to_csv(aligned_dataset1_file, index=False)
	df_aligned2.to_csv(aligned_dataset2_file, index=False)

filename_test1 = os.path.join(data_path, "datasets", f"test1-times.csv")
filename_test2 = os.path.join(data_path, "datasets", f"test2-times.csv")

align_datasets(filename_test1, filename_test2, filename_btc_aligned, filename_eth_aligned)

# align_datasets(filename_btc, filename_eth, filename_btc_aligned, filename_eth_aligned)
# align_datasets(filename_test1, filename_test2, filename_btc_aligned, filename_eth_aligned)

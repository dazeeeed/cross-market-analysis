import utilities
import os
import numpy as np
import json
import pandas as pd
from tqdm import tqdm

### PARAMETERS
product = "eth"
###

data_path = utilities.get_data_path(tree_level=2)
filename = os.path.join(data_path, f"messages-{product}.txt")

class Orderbook:
	def __init__(self):
		self.asks = {} # Sell 
		self.bids = {} # Buy

	def update_order_book(self, change):
		order_type, price, amount = change
		order_dict = self.bids if order_type == 'buy' else self.asks

		# if price in order_dict:
		# 	if amount == '0.00000000':
		# 		order_dict.pop(price)
		# 		print("Removing: ", price)
		# 	else:
		# 		order_dict[price] = amount
		# 		print("Updating: ", price)
		# else:
		# 	order_dict[price] = amount
		# 	print("Adding: ", price)

		if amount == '0.00000000':
			rc = order_dict.pop(price, None)
			# print("Removing: ", price, ("NOT FOUND" if rc == None else "OK"))
		else:
			order_dict[price] = amount
			# print("Adding/Updating: ", price)


def update_stats(ob, stats):
	"""Update stats array from orderbook (ob) data"""
	keys_bids = np.fromiter(ob.bids.keys(), dtype=float)
	keys_asks = np.fromiter(ob.asks.keys(), dtype=float)
	values_bids = np.fromiter(ob.bids.values(), dtype=float)
	values_asks = np.fromiter(ob.asks.values(), dtype=float)
	
	### Basic stats of bid prices
	stats[i, 0] = np.min(keys_bids)
	stats[i, 1] = np.quantile(keys_bids, .25)
	stats[i, 2] = np.quantile(keys_bids, .50)
	stats[i, 3] = np.quantile(keys_bids, .75)
	stats[i, 4] = np.max(keys_bids)
	stats[i, 5] = np.mean(keys_bids)
	stats[i, 6] = np.std(keys_bids)

	### Basic stats of ask prices
	stats[i, 7] = np.min(keys_asks)
	stats[i, 8] = np.quantile(keys_asks, .25)
	stats[i, 9] = np.quantile(keys_asks, .50)
	stats[i, 10] = np.quantile(keys_asks, .75)
	stats[i, 11] = np.max(keys_asks)
	stats[i, 12] = np.mean(keys_asks)
	stats[i, 13] = np.std(keys_asks)

	### Stats of combinations bid * amount
	bid_volume = keys_bids * values_bids
	# Total bid volume - calkowita wartosc zlecen kupna na gieldzie
	stats[i, 14] = np.sum(bid_volume)
	stats[i, 15] = np.min(bid_volume)
	stats[i, 16] = np.quantile(bid_volume, .25)
	stats[i, 17] = np.quantile(bid_volume, .50)
	stats[i, 18] = np.quantile(bid_volume, .75)
	stats[i, 19] = np.max(bid_volume)
	stats[i, 20] = np.mean(bid_volume)
	stats[i, 21] = np.std(bid_volume)

	### Stats of combination ask * amount
	ask_volume = keys_asks * values_asks
	# Total ask volume - calkowita wartosc zlecen sprzedazy na gieldzie
	stats[i, 22] = np.sum(ask_volume)
	stats[i, 23] = np.min(ask_volume)
	stats[i, 24] = np.quantile(ask_volume, .25)
	stats[i, 25] = np.quantile(ask_volume, .50)
	stats[i, 26] = np.quantile(ask_volume, .75)
	stats[i, 27] = np.max(ask_volume)
	stats[i, 28] = np.mean(ask_volume)
	stats[i, 29] = np.std(ask_volume)

	return stats

num_lines = sum(1 for _ in open(filename))
# Length of timestamp always 27, check with regex '\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{6}Z'
data_times = np.chararray(shape=num_lines, itemsize=27)
stats = np.zeros(shape=(num_lines, 30))

ob = Orderbook()

with open(filename) as file:
	for i in tqdm(range(num_lines)):
	# for i in range(num_lines):
		line = json.loads(file.readline())

		data_times[i] = line["time"]

		if i == 0:
			ob.bids = {price: amount for price, amount in line["bids"]}
			ob.asks = {price: amount for price, amount in line["asks"]}
			stats = update_stats(ob, stats)	
			continue
		
		changes = line["changes"]

		for change in changes:
			# Remember that some changes are proecessed but do not affect orderbook as some prices
			# are missing
			ob.update_order_book(change)
	
		stats = update_stats(ob, stats)

		# if i == 1000:
			# break

df_times = pd.DataFrame({'time': data_times})

df_stats = pd.DataFrame({
	'bid_price_min': stats[:, 0],
	'bid_price_q1': stats[:, 1],
	'bid_price_median': stats[:, 2],
	'bid_price_q3': stats[:, 3],
	'bid_price_max': stats[:, 4],
	'bid_price_mean': stats[:, 5],
	'bid_price_std': stats[:, 6],

	'ask_price_min': stats[:, 7],
	'ask_price_q1': stats[:, 8],
	'ask_price_median': stats[:, 9],
	'ask_price_q3': stats[:, 10],
	'ask_price_max': stats[:, 11],
	'ask_price_mean': stats[:, 12],
	'ask_price_std': stats[:, 13],

	'bid_vol_price_sum': stats[:, 14],
	'bid_vol_price_min': stats[:, 15],
	'bid_vol_price_q1': stats[:, 16],
	'bid_vol_price_median': stats[:, 17],
	'bid_vol_price_q3': stats[:, 18],
	'bid_vol_price_max': stats[:, 19],
	'bid_vol_price_mean': stats[:, 20],
	'bid_vol_price_std': stats[:, 21],

	'ask_vol_price_sum': stats[:, 22],
	'ask_vol_price_min': stats[:, 23],
	'ask_vol_price_q1': stats[:, 24],
	'ask_vol_price_median': stats[:, 25],
	'ask_vol_price_q3': stats[:, 26],
	'ask_vol_price_max': stats[:, 27],
	'ask_vol_price_mean': stats[:, 28],
	'ask_vol_price_std': stats[:, 29],
})

### Add more statistics
# Spread stats
df_stats['spread_min'] = df_stats['ask_price_min'] - df_stats['bid_price_max']
df_stats['spread_btwn_means'] = df_stats['ask_price_mean'] - df_stats['bid_price_mean']
df_stats['spread_btwn_medians'] = df_stats['ask_price_median'] - df_stats['bid_price_median']
df_stats['spread_btwn_vol_sums'] = df_stats['ask_vol_price_sum'] - df_stats['bid_vol_price_sum']
df_stats['spread_btwn_vol_means'] = df_stats['ask_vol_price_mean'] - df_stats['bid_vol_price_mean']
df_stats['spread_btwn_vol_medians'] = df_stats['ask_vol_price_median'] - df_stats['bid_vol_price_median']

df_combined = pd.concat([df_times, df_stats], axis=1)

# Save to parquet
# df_times.to_parquet(os.path.join(data_path, 'datasets', 'btc_times.parquet'))
# df_stats.to_parquet(os.path.join(data_path, 'datasets', 'btc_stats.parquet'))
# df_combined.to_parquet(os.path.join(data_path, 'datasets', f'{product}_stats.parquet'))
df_combined.to_csv(os.path.join(data_path, "datasets", f"{product}_stats.csv"), index=False)
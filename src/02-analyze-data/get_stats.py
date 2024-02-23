import utilities
import os
import numpy as np
import json
from collections import OrderedDict
from tqdm import tqdm

data_path = utilities.get_data_path(tree_level=2)
filename = os.path.join(data_path, "messages-btc.txt")

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
	
	# Basic stats of bid prices
	stats[i, 0] = np.min(keys_bids)
	stats[i, 1] = np.quantile(keys_bids, .25)
	stats[i, 2] = np.quantile(keys_bids, .50)
	stats[i, 3] = np.quantile(keys_bids, .75)
	stats[i, 4] = np.max(keys_bids)
	stats[i, 5] = np.mean(keys_bids)
	stats[i, 6] = np.std(keys_bids)

	# Basic stats of ask prices
	stats[i, 7] = np.min(keys_asks)
	stats[i, 7] = np.quantile(keys_asks, .25)
	stats[i, 9] = np.quantile(keys_asks, .50)
	stats[i, 10] = np.quantile(keys_asks, .75)
	stats[i, 11] = np.max(keys_asks)
	stats[i, 12] = np.mean(keys_asks)
	stats[i, 13] = np.std(keys_asks)

	# Stats of combinations bid * amount
	...

	# Stats of combination ask * amount
	...

	
	return stats

num_lines = sum(1 for _ in open(filename))
# Length of timestamp always 27, check with regex '\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{6}Z'
data_times = np.chararray(shape=num_lines, itemsize=27)
stats = np.zeros(shape=(num_lines, 14))

ob = Orderbook()

with open(filename) as file:
	# for i in tqdm(range(num_lines)):
	for i in range(num_lines):
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

		if i == 18:
			break

		# print(i, "asks ", ob.asks)
		# print(i, "bids ", ob.bids)

print(stats[:20])
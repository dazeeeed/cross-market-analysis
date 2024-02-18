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

def update_order_book(ob, change):
	order_type, price, amount = change
	order_dict = ob.bids if order_type == 'buy' else ob.asks

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


num_lines = sum(1 for _ in open(filename))

# Length of timestamp always 27, check with regex '\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{6}Z'
data_times = np.chararray(shape=(num_lines), itemsize=27)

ob = Orderbook

with open(filename) as file:
	# for i in tqdm(range(num_lines)):
	for i in range(num_lines):
		line = json.loads(file.readline())

		data_times[i] = line["time"]

		if i == 0:
			ob.asks = {price: amount for price, amount in line["asks"]}
			ob.bids = {price: amount for price, amount in line["bids"]}
			# print(i, ob.asks)
			continue
		
		changes = line["changes"]
		# print(i, changes)
		for change in changes:
			update_order_book(ob, change)
	
		if i > 2:
			break

		print(i, "asks ", ob.asks)
		# print(i, "bids ", ob.bids)


import os
import numpy as np

def get_current_path():
    return os.path.dirname(os.path.realpath(__file__))

def get_data_path(tree_level=1):
    return os.path.abspath(os.path.join(get_current_path(), tree_level * '../', 'data'))

def running_mean(x, N):
    out = np.zeros_like(x, dtype=np.float64)
    dim_len = x.shape[0]
    for i in range(dim_len):
        if N % 2 == 0:
            a = i - (N-1) // 2
            b = i + (N-1) // 2 + 2
        else:
            a = i - (N-1) // 2
            b = i + (N-1) // 2 + 1

        #cap indices to min and max indices
        a = max(0, a)
        b = min(dim_len, b)
        out[i] = np.mean(x[a:b])
    return out


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

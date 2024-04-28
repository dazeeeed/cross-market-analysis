import utilities, os, numpy as np, tqdm, json, pandas as pd
import matplotlib.pyplot as plt

### PARAMETERS
product = "eth"

NUM_BINS = 100
x_lim_max = 7500
###

data_path = utilities.get_data_path(tree_level=2)
filename = os.path.join(data_path, f"messages-{product}.txt")



with open(filename) as file:
	line = json.loads(file.readline())
	bids = {float(price): float(amount) for price, amount in line["bids"]}
	asks = {float(price): float(amount) for price, amount in line["asks"]}

bids_prices = np.array(list(bids.keys()))
bid_mask = np.where(bids_prices > 20, True, False)
bids_prices = bids_prices[bid_mask]
bids_amount = np.array(list(bids.values()))[bid_mask]

ask_prices = np.array(list(asks.keys()))
ask_mask = np.where(ask_prices < x_lim_max, True, False)
ask_prices = ask_prices[ask_mask]
asks_amount = np.array(list(asks.values()))[ask_mask]

bids_bins = np.linspace(min(bids_prices), max(bids_prices), NUM_BINS)
bids_digitized = np.digitize(bids_prices, bids_bins)
bids_bin_means = [bids_prices[bids_digitized == i].mean() for i in range(1, len(bids_bins))]
bids_amount_sum = [bids_amount[bids_digitized == i].sum() for i in range(1, len(bids_bins))]
bids_amount_cumsum = np.cumsum(bids_amount_sum[::-1])[::-1]

asks_bins = np.linspace(min(ask_prices), max(ask_prices), NUM_BINS)
asks_digitized = np.digitize(ask_prices, asks_bins)
asks_bin_means = [ask_prices[asks_digitized == i].mean() for i in range(1, len(asks_bins))]
asks_amount_sum = [asks_amount[asks_digitized == i].sum() for i in range(1, len(asks_bins))]
asks_amount_cumsum = np.cumsum(asks_amount_sum)

plt.figure(figsize=(10, 6))
plt.plot(bids_bin_means, bids_amount_cumsum, label="Bid", drawstyle="steps")
plt.plot(asks_bin_means, asks_amount_cumsum, label="Ask", drawstyle="steps")
plt.fill_between(bids_bin_means, bids_amount_cumsum, step="pre", alpha=0.4)
plt.fill_between(asks_bin_means, asks_amount_cumsum, step="pre", alpha=0.4)

plt.xlabel('Cena')
plt.ylabel('Ilość')
plt.title('Głębokość rynku ETH')
plt.legend()
plt.xlim(left=0)
plt.ylim(bottom=0)
# plt.tight_layout()
plt.show()
import json 
from datetime import datetime, timedelta
import utilities
import os
import matplotlib.pyplot as plt
import numpy as np

### PARAMETERS
draw_chart = True
draw_moving_avg = False
draw_median = False
moving_avg_neighbors = 5
###

data_path = utilities.get_data_path(tree_level=2)
basename = "messages"
filename_btc = os.path.join(data_path, f"{basename}-btc.txt")
filename_eth = os.path.join(data_path, f"{basename}-eth.txt")

def get_timediffs(filename):
	with open(filename, "rb") as file:
		lines = [json.loads(line.decode('utf-8')) for line in file.readlines()]

	times = [line.get("time") for line in lines][1:]
	times = [datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ") for time in times][:100]

	diffs = [0]
	for i, time in enumerate(times[:-1]):
		diff = - round((time - times[i+1]) / timedelta(milliseconds=1), 1)
		diffs.append(diff)
	
	# Diffs in milliseconds, should be 50
	return times, np.array(diffs)

times_btc, diffs_btc = get_timediffs(filename_btc)
times_eth, diffs_eth = get_timediffs(filename_eth)

min_datetime = min(min(times_btc), min(times_eth))

def convert_datetimes_to_floats(times, min_datetime):
	tmp_times = [(dt - min_datetime) for dt in times]
	return np.array([tmp_time.seconds + tmp_time.microseconds / 1e6 for tmp_time in tmp_times])

times_btc = convert_datetimes_to_floats(times_btc, min_datetime)
times_eth = convert_datetimes_to_floats(times_eth, min_datetime)

if draw_chart:
	fig, ax = plt.subplots()

	if draw_moving_avg:
		diffs_btc_mov_avg = utilities.running_mean(diffs_btc, moving_avg_neighbors)
		diffs_eth_mov_avg = utilities.running_mean(diffs_eth, moving_avg_neighbors)
		ax.plot(diffs_btc_mov_avg, label="BTC")
		ax.plot(diffs_eth_mov_avg, label="ETH")
	else:
		# ax.plot(diffs_btc)
		# ax.plot(diffs_eth)
		# ax.scatter(range(len(diffs_btc)), diffs_btc)
		# ax.scatter(range(len(diffs_eth)),diffs_eth)
		ax.vlines(times_btc, ymin=-0.1, ymax=1, color="blue", label="BTC")
		ax.vlines(times_eth, ymin=-1, ymax=0.1, color="orange", label="ETH")
		# ax.axvline(times_btc, [1] * len(diffs_btc), width=0.1, label="BTC")
		# ax.axvline(times_eth, [1] * len(diffs_eth), width=0.1, label="ETH")
	
	if draw_median:
		median_btc = np.median(diffs_btc)
		median_eth = np.median(diffs_eth)

		ax.plot([0, diffs_btc.shape[0]], [median_btc for _ in range(2)])
		ax.plot([0, diffs_eth.shape[0]], [median_eth for _ in range(2)])

	plt.legend()
	plt.show()

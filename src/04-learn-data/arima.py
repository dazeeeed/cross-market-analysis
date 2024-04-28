import utilities
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller
from numpy import log
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error, mean_absolute_error
from math import sqrt
from pandas import read_csv
import multiprocessing as mp


### PARAMETERS
products = ["btc", "eth"]
# col_to_plot = "ask_price_min"
###

data_path = utilities.get_data_path(tree_level=2)
filenames = {}
dataframes = {}
scalers = {}

fig, ax = plt.subplots()

for product in products:
	filenames[product] = os.path.join(data_path, "datasets", f"{product}_stats_aligned.csv")
	dataframes[product] = pd.read_csv(filenames[product], index_col=0)

	# Normalize
	scalers[product] = MinMaxScaler()
	dataframes[product] = pd.DataFrame(scalers[product].fit_transform(dataframes[product]),
									   columns=dataframes[product].columns,
									   index=dataframes[product].index)
	
	time = dataframes[product].index
	# ax.plot(time, dataframes[product][col_to_plot])

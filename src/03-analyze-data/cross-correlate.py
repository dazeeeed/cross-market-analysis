import utilities
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from scipy.signal import correlate

### THEORETICAL SOURCES
# Cross correlation on images: 6.56 min
# https://www.youtube.com/watch?v=MQm6ZP1F6ms
#
# How to Measure a Time Delay Using Cross Correlation? (for one dim variables - signals)
# https://www.youtube.com/watch?v=L6YJqhbsuFY
#
# Page 579, Hecht Eugene, Optics
# https://emineter.files.wordpress.com/2020/04/hecht-optics-5ed.pdf

### PARAMETERS
products = ["btc", "eth"]
col_to_plot = "ask_price_min"
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

crosscorr = correlate(dataframes[products[0]][col_to_plot], dataframes[products[1]][col_to_plot])
print(len(crosscorr))

# plt.show()

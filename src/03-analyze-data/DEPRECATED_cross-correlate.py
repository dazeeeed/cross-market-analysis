import utilities
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler, StandardScaler

from scipy import signal

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
    scalers[product] = StandardScaler()
    dataframes[product] = pd.DataFrame(scalers[product].fit_transform(dataframes[product]),
                                       columns=dataframes[product].columns,
                                       index=dataframes[product].index)
    
    time = dataframes[product].index
    ax.plot(time, dataframes[product][col_to_plot], label=product.upper())

x1 = dataframes[products[0]]
x2 = dataframes[products[1]]

x1_1d = dataframes[products[0]][col_to_plot].values
x2_1d = dataframes[products[1]][col_to_plot].values

corr = signal.correlate(x1_1d, x2_1d)
lags = signal.correlation_lags(len(x1_1d), len(x2_1d))
corr /= np.max(corr)

fig, (ax_orig, ax_noise, ax_corr) = plt.subplots(3, 1)

ax_orig.plot(x1_1d)
ax_orig.set_title(f"Sygnał {products[0].upper()}")
ax_orig.set_xlim([0, 25000])

ax_noise.plot(x2_1d)
ax_noise.set_title(f"Sygnał {products[1].upper()}")
ax_noise.set_xlim([0, 25000])

ax_corr.plot(lags, corr)
# ax_corr.axhline(0.5, ls=':')
ax_corr.set_title('Korelacja wzajemna')
ax_corr.set_xlim([-25000, 25000])
ax_orig.margins(0, 0.1)
fig.tight_layout()
plt.show()

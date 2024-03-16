import utilities
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler

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
    ax.plot(time, dataframes[product][col_to_plot])

plt.show()


# correlation_matrix = df.corr()

# plot = sns.pairplot(df, diag_kind='kde')
# plt.show()

# fig, ax = plt.subplots(figsize=(8, 6))

# ax.bar(range(1, len(features) + 1),
#         explained_variance * 100,
#         alpha=0.7, 
#         label='Individual Explained Variance')

# ax.step(range(1, len(features) + 1),
#          np.cumsum(explained_variance) * 100,
#          where='mid',
#         #  marker='o', 
#         #  linestyle='-',
#          color='orange',
#          label='Cumulative Explained Variance')

# Major ticks every 20, minor ticks every 5
# major_ticks = np.arange(0, 101, 10)
# minor_ticks = np.arange(0, 101, 2)

# ax.set_xticks(major_ticks)
# ax.set_xticks(minor_ticks, minor=True)
# ax.set_yticks(major_ticks)
# ax.set_yticks(minor_ticks, minor=True)

# And a corresponding grid
# ax.grid(which='both')

# Or if you want different settings for the grids:
# ax.grid(which='minor', alpha=0.2)
# ax.grid(which='major', alpha=0.5)
# plt.xlabel("Principal Components")
# plt.ylabel("Explained Variance (%)")
# plt.title("Explained Variance Ratio")

# plt.show()
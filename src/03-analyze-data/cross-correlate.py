import utilities
import os
import numpy as np
import json
import pandas as pd
from tqdm import tqdm

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
# ???
###

data_path = utilities.get_data_path(tree_level=2)
basename_btc = f"btc"
basename_eth = f"eth"

filename_btc = os.path.join(data_path, "datasets", f"{basename_btc}_stats_aligned.csv")
filename_eth = os.path.join(data_path, "datasets", f"{basename_eth}_stats_aligned.csv")


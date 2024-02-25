# cross-market-analysis

## 01 - Collect data
Steps to collect data using websocket:
1. Run `01-collect-data/get_data_websocket.py` which creates 'messages.txt' file for all currencies.
2. (optional) Analyze the data receival times using `01-collect-data/get_times.py`
3. Split data for different currencies using `01-collect-data/split_data.py`. Note the correct messages file and output files.
4. Collect dataset statistics using `02-analyze-data/get_stats.py` for both currencies. 
5. Do a PCA for both datasets.
# cross-market-analysis

## Convention
For easier explaination a convention will be used to describe cryptocurrencies as:  
{product1} - first cryptocurrency
{product2} - second cryptocurrency

## 01 - Collect data
Steps to collect data using websocket:
1. Run `01-collect-data/get_data_websocket.py` which creates 'messages.txt' file for all currencies.
2. (optional) Analyze the data receival times using `01-collect-data/get_times.py`
3. Split data for different currencies using `01-collect-data/split_data.py`. Note the correct messages file and output files.

## 02 - Analyze data
0. REMOVE ALL LIMITATIONS TO PROCESS ONLY FIRST 1000 ROWS!
1. Collect dataset statistics using `02-analyze-data/get_stats.py` for both currencies. Datasets that will be created in this step:  
{product1}_stats.parquet  
{product1}_stats.csv  
{product2}_stats.parquet  
{product2}_stats.csv

2. Transform times from format b'%Y-%m-%dT%H:%M:%S.%fZ' to floats representing seconds with precision of 6 numbers after comma using `02-analyze-data/transform_times.py`. Datasets created in this step:
{product1}_times_transformed.csv
{product2}_times_transformed.csv  

3. Aligns two datasets with potentially different timestamps by filling missing entries with duplicates using `02-analyze-data/equalize_dataset.py`. Forward fill is used for most observations, the first observation where there is no previous record is created using backward fill. 

3. Do a PCA for both datasets.
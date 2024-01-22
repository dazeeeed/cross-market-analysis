import concurrent.futures
import requests
import json
import time
from datetime import datetime
import os
from path import get_data_path_from_src

def get_json_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def save_json_data(request_time, data, filename):
    with open(filename, 'a') as file:
        # json.dump(data, file, indent=None)
        file.write(f"{request_time} {data.get('sequence')} {data.get('time')}")
        file.write('\n')

def fetch_and_save(url, filename):
    DELAY = 1
    for i in range(10):
        request_time = time.time()
        data = get_json_data(url)

        # print(f"{start_time} --- Data requested successfully.")

        if data:
            # saving_start = time.time()
            save_json_data(request_time, data, filename)
            # print(f"Saving time: {time.time() - saving_start} s")
        else:
            print(f"Failed to fetch data from {url}.")
        
        while request_time + DELAY > time.time():
            time.sleep(0.01) 

def main():
    # Define the URLs and filenames for fetching and saving JSON data
    url1 = "https://api.exchange.coinbase.com/products/BTC-USDT/book?level=2"
    url2 = "https://api.exchange.coinbase.com/products/ETH-USDT/book?level=2"
    filename1 = os.path.join(get_data_path_from_src(), "btc-usdt")
    filename2 = os.path.join(get_data_path_from_src(), "eth-usdt")
    # fetch_and_save(url1, filename1)

    # Use ThreadPoolExecutor for parallel execution
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        # Submit tasks for fetching and saving data in parallel
        future1 = executor.submit(fetch_and_save, url1, filename1)
        executor.submit(fetch_and_save, url2, filename2)

        print(f"Result: {future1.result()}")

if __name__ == "__main__":
    main()
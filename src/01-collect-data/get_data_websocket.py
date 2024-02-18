# import websocket
# import json
# import time
# import threading

# # Define the products and the file names
# # products = ["BTC-USD", "ETH-USD"]
# # file_names = ["btc_usd.txt", "eth-usd.txt"]

# products = ["BTC-USD"]
# file_names = ["btc-usd.txt"]

# # Create a custom websocket client class
# class CoinbaseWebsocketClient(websocket.WebSocketApp):
#     def __init__(self, url, products):
#         super().__init__(url,
#                          on_open=self.on_open,
#                          on_message=self.on_message,
#                          on_error=self.on_error,
#                          on_close=self.on_close)
#         self.url = url
#         self.products = products
#         self.files = {} # A dictionary to store the file objects
#         self.data = {"type": "subscribe", "product_ids": products, "channels": ["level2_batch"]}

#     def on_open(self, ws):
#         print("Websocket opened")
#         # Subscribe to the level2_batch channel for the products
#         self.send(json.dumps(self.data))
#         # Open the files for writing
#         for product, file_name in zip(self.products, file_names):
#             self.files[product] = open(file_name, "a")

#     def on_message(self, ws, message):
#         # Parse the message as a JSON object
#         # message = json.loads(message)
#         print(type(message))
#         if message.find(b"BTC-USD") != -1:
#             pass

#         # if "changes" in message:
#         #     product = message["product_id"]
#         #     self.files[product].write(f"{message['time']}, {message['changes']}\n")
#         # elif "snapshot" in message:
#         #     product = message["product_id"]
#         #     self.files[product].write(f"{message}\n")

#     def on_error(self, ws, error):
#         print(f"ERROR: {error}")

#     def on_close(self, ws, close_status_code, close_msg):
#         print(f"{close_status_code} --- {close_msg}")
#         # Close the files
#         for file in self.files.values():
#             file.close()


# def main():
#     # Create an instance of the websocket client
#     ws = CoinbaseWebsocketClient("wss://ws-feed.pro.coinbase.com", products)
#     websocket.enableTrace(True)

    
#     try:
#         ws.run_forever(skip_utf8_validation=True)

#     except KeyboardInterrupt:
#         # Close the websocket client
#         ws.close()

    

# main()

# ===================================================
# ===================================================
# ===================================================

import websocket
import json
import time
import threading

# Define the products and the file names
# products = ["BTC-USD", "ETH-USD"]
# file_names = ["btc_usd.txt", "eth-usd.txt"]

products = ["BTC-USD"]
file_names = ["btc-usd.txt"]

# files = {} # A dictionary to store the file objects
# for product, file_name in zip(products, file_names):
#     files[product] = open(file_name, "wb")

file = open("messages-test.txt", "wb")

def on_open(ws):
    print("Websocket opened")
    # Subscribe to the level2_batch channel for the products
    ws.send(json.dumps({"type": "subscribe", "product_ids": products, "channels": ["level2_batch"]}))

def on_message(ws, message):
    file.write(message + b"\n")

def on_error(ws, error):
    print(f"ERROR: {error}")

def on_close(ws, close_status_code, close_msg):
    print(f"{close_status_code} --- {close_msg}")
    file.close()

def main1():
    # Create an instance of the websocket client
    ws = websocket.WebSocketApp("wss://ws-feed.pro.coinbase.com",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    # websocket.enableTrace(True)

    try:
        ws.run_forever(skip_utf8_validation=True)

    except KeyboardInterrupt:
        # Close the websocket client
        ws.close()

main1()
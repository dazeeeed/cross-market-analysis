import websocket
import json
import time
import threading

# Define the products and the file names
products = ["BTC-USD", "ETH-USD"]
file_names = ["btc-usd.txt"]

file = open("messages-test.txt", "wb")

def on_open(ws):
    print("Websocket opened")
    # Subscribe to the level2_batch channel for the products
    ws.send(json.dumps({"type": "subscribe",
                        "product_ids": products,
                        "channels": ["level2_batch"]}))

def on_message(ws, message):
    file.write(message + b"\n")

def on_error(ws, error):
    if type(error) != KeyboardInterrupt:
        print(f"ERROR: {error}")

def on_close(ws, close_status_code, close_msg):
    print(f"CLOSING CONNECTION! Status code: {close_status_code} --- Message: {close_msg}")
    file.close()

def main():
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

if __name__ == '__main__':
    main()
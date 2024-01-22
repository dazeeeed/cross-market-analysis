const WebSocket = require("ws");
const fs = require("fs");

const ws = new WebSocket("wss://ws-feed.pro.coinbase.com");

ws.on('error', console.error);

ws.on('open', function open() {
    ws.send(JSON.stringify({
        "type": "subscribe",
        "product_ids": [
          "BTC-USD"
        ],
        "channels": [
            "level2_batch"
        ]
      }));
});

ws.on('message', function message(data) {
    fs.appendFile('messages.txt', data + '\n', function (err) {
        if (err) throw err;
      });
});
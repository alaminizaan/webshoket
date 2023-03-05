import asyncio
import json
from flask import Flask, render_template
import websockets

app = Flask(__name__)

exchanges = [
    "wss://stream.binance.com:9443/ws/btcusdt@aggTrade",
    "wss://stream.bittrex.com/signalr/connect?transport=webSockets&clientProtocol=1.5&connectionToken=...",
    "wss://www.bitstamp.net/websocket/",
    "wss://api.gemini.com/v1/marketdata/BTCUSD",
    "wss://ws.kraken.com/",
    "wss://socket.polygon.io/crypto",
    "wss://stream.binance.us:9443/ws/btcusd@trade",
    "wss://socket.bittrex.com/signalr/connect?transport=webSockets&clientProtocol=1.5&connectionToken=...",
    "wss://ws-feed.pro.coinbase.com",
    "wss://stream.stellar.org/streams/transactions"
]

@app.route("/")
def home():
    return render_template("index.html")

async def get_prices():
    async with websockets.connect(exchanges[0]) as websocket:
        while True:
            try:
                data = await websocket.recv()
                # Parse the data and extract the price information
                # ...
                # Add the price information to a database or in-memory data structure
            except Exception as e:
                print(f"Error: {str(e)}")
                # Handle the error as necessary, such as reconnecting to the websocket

async def main():
    # Start a task for each exchange's websocket connection
    tasks = [asyncio.create_task(get_prices()) for exchange in exchanges]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
    app.run(debug=True)

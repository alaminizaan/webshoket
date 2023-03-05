import asyncio
import json
from flask import Flask, render_template
import websockets

app = Flask(__name__)

exchanges = [
    {
        "name": "Binance",
        "websocket_url": "wss://stream.binance.com:9443/ws/btcusdt@aggTrade",
        "price": None
    },
    {
        "name": "Bittrex",
        "websocket_url": "wss://stream.bittrex.com/signalr/connect?transport=webSockets&clientProtocol=1.5&connectionToken=...",
        "price": None
    },
    {
        "name": "Bitstamp",
        "websocket_url": "wss://www.bitstamp.net/websocket/",
        "price": None
    },
    {
        "name": "Gemini",
        "websocket_url": "wss://api.gemini.com/v1/marketdata/BTCUSD",
        "price": None
    },
    {
        "name": "Kraken",
        "websocket_url": "wss://ws.kraken.com/",
        "price": None
    },
    {
        "name": "Polygon",
        "websocket_url": "wss://socket.polygon.io/crypto",
        "price": None
    },
    {
        "name": "Binance US",
        "websocket_url": "wss://stream.binance.us:9443/ws/btcusd@trade",
        "price": None
    },
    {
        "name": "Bittrex 2",
        "websocket_url": "wss://socket.bittrex.com/signalr/connect?transport=webSockets&clientProtocol=1.5&connectionToken=...",
        "price": None
    },
    {
        "name": "Coinbase Pro",
        "websocket_url": "wss://ws-feed.pro.coinbase.com",
        "price": None
    },
    {
        "name": "Stellar",
        "websocket_url": "wss://stream.stellar.org/streams/transactions",
        "price": None
    }
]

@app.route("/")
def home():
    return render_template("index.html", exchanges=exchanges)

async def get_prices(exchange):
    async with websockets.connect(exchange["websocket_url"]) as websocket:
        while True:
            try:
                data = await websocket.recv()
                # Parse the data and extract the price information
                price = json.loads(data)["p"]
                # Update the exchange object with the latest price
                exchange["price"] = price
            except Exception as e:
                print(f"Error: {str(e)}")
                # Handle the error as necessary, such as reconnecting to the websocket

async def main():
    # Start a task for each exchange's websocket connection
    tasks = [asyncio.create_task(get_prices(exchange)) for exchange in exchanges]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
    app.run(debug=True)

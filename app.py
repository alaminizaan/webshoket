import asyncio
import json
from flask import Flask, render_template
import websockets

app = Flask(__name__)

exchanges = [
    {
        "name": "Binance",
        "websocket_url": "wss://stream.binance.com:9443/stream?streams=!ticker@arr",
        "prices": {}
    },
    {
        "name": "Bittrex",
        "websocket_url": "wss://socket.bittrex.com/signalr/connect?transport=webSockets&clientProtocol=1.5&connectionToken=...&connectionData=%5B%7B%22name%22%3A%22c2%22%7D%5D&tid=2",
        "prices": {}
    },
    {
        "name": "Bitstamp",
        "websocket_url": "wss://ws.bitstamp.net",
        "prices": {}
    },
    {
        "name": "Gemini",
        "websocket_url": "wss://api.gemini.com/v2/marketdata",
        "prices": {}
    },
    {
        "name": "Kraken",
        "websocket_url": "wss://ws.kraken.com/",
        "prices": {}
    },
    {
        "name": "Polygon",
        "websocket_url": "wss://socket.polygon.io/crypto",
        "prices": {}
    },
    {
        "name": "Binance US",
        "websocket_url": "wss://stream.binance.us:9443/stream?streams=!ticker@arr",
        "prices": {}
    },
    {
        "name": "Bittrex 2",
        "websocket_url": "wss://socket.bittrex.com/signalr/connect?transport=webSockets&clientProtocol=1.5&connectionToken=...&connectionData=%5B%7B%22name%22%3A%22c2%22%7D%5D&tid=2",
        "prices": {}
    },
    {
        "name": "Coinbase Pro",
        "websocket_url": "wss://ws-feed.pro.coinbase.com",
        "prices": {}
    },
    {
        "name": "Stellar",
        "websocket_url": "wss://horizon.stellar.org",
        "prices": {}
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
                # Parse the data and extract the price information for each coin pair
                ticker_data = json.loads(data)
                for ticker in ticker_data["data"]:
                    symbol = ticker["s"]
                    price = ticker["c"]
                    # Update the exchange object with the latest price for each coin pair
                    exchange["prices"][symbol] = price
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

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

# Create an empty dictionary to hold the latest prices for each exchange
latest_prices = {}

async def get_prices(exchange):
    async with websockets.connect(exchange) as websocket:
        while True:
            try:
                data = await websocket.recv()
                # Parse the data and extract the price information
                # ...
                # Add the price information to the latest_prices dictionary
                latest_prices[exchange] = price_data
            except Exception as e:
                print(f"Error: {str(e)}")
                # Handle the error as necessary, such as reconnecting to the websocket

async def main():
    # Start a task for each exchange's websocket connection
    tasks = [asyncio.create_task(get_prices(exchange)) for exchange in exchanges]
    await asyncio.gather(*tasks)

@app.route("/")
def home():
    # Build a list of dictionaries containing the latest prices for each exchange
    prices = []
    for exchange, price_data in latest_prices.items():
        prices.append({
            "exchange": exchange,
            "coin": price_data["coin"],
            "price": price_data["price"]
        })
    # Render the template with the latest prices
    return render_template("index.html", prices=prices)

if __name__ == "__main__":
    asyncio.run(main())
    app.run(debug=True)

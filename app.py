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
        "name": "Kraken",
        "websocket_url": "wss://ws.kraken.com/",
        "prices": {}
    },
    {
        "name": "KuCoin",
        "websocket_url": "wss://push1.kucoin.com/endpoint",
        "prices": {}
    },
    {
        "name": "Poloniex",
        "websocket_url": "wss://api2.poloniex.com",
        "prices": {}
    },
    {
        "name": "Mexc Global",
        "websocket_url": "wss://wspush.mexc.com/ws",
        "prices": {}
    },
    {
        "name": "Bithumb",
        "websocket_url": "wss://pubwss.bithumb.com/pub/ws",
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
                    price = ticker["p"]
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

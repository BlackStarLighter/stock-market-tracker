import requests
import json
from kafka import KafkaProducer
import os
import time

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
TOPIC = "stock_prices"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def fetch_stock(symbol: str):
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
    response = requests.get(url).json()
    price = response.get("Global Quote", {}).get("05. price", "N/A")
    producer.send(TOPIC, {"symbol": symbol, "price": price})
    print(f"Fetched stock price for {symbol}: {price}")

def fetch_historical_data(symbol: str):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
    response = requests.get(url).json()
    return response.get("Time Series (Daily)", {})

if __name__ == "__main__":
    while True:
        fetch_stock("AAPL")
        time.sleep(60)
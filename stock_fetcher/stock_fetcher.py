import requests
import json
import os
import time
from kafka import KafkaProducer

# Load environment variables
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
TOPIC = "stock_prices"

# Validate API key
if not ALPHA_VANTAGE_API_KEY:
    raise ValueError("Missing ALPHA_VANTAGE_API_KEY. Please set the environment variable.")

# Kafka producer setup
try:
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER,
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )
except Exception as e:
    raise ConnectionError(f"Failed to connect to Kafka broker: {e}")

def fetch_stock(symbol: str):
    """Fetches real-time stock price from Alpha Vantage API."""
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        price = data.get("Global Quote", {}).get("05. price")

        if price:
            producer.send(TOPIC, {"symbol": symbol, "price": price})
            print(f"Fetched stock price for {symbol}: {price}")
        else:
            print(f"Warning: No valid price data for {symbol}. Response: {data}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching stock data for {symbol}: {e}")

def fetch_historical_data(symbol: str):
    """Fetches historical stock data from Alpha Vantage API."""
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get("Time Series (Daily)", {})
    except requests.exceptions.RequestException as e:
        print(f"Error fetching historical data for {symbol}: {e}")
        return {}

if __name__ == "__main__":
    try:
        while True:
            fetch_stock("AAPL")
            time.sleep(60)  # Ensure we don't exceed API rate limits
    except KeyboardInterrupt:
        print("Script terminated by user.")
    except Exception as e:
        print(f"Unexpected error: {e}")

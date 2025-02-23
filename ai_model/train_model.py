import numpy as np
import pandas as pd
from tensorflow import keras
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
import requests
import os

# Set API Key for Alpha Vantage
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
STOCK_SYMBOL = "AAPL"

if not ALPHA_VANTAGE_API_KEY:
    raise ValueError("API Key is missing. Set ALPHA_VANTAGE_API_KEY as an environment variable.")

def fetch_historical_data(symbol):
    """Fetch historical stock price data from Alpha Vantage API."""
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}&outputsize=full"
    response = requests.get(url).json()

    if "Time Series (Daily)" not in response:
        print(f"API Error: {response}")
        raise ValueError("Invalid API response. Check API key and quota limits.")

    data = response["Time Series (Daily)"]
    df = pd.DataFrame.from_dict(data, orient="index")
    df.columns = df.columns.str.lower()
    
    df = df.rename(columns={"4. close": "Close"}).astype(float)
    df = df[["Close"]].sort_index()

    return df

# Fetch and preprocess data
df = fetch_historical_data(STOCK_SYMBOL)

scaler = MinMaxScaler(feature_range=(0, 1))
df_scaled = scaler.fit_transform(df)

# Create sequences for LSTM
sequence_length = 50
X, y = [], []
for i in range(len(df_scaled) - sequence_length):
    X.append(df_scaled[i:i+sequence_length])
    y.append(df_scaled[i+sequence_length])

X, y = np.array(X), np.array(y)
X = X.reshape(-1, sequence_length, 1)
y = y.reshape(-1, 1)

print("X shape:", X.shape, "y shape:", y.shape)

# Define LSTM model
model = Sequential([
    LSTM(50, return_sequences=True, input_shape=(sequence_length, 1)),
    LSTM(50, return_sequences=False),
    Dense(25, activation="relu"),
    Dense(1)
])

model.compile(optimizer="adam", loss="mean_squared_error")

# Train the model
model.fit(X, y, batch_size=16, epochs=10)  # Reduced batch size for small datasets

# Save the trained model
if not os.path.exists("models"):
    os.makedirs("models")
model.save("models/model.h5")
print("Model saved successfully!")

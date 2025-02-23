import numpy as np
import pandas as pd
import tensorflow as tf
import stock_fetcher.stock_fetcher as stock_fetcher
from sklearn.preprocessing import MinMaxScaler

MODEL_PATH = "ai_model/model.h5"
model = tf.keras.models.load_model(MODEL_PATH)

def predict(symbol):
    # Fetch historical data
    data = stock_fetcher.fetch_historical_data(symbol)

    # Debugging step: Check data format
    if not data:
        raise ValueError(f"No data retrieved for symbol: {symbol}")

    print("Raw Data:", data)

    # Convert API response to DataFrame
    df = pd.DataFrame.from_dict(data, orient='index')
    
    # Ensure column exists
    if '5. adjusted close' not in df.columns:
        raise KeyError(f"Column '5. adjusted close' not found in API response for {symbol}")

    df = df.rename(columns={'5. adjusted close': 'close'}).astype(float, errors='coerce')
    df = df[['close']].sort_index()

    # Compute returns for prediction
    df['return'] = df['close'].pct_change()
    df.dropna(inplace=True)

    # Ensure we have at least 10 return values
    if len(df) < 10:
        raise ValueError(f"Not enough historical data for {symbol}. At least 10 days required.")

    # Scale the return values
    scaler = MinMaxScaler(feature_range=(0, 1))
    df['scaled_return'] = scaler.fit_transform(df[['return']])

    # Prepare input for prediction (last 10 days of returns)
    recent_data = df['scaled_return'].values[-10:].reshape(1, 10, 1)

    print("Shape before prediction:", recent_data.shape)  # Debugging step

    # Make a prediction
    predicted_return = model.predict(recent_data)[0, 0]

    # Convert the predicted return back to a price estimate
    predicted_price = df['close'].iloc[-1] * (1 + predicted_return)

    return {"symbol": symbol, "predicted_price": predicted_price}


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
    
    # Convert API response to DataFrame
    df = pd.DataFrame.from_dict(data, orient='index')
    df = df.rename(columns={'5. adjusted close': 'close'}).astype(float)
    df = df[['close']].sort_index()
    
    # Compute returns for prediction
    df['return'] = df['close'].pct_change()
    df.dropna(inplace=True)

    # Scale the return values
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_returns = scaler.fit_transform(df[['return']])

    # Prepare input for prediction (last 10 days of returns)
    recent_data = scaled_returns[-10:].reshape(1, 10, 1)

    # Make a prediction
    predicted_return = model.predict(recent_data)[0, 0]

    # Convert the predicted return back to a price estimate
    predicted_price = df['close'].iloc[-1] * (1 + predicted_return)

    return {"symbol": symbol, "predicted_price": predicted_price}

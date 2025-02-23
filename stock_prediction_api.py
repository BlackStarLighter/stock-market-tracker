from fastapi import FastAPI, HTTPException
import numpy as np
import pandas as pd
import tensorflow as tf
from stock_fetcher import fetch_historical_data
from sklearn.preprocessing import MinMaxScaler

# Load the trained AI model
MODEL_PATH = "ai_model/model.h5"
try:
    model = tf.keras.models.load_model(MODEL_PATH)
except Exception as e:
    raise RuntimeError(f"Failed to load AI model: {e}")

# Initialize FastAPI app
app = FastAPI()

@app.get("/predict/")
def predict(symbol: str):
    try:
        # Fetch historical data
        data = fetch_historical_data(symbol)
        if "Time Series (Daily)" in data:
            data = data["Time Series (Daily)"]
        
        # Convert API response to DataFrame
        df = pd.DataFrame.from_dict(data, orient='index')

        # Ensure correct column naming
        if '5. adjusted close' in df.columns:
            df = df.rename(columns={'5. adjusted close': 'close'})
        elif 'adjusted close' in df.columns:
            df = df.rename(columns={'adjusted close': 'close'})
        else:
            raise ValueError("Expected column 'adjusted close' not found in data.")
        
        df = df[['close']].astype(float).sort_index()

        # Compute returns for prediction
        df['return'] = df['close'].pct_change()
        df.dropna(inplace=True)

        # Check if enough data is available
        if df.empty or len(df) < 10:
            raise ValueError("Not enough historical data to make a prediction.")

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
    
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the API with: uvicorn filename:app --reload

from fastapi import FastAPI, HTTPException
import grpc
import logging
import stock_processor.stock_pb2 as stock_pb2
import stock_processor.stock_pb2_grpc as stock_pb2_grpc
import ai_model.predict as ai_predict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/stock/{symbol}")
def get_stock(symbol: str):
    try:
        with grpc.insecure_channel("stock_processor:50051") as channel:
            stub = stock_pb2_grpc.StockServiceStub(channel)
            response = stub.GetStock(stock_pb2.StockRequest(symbol=symbol))
        return {"symbol": response.symbol, "price": response.price}
    except grpc.RpcError as e:
        logger.error(f"gRPC error: {e.code()} - {e.details()}")
        raise HTTPException(status_code=500, detail="Error fetching stock data")

@app.get("/predict/{symbol}")
def predict_stock(symbol: str):
    try:
        predicted_price = ai_predict.predict(symbol)
        return {"symbol": symbol, "predicted_price": predicted_price}
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error predicting stock price")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

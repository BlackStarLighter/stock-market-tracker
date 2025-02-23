from fastapi import FastAPI
import grpc
import stock_processor.stock_pb2 as stock_pb2
import stock_processor.stock_pb2_grpc as stock_pb2_grpc
import ai_model.predict as ai_predict

app = FastAPI()

@app.get("/stock/{symbol}")
def get_stock(symbol: str):
    with grpc.insecure_channel("stock_processor:50051") as channel:
        stub = stock_pb2_grpc.StockServiceStub(channel)
        response = stub.GetStock(stock_pb2.StockRequest(symbol=symbol))
    return {"symbol": response.symbol, "price": response.price}

@app.get("/predict/{symbol}")
def predict_stock(symbol: str):
    predicted_price = ai_predict.predict(symbol)
    return {"symbol": symbol, "predicted_price": predicted_price}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
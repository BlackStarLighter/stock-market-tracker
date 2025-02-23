import grpc
from concurrent import futures
import stock_pb2
import stock_pb2_grpc
from kafka import KafkaConsumer
import json
import os
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = "stock_db"
COLLECTION_NAME = "stocks"
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
TOPIC = "stock_prices"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

class StockService(stock_pb2_grpc.StockServiceServicer):
    def GetStock(self, request, context):
        stock = collection.find_one({"symbol": request.symbol})
        if stock:
            return stock_pb2.StockResponse(symbol=stock["symbol"], price=stock["price"])
        return stock_pb2.StockResponse(symbol=request.symbol, price=0.0)

def consume_kafka():
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=KAFKA_BROKER,
        value_deserializer=lambda m: json.loads(m.decode("utf-8"))
    )
    for message in consumer:
        collection.update_one(
            {"symbol": message.value["symbol"]},
            {"$set": {"price": message.value["price"]}},
            upsert=True
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    stock_pb2_grpc.add_StockServiceServicer_to_server(StockService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    from multiprocessing import Process
    Process(target=consume_kafka).start()
    serve()
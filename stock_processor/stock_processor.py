import grpc
from concurrent import futures
import stock_pb2
import stock_pb2_grpc
from kafka import KafkaConsumer
import json
import os
import logging
from pymongo import MongoClient
from multiprocessing import Process

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
TOPIC = "stock_prices"

# MongoDB setup
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client.get_database("stock_db")
    collection = db.get_collection("stocks")
    client.admin.command("ping")  # Check MongoDB connection
    logger.info("Connected to MongoDB successfully")
except Exception as e:
    logger.error(f"MongoDB connection error: {e}")
    exit(1)

# gRPC Service
class StockService(stock_pb2_grpc.StockServiceServicer):
    def GetStock(self, request, context):
        try:
            stock = collection.find_one({"symbol": request.symbol})
            if stock:
                return stock_pb2.StockResponse(symbol=stock["symbol"], price=stock["price"])
            return stock_pb2.StockResponse(symbol=request.symbol, price=0.0)
        except Exception as e:
            logger.error(f"Error fetching stock: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal Server Error")
            return stock_pb2.StockResponse(symbol=request.symbol, price=0.0)

# Kafka Consumer
def consume_kafka():
    try:
        consumer = KafkaConsumer(
            TOPIC,
            bootstrap_servers=KAFKA_BROKER,
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            auto_offset_reset="earliest",
            enable_auto_commit=True,
        )
        logger.info("Kafka consumer started listening")

        for message in consumer:
            stock_data = message.value
            logger.info(f"Received Kafka message: {stock_data}")
            collection.update_one(
                {"symbol": stock_data["symbol"]},
                {"$set": {"price": stock_data["price"]}},
                upsert=True
            )
    except Exception as e:
        logger.error(f"Kafka Consumer error: {e}")

# gRPC Server
def serve():
    try:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        stock_pb2_grpc.add_StockServiceServicer_to_server(StockService(), server)
        server.add_insecure_port("[::]:50051")
        server.start()
        logger.info("gRPC server started on port 50051")
        server.wait_for_termination()
    except Exception as e:
        logger.error(f"gRPC server error: {e}")
        exit(1)

if __name__ == "__main__":
    Process(target=consume_kafka, daemon=True).start()
    serve()

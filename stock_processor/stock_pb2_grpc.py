import grpc
from . import stock_pb2 as stock__pb2  # Ensure correct relative import

class StockServiceStub(object):
    """Stub for the StockService gRPC service."""

    def __init__(self, channel):
        """Initialize the gRPC client stub with a channel."""
        self.GetStock = channel.unary_unary(
            "/StockService/GetStock",
            request_serializer=stock__pb2.StockRequest.SerializeToString,
            response_deserializer=stock__pb2.StockResponse.FromString,
        )

class StockServiceServicer(object):
    """Servicer for the StockService gRPC service."""

    def GetStock(self, request, context):
        """Returns a dummy stock price for the given symbol."""
        import random
        stock_price = round(random.uniform(100, 500), 2)  # Simulated stock price
        return stock__pb2.StockResponse(symbol=request.symbol, price=stock_price)

def add_StockServiceServicer_to_server(servicer, server):
    """Registers the StockServiceServicer with the gRPC server."""
    rpc_method_handlers = {
        "GetStock": grpc.unary_unary_rpc_method_handler(
            servicer.GetStock,
            request_deserializer=stock__pb2.StockRequest.FromString,
            response_serializer=stock__pb2.StockResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "StockService", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))

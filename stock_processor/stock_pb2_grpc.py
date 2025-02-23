import grpc
from . import stock_pb2 as stock__pb2

class StockServiceStub(object):
    """Stub for the StockService gRPC service."""

    def __init__(self, channel):
        self.GetStock = channel.unary_unary(
            "/StockService/GetStock",
            request_serializer=stock__pb2.StockRequest.SerializeToString,
            response_deserializer=stock__pb2.StockResponse.FromString,
        )

class StockServiceServicer(object):
    """Servicer for the StockService gRPC service."""

    def GetStock(self, request, context):
        """Method to fetch stock price based on the symbol"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

def add_StockServiceServicer_to_server(servicer, server):
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

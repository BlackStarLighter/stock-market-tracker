from stock_processor.stock_processor import StockService
from stock_processor.stock_pb2 import StockRequest

def test_get_stock(mocker):
    mock_collection = mocker.Mock()
    mock_collection.find_one.return_value = {"symbol": "AAPL", "price": 150.0}
    service = StockService()
    response = service.GetStock(StockRequest(symbol="AAPL"), None)
    assert response.price == 150.0
import unittest
from unittest.mock import patch
from stock_processor import StockProcessor
import stock_processor.stock_pb2 as stock_pb2

class TestStockProcessor(unittest.TestCase):
    @patch('stock_processor.StockProcessor.get_stock_from_db')
    def test_get_stock_from_db(self, mock_db):
        mock_db.return_value = {'symbol': 'AAPL', 'price': 150.0}
        stock_processor = StockProcessor()
        stock = stock_processor.get_stock_from_db('AAPL')
        self.assertEqual(stock, {'symbol': 'AAPL', 'price': 150.0})

    @patch('stock_processor.StockProcessor.store_stock_data')
    def test_store_stock_data(self, mock_store):
        stock_processor = StockProcessor()
        stock_processor.store_stock_data('AAPL', 150.0)
        mock_store.assert_called_with('AAPL', 150.0)

    @patch('stock_processor.StockProcessor.GetStock')
    def test_grpc_get_stock(self, mock_grpc):
        request = stock_pb2.StockRequest(symbol='AAPL')
        mock_grpc.return_value = stock_pb2.StockResponse(symbol='AAPL', price=150.0)
        stock_processor = StockProcessor()
        response = stock_processor.GetStock(request, None)
        self.assertEqual(response.symbol, 'AAPL')
        self.assertEqual(response.price, 150.0)

if __name__ == '__main__':
    unittest.main()

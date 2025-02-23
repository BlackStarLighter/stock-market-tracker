import unittest
from unittest.mock import patch, MagicMock
from api_gateway import app as api_gateway_app
from stock_fetcher import fetch_stock_data, produce_stock_message
from stock_processor import StockProcessor
from stock_processor import stock_pb2
import grpc

class TestApiGateway(unittest.TestCase):
    def setUp(self):
        self.app = api_gateway_app.test_client()

    @patch('api_gateway.get_stock_price')
    def test_get_stock_success(self, mock_get_stock_price):
        mock_get_stock_price.return_value = {'symbol': 'AAPL', 'price': 150.0}
        response = self.app.get('/stock/AAPL')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'symbol': 'AAPL', 'price': 150.0})

    @patch('api_gateway.get_stock_price')
    def test_get_stock_not_found(self, mock_get_stock_price):
        mock_get_stock_price.return_value = None
        response = self.app.get('/stock/INVALID')
        self.assertEqual(response.status_code, 404)

class TestStockFetcher(unittest.TestCase):
    @patch('stock_fetcher.requests.get')
    def test_fetch_stock_data_success(self, mock_requests_get):
        mock_requests_get.return_value.json.return_value = {"Global Quote": {"05. price": "150.00"}}
        price = fetch_stock_data('AAPL')
        self.assertEqual(price, 150.00)

    @patch('stock_fetcher.requests.get')
    def test_fetch_stock_data_error(self, mock_requests_get):
        mock_requests_get.return_value.json.return_value = {}
        price = fetch_stock_data('INVALID')
        self.assertIsNone(price)

    @patch('stock_fetcher.produce_stock_message')
    def test_produce_stock_message(self, mock_produce):
        produce_stock_message('AAPL', 150.0)
        mock_produce.assert_called_once_with('AAPL', 150.0)

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
        mock_store.assert_called_once_with('AAPL', 150.0)

    @patch.object(StockProcessor, 'GetStock')
    def test_grpc_get_stock(self, mock_grpc):
        request = stock_pb2.StockRequest(symbol='AAPL')
        mock_grpc.return_value = stock_pb2.StockResponse(symbol='AAPL', price=150.0)
        
        stock_processor = StockProcessor()
        response = stock_processor.GetStock(request, None)

        self.assertEqual(response.symbol, 'AAPL')
        self.assertEqual(response.price, 150.0)

if __name__ == '__main__':
    unittest.main()

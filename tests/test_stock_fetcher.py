import unittest
from unittest.mock import patch
from stock_fetcher import fetch_stock_data, produce_stock_message

class TestStockFetcher(unittest.TestCase):
    @patch('stock_fetcher.requests.get')
    def test_fetch_stock_data_success(self, mock_requests_get):
        mock_requests_get.return_value.json.return_value = {'Global Quote': {'05. price': '150.00'}}
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
        mock_produce.assert_called_with('AAPL', 150.0)

if __name__ == '__main__':
    unittest.main()

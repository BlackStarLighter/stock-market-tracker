import unittest
from unittest.mock import patch
from api_gateway import app as api_gateway_app

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

if __name__ == '__main__':
    unittest.main()

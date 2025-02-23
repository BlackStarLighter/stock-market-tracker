from stock_fetcher import fetch_stock

def test_fetch_stock(mocker):
    mock_response = {"Global Quote": {"05. price": "150.00"}}
    mocker.patch("requests.get", return_value=mocker.Mock(json=lambda: mock_response))
    fetch_stock("AAPL")
    assert True  # Ensure no exceptions occurred
import unittest
from services.data_service.src.data_fetcher import fetch_historical_data

class TestDataFetcher(unittest.TestCase):
    def test_fetch_historical_data(self):
        data = fetch_historical_data('RELIANCE', '1day', '2023-01-01', '2023-12-31')
        self.assertIsNotNone(data)

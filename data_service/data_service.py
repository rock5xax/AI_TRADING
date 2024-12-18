from fetch_historical_data import fetch_historical_data
from fetch_realtime_data import fetch_realtime_data
from preprocess_data import preprocess_data
from database import MongoDB
import yaml

class DataService:
    def __init__(self, config_file):
        with open(config_file, "r") as file:
            config = yaml.safe_load(file)
        self.db = MongoDB(config["database"])

    def collect_and_store_historical_data(self, start_date, end_date, symbol):
        raw_data = fetch_historical_data(start_date, end_date, symbol)
        processed_data = preprocess_data(raw_data)
        self.db.store_data("historical_data", processed_data)

    def collect_and_store_realtime_data(self, symbol):
        raw_data = fetch_realtime_data(symbol)
        processed_data = preprocess_data(raw_data)
        self.db.store_data("realtime_data", processed_data)

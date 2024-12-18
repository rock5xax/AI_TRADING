import requests
import yaml
from utils.icici_auth_helper import get_access_token

# Load configuration
with open("config/icici_config.yaml", "r") as file:
    config = yaml.safe_load(file)

BASE_URL = config["api"]["base_url"]

class ICICIService:
    def __init__(self):
        self.client_id = config["api"]["client_id"]
        self.client_secret = config["api"]["client_secret"]
        self.app_key = config["api"]["app_key"]
        self.redirect_uri = config["api"]["redirect_uri"]
        self.access_token = get_access_token()

    def fetch_historical_data(self, stock_code, start_date, end_date):
        url = f"{BASE_URL}/historical"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        payload = {
            "stock_code": stock_code,
            "start_date": start_date,
            "end_date": end_date,
        }

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()

    def fetch_realtime_data(self, stock_code):
        url = f"{BASE_URL}/realtime"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        payload = {"stock_code": stock_code}

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()

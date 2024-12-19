import requests
import yaml
import os
from utils.icici_auth_helper import get_access_token

# Load configuration
config_path = os.path.join(os.path.dirname(__file__), "../config/icici_config.yaml")
with open(config_path, "r") as file:
    config = yaml.safe_load(file)

BASE_URL = config["api"]["base_url"]
HISTORICAL_ENDPOINT = config["api"]["endpoints"]["historical"]
REALTIME_ENDPOINT = config["api"]["endpoints"]["realtime"]

class ICICIService:
    def __init__(self):
        self.client_id = config["api"]["client_id"]
        self.client_secret = config["api"]["client_secret"]
        self.app_key = config["api"]["app_key"]
        self.redirect_uri = config["api"]["redirect_uri"]
        self.access_token = get_access_token()

    def refresh_access_token(self):
        """Refresh the access token if it expires."""
        self.access_token = get_access_token()

    def handle_response(self, response):
        """Handle API responses."""
        try:
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as e:
            return {"error": f"HTTP error occurred: {e}"}
        except Exception as e:
            return {"error": f"An unexpected error occurred: {e}"}

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

    def fetch_historical_data(self, stock_code, start_date, end_date):
        url = f"{BASE_URL}{HISTORICAL_ENDPOINT}"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        payload = {
            "stock_code": stock_code,
            "start_date": start_date,
            "end_date": end_date,
        }

        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 401:  # Unauthorized, likely token expiration
            self.refresh_access_token()
            headers["Authorization"] = f"Bearer {self.access_token}"
            response = requests.post(url, headers=headers, json=payload)

        return self.handle_response(response)

    def fetch_realtime_data(self, stock_code):
        url = f"{BASE_URL}{REALTIME_ENDPOINT}"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        payload = {"stock_code": stock_code}

        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 401:  # Unauthorized, likely token expiration
            self.refresh_access_token()
            headers["Authorization"] = f"Bearer {self.access_token}"
            response = requests.post(url, headers=headers, json=payload)

        return self.handle_response(response)

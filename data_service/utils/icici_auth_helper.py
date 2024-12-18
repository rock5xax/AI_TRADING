import requests
import yaml

# Load configuration
with open("config/icici_config.yaml", "r") as file:
    config = yaml.safe_load(file)

BASE_URL = config["api"]["base_url"]

def get_access_token():
    """
    Fetches the access token from ICICI Direct.
    """
    url = f"{BASE_URL}/oauth/token"
    payload = {
        "client_id": config["api"]["client_id"],
        "client_secret": config["api"]["client_secret"],
        "grant_type": "client_credentials",
    }

    response = requests.post(url, data=payload)
    response.raise_for_status()
    return response.json().get("access_token")

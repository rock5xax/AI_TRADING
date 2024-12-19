import requests
import yaml
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CONFIG_PATH = Path("config/icici_config.yaml")

def load_config():
    """
    Loads the configuration from the specified file.
    """
    if not CONFIG_PATH.exists():
        logger.error(f"Configuration file not found: {CONFIG_PATH}")
        raise FileNotFoundError(f"Configuration file not found: {CONFIG_PATH}")
    
    with open(CONFIG_PATH, "r") as file:
        return yaml.safe_load(file)

def get_access_token():
    """
    Fetches the access token from ICICI Direct.
    """
    try:
        config = load_config()
        base_url = config["api"]["base_url"]
        url = f"{base_url}/oauth/token"
        payload = {
            "client_id": config["api"]["client_id"],
            "client_secret": config["api"]["client_secret"],
            "grant_type": "client_credentials",
            "app_key": config["api"]["app_key"],  # New field
            "redirect_uri": config["api"]["redirect_uri"],  # New field
        }

        logger.info("Requesting access token...")
        response = requests.post(url, data=payload)
        response.raise_for_status()
        access_token = response.json().get("access_token")

        if not access_token:
            logger.error("Access token not found in response.")
            raise ValueError("Access token not found in response.")
        
        logger.info("Access token successfully retrieved.")
        return access_token

    except requests.exceptions.RequestException as e:
        logger.error(f"HTTP Request failed: {e}")
        raise

    except Exception as e:
        logger.error(f"Error fetching access token: {e}")
        raise

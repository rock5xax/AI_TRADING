# setup_dev_env.py
import os
import json
from pathlib import Path

def setup_dev_environment():
    """Set up development environment variables"""
    # Load credentials from a secure location (e.g., config file)
    config_path = Path("secure_config.json")
    
    if not config_path.exists():
        raise FileNotFoundError(
            f"Config file not found at {config_path}. "
            "Please create it with your API credentials."
        )
    
    # Load credentials
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    # Create .env file
    env_content = [
        f"BREEZE_API_KEY={config['breeze_api_key']}",
        f"BREEZE_SESSION_TOKEN={config['session_token']}"
    ]
    
    with open(".env", "w") as f:
        f.write("\n".join(env_content))
    
    print("Development environment set up successfully!")

if __name__ == "__main__":
    setup_dev_environment()
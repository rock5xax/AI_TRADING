import os
import yaml
import logging
from typing import Dict, Any
from pathlib import Path

# Initialize logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class ConfigManager:
    def __init__(self, environment: str = None):
        """
        Initialize Configuration Manager
        
        Args:
            environment (str, optional): Specific environment to load. Defaults to 'development'.
        """
        self.environment = environment or os.getenv("APP_ENV", "development")
        self._service_config_cache = {}
        self.config = self._load_configurations()
        logger.info(f"Configuration loaded for environment: {self.environment}")

    def _load_configurations(self) -> Dict[str, Any]:
        """
        Load all configuration files and merge them into a single dictionary.
        
        Returns:
            Dict[str, Any]: Merged configuration dictionary
        """
        # Base configuration
        config = self._load_yaml("config/common/base.yaml") or {}
        
        # Logging configuration
        logging_config = self._load_yaml("config/common/logging.yaml") or {}
        config["logging"] = config.get("logging", {})
        config["logging"].update(logging_config.get("logging", {}))
        
        # Environment-specific configuration
        env_config = self._load_yaml(f"config/environments/{self.environment}.yaml") or {}
        config = self._deep_merge(config, env_config)
        
        # Service-specific configurations
        service_configs = self._load_service_configs()
        config = self._deep_merge(config, service_configs)
        
        return config

    def _load_yaml(self, file_path: str) -> Dict[str, Any]:
        """
        Load a YAML configuration file and return its contents as a dictionary.
        
        Args:
            file_path (str): Path to the YAML file
        
        Returns:
            Dict[str, Any]: Configuration data
        """
        try:
            with open(file_path, "r") as file:
                logger.info(f"Loading configuration from {file_path}")
                return yaml.safe_load(file) or {}
        except FileNotFoundError:
            logger.warning(f"Configuration file not found: {file_path}")
            return {}
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML file {file_path}: {str(e)}")
            return {}

    def _load_service_configs(self) -> Dict[str, Any]:
        """
        Load service-specific configurations from `config/services`.
        
        Returns:
            Dict[str, Any]: Merged service configurations
        """
        service_config = {}
        services_dir = Path("config/services")
        
        for service_path in services_dir.glob("**/config.yaml"):
            service_name = service_path.parent.name
            config = self._load_yaml(str(service_path))
            service_config[service_name] = config
        
        return service_config

    def _deep_merge(self, base: Dict, update: Dict) -> Dict:
        """
        Recursively merge two dictionaries.
        
        Args:
            base (Dict): Base dictionary
            update (Dict): Dictionary to merge into the base
        
        Returns:
            Dict: Merged dictionary
        """
        for key, value in update.items():
            if isinstance(value, dict) and isinstance(base.get(key), dict):
                base[key] = self._deep_merge(base[key], value)
            else:
                base[key] = value
        return base

    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieve a configuration value using dot-separated keys.
        
        Args:
            key (str): Dot-separated configuration key
            default (Any, optional): Default value if the key is not found
        
        Returns:
            Any: Configuration value or default
        """
        keys = key.split(".")
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default

# Usage example
if __name__ == "__main__":
    config = ConfigManager(environment="development")
    
    # Example: Fetch Breeze API Key and Secret Key
    api_key = config.get("breeze_connector.api_key", "default_api_key")
    secret_key = config.get("breeze_connector.secret_key", "default_secret_key")
    logger.info(f"Breeze API Key: {api_key}")
    logger.info(f"Breeze Secret Key: {secret_key}")

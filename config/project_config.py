# config.py

import os
import yaml
import logging
from typing import Dict, Any
from pathlib import Path

# Initialize logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
SECURITY_MASTER_URL = "https://api.icicidirect.com/apiuser/login?api_key=YOUR_API_KEY"

class ConfigManager:
    def __init__(self,config_dir="config/environments", environment: str = None, required_keys=None):
        """
        Initialize Configuration Manager.
        
        Args:
            environment (str, optional): Specific environment to load. Defaults to 'development'.
        """
        self.config_dir = config_dir
        self.required_keys = required_keys if required_keys else []
        logging.basicConfig(level=logging.INFO)
        self.environment = environment or os.getenv("APP_ENV", "development")
        self._service_config_cache = {}
        self.config = self._load_configurations()
        logger.info(f"Configuration loaded for environment: {self.environment}")
        
        # Access Breeze API key and logging level from self.config
        api_key = self.config.get("breeze_connector.api_key", "default_api_key")
        logging_level = self.config.get("logging.level", "INFO")
        logger.info(f"Breeze API Key: {api_key}")
        logger.info(f"Logging Level: {logging_level}")

    def load_config(self, env=None):
        """Load configuration based on the environment."""
        env = env or os.getenv("APP_ENV", "development")
        config_path = os.path.join(self.config_dir, f"{env}.yaml")

        try:
            with open(config_path, 'r') as file:
                config = yaml.safe_load(file)
            
            # Validate configuration keys
            missing_keys = [key for key in self.required_keys if key not in config]
            if missing_keys:
                raise Exception(f"Missing required configuration keys: {missing_keys}")

            logging.info(f"Successfully loaded configuration for environment: {env}")
            return config

        except FileNotFoundError:
            logging.error(f"Configuration file {config_path} not found.")
            raise Exception(f"Configuration file {config_path} not found.")
        except yaml.YAMLError as e:
            logging.error(f"Error parsing YAML configuration: {e}")
            raise Exception(f"Error parsing YAML configuration: {e}")
        except Exception as e:
            logging.error(f"Configuration loading failed: {e}")
            raise

    # def load_config(self, env="development"):
    #     """Load configuration based on the environment."""
    #     config_path = os.path.join(self.config_dir, f"{env}.yaml")
    #     try:
    #         with open(config_path, 'r') as file:
    #             config = yaml.safe_load(file)
    #         return config
    #     except FileNotFoundError:
    #         raise Exception(f"Configuration file {config_path} not found.")
    #     except yaml.YAMLError as e:
    #         raise Exception(f"Error parsing YAML configuration: {e}")


    def _load_configurations(self) -> Dict[str, Any]:
        """
        Load and merge all configuration files into a single dictionary.
        
        Returns:
            Dict[str, Any]: Merged configuration dictionary.
        """
        config = {}

        # Load base configuration
        config = self._deep_merge(config, self._load_yaml("config/common/base.yaml"))

        # Load logging configuration
        logging_config = self._load_yaml("config/common/logging.yaml")
        if logging_config:
            config.setdefault("logging", {}).update(logging_config.get("logging", {}))

        # Load environment-specific configuration
        env_config = self._load_yaml(f"config/environments/{self.environment}.yaml")
        config = self._deep_merge(config, env_config)

        # Load service-specific configurations
        service_configs = self._load_service_configs()
        config = self._deep_merge(config, service_configs)

        # Load ICICI Direct API configuration
        icici_config = self._load_icici_direct_config()
        if icici_config:
            config["icicidirect"] = icici_config

        return config

    def _load_yaml(self, file_path: str) -> Dict[str, Any]:
        """
        Load a YAML configuration file and return its contents as a dictionary.
        
        Args:
            file_path (str): Path to the YAML file.
        
        Returns:
            Dict[str, Any]: Parsed configuration data or an empty dictionary if the file doesn't exist.
        """
        try:
            with open(file_path, "r") as file:
                logger.info(f"Loading configuration from {file_path}")
                return yaml.safe_load(file) or {}
        except FileNotFoundError:
            logger.warning(f"Configuration file not found: {file_path}")
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML file {file_path}: {str(e)}")
        return {}

    def _load_service_configs(self) -> Dict[str, Any]:
        """
        Load service-specific configurations from `config/services`.
        
        Returns:
            Dict[str, Any]: Merged service configurations.
        """
        service_config = {}
        services_dir = Path("config/services")
        
        if services_dir.exists():
            for service_path in services_dir.glob("**/config.yaml"):
                service_name = service_path.parent.name
                config = self._load_yaml(str(service_path))
                if config:
                    service_config[service_name] = config
        else:
            logger.warning(f"Services directory does not exist: {services_dir}")
        
        return service_config

    def _load_icici_direct_config(self) -> Dict[str, Any]:
        """
        Load ICICIDirect API configuration from a secure location.
        
        Returns:
            Dict[str, Any]: ICICIDirect API configuration.
        """
        icici_config_path = Path("config/credentials.json")
        
        try:
            with icici_config_path.open("r") as file:
                logger.info(f"Loading ICICIDirect API configuration from {icici_config_path}")
                return yaml.safe_load(file) or {}
        except FileNotFoundError:
            logger.error(f"ICICIDirect API credentials file not found: {icici_config_path}")
        except yaml.YAMLError as e:
            logger.error(f"Error parsing ICICIDirect API credentials file: {str(e)}")
        return {}

    def _deep_merge(self, base: Dict, update: Dict) -> Dict:
        """
        Recursively merge two dictionaries.
        
        Args:
            base (Dict): Base dictionary.
            update (Dict): Dictionary to merge into the base.
        
        Returns:
            Dict: Merged dictionary.
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
            key (str): Dot-separated configuration key.
            default (Any, optional): Default value if the key is not found.
        
        Returns:
            Any: Configuration value or the default.
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
    config_manager = ConfigManager(environment="development")
    
    # Access configuration values
    api_key = config_manager.get("breeze_connector.api_key", "default_api_key")
    secret_key = config_manager.get("breeze_connector.secret_key", "default_secret_key")
    
    logger.info(f"Breeze API Key: {api_key}")
    logger.info(f"Breeze Secret Key: {secret_key}")

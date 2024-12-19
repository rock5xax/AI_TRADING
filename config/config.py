# config/config.py
import os
import yaml
import logging
from typing import Dict, Any
from pathlib import Path

# Initialize logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class ConfigManager:
    def __init__(self, environment: str = None):
        """
        Initialize Configuration Manager
        
        Args:
            environment (str, optional): Specific environment to load
        """
        # Determine environment
        self.environment = environment or os.getenv('APP_ENV', 'development')
        self._service_config_cache = {}
        self.config = self._load_configurations()
        logger.info(f"Configuration loaded for environment: {self.environment}")


    
    def _load_configurations(self) -> Dict[str, Any]:
        """
        Load all configuration files
        
        Returns:
            Dict[str, Any]: Merged configuration dictionary
        """
        # Base configurations
        config = self._load_yaml('config/common/base.yaml')
        
        # Logging configuration
        logging_config = self._load_yaml('config/common/logging.yaml')
        config['logging'].update(logging_config.get('logging', {}))
        
        # Environment-specific configuration
        env_config = self._load_yaml(f'config/environments/{self.environment}.yaml')
        config = self._deep_merge(config, env_config)
        
        # Service-specific configurations
        service_configs = self._load_service_configs()
        config = self._deep_merge(config, service_configs)
        
        return config
    
    def _load_yaml(self, file_path: str) -> Dict[str, Any]:
        """
        Load YAML configuration file
        
        Args:
            file_path (str): Path to YAML file
        
        Returns:
            Dict[str, Any]: Configuration dictionary
        """
        try:
            with open(file_path, 'r') as file:
                return yaml.safe_load(file) or {}
        except FileNotFoundError:
            print(f"Warning: Configuration file not found - {file_path}")
            return {}
    
    def _load_service_configs(self) -> Dict[str, Any]:
        """
        Load service-specific configurations
        
        Returns:
            Dict[str, Any]: Merged service configurations
        """
        service_config = {}
        services_dir = Path('config/services')
        
        for service_path in services_dir.glob('**/config.yaml'):
            service_name = service_path.parent.name
            config = self._load_yaml(str(service_path))
            service_config[service_name] = config
        
        return service_config
    
    def _deep_merge(self, base: Dict, update: Dict) -> Dict:
        """
        Recursively merge two dictionaries
        
        Args:
            base (Dict): Base dictionary
            update (Dict): Dictionary to merge
        
        Returns:
            Dict: Merged dictionary
        """
        for key, value in update.items():
            if isinstance(value, dict):
                base[key] = self._deep_merge(base.get(key, {}), value)
            else:
                base[key] = value
        return base
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieve configuration value
        
        Args:
            key (str): Dot-separated configuration key
            default (Any, optional): Default value if key not found
        
        Returns:
            Any: Configuration value
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value or default

# Usage example
config = ConfigManager(environment='development')
api_key = config.get('data_service.api_credentials.breeze.key_placeholder')
stocks = config.get('data_service.stocks_to_fetch', ['RELIANCE'])
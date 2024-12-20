import os
from typing import Dict, Any
import yaml
from cryptography.fernet import Fernet
import logging

# Initialize logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class SecretsManager:
    def __init__(self, environment: str = 'development'):
        """
        Initialize Secrets Manager
        
        Args:
            environment (str): Environment to load secrets for
        """
        self.environment = environment
        self.secrets_path = f'config/.secrets/{environment}.yaml'
        self.encryption_key = self._get_encryption_key()
        self.cipher_suite = Fernet(self.encryption_key)
        logger.info(f"Secrets Manager initialized for environment: {self.environment}")

    def _get_encryption_key(self) -> bytes:
        """
        Retrieve or generate encryption key.
        
        Returns:
            bytes: Encryption key
        """
        key = os.getenv('ENCRYPTION_KEY')
        if not key:
            logger.warning("ENCRYPTION_KEY environment variable not set. Generating a new key.")
            key = Fernet.generate_key()
            logger.info("New encryption key generated. Store this key securely.")
            # For development, you can persist the key (DO NOT DO THIS IN PRODUCTION)
            os.environ['ENCRYPTION_KEY'] = key.decode()
        return key.encode() if isinstance(key, str) else key

    def get_secret(self, secret_path: str) -> Any:
        """
        Retrieve and decrypt a secret from the secrets file.
        
        Args:
            secret_path (str): Dot-separated path to the secret.
        
        Returns:
            Any: Decrypted secret value.
        """
        try:
            with open(self.secrets_path, 'r') as file:
                secrets = yaml.safe_load(file)
        except FileNotFoundError:
            logger.error(f"Secrets file not found: {self.secrets_path}")
            return None
        except yaml.YAMLError as e:
            logger.error(f"Error reading secrets file: {e}")
            return None

        # Navigate through nested dictionary
        keys = secret_path.split('.')
        secret = secrets
        for key in keys:
            secret = secret.get(key)
            if secret is None:
                logger.warning(f"Secret path not found: {secret_path}")
                return None

        # Decrypt if encrypted
        if isinstance(secret, str) and secret.startswith('encrypted:'):
            encrypted_value = secret.split(':', 1)[1]
            try:
                decrypted_value = self.cipher_suite.decrypt(encrypted_value.encode()).decode()
                return decrypted_value
            except Exception as e:
                logger.error(f"Error decrypting secret: {e}")
                return None

        return secret

    def set_secret(self, secret_path: str, value: Any) -> None:
        """
        Encrypt and store a secret in the secrets file.
        
        Args:
            secret_path (str): Dot-separated path to the secret.
            value (Any): Value to store.
        """
        try:
            # Load existing secrets or create a new dictionary
            try:
                with open(self.secrets_path, 'r') as file:
                    secrets = yaml.safe_load(file) or {}
            except FileNotFoundError:
                secrets = {}

            # Navigate to the right location and set the value
            keys = secret_path.split('.')
            secret = secrets
            for key in keys[:-1]:
                secret = secret.setdefault(key, {})
            encrypted_value = f"encrypted:{self.cipher_suite.encrypt(str(value).encode()).decode()}"
            secret[keys[-1]] = encrypted_value

            # Save the updated secrets file
            with open(self.secrets_path, 'w') as file:
                yaml.dump(secrets, file)
            logger.info(f"Secret saved at path: {secret_path}")

        except Exception as e:
            logger.error(f"Error setting secret: {e}")

# Usage example
if __name__ == "__main__":
    manager = SecretsManager(environment="development")

    # Set a new secret
    manager.set_secret("icicidirect.api_key", "your_api_key")
    manager.set_secret("icicidirect.api_secret", "your_api_secret")
    manager.set_secret("icicidirect.access_token", "your_access_token")

    # Retrieve a secret
    api_key = manager.get_secret("icicidirect.api_key")
    api_secret = manager.get_secret("icicidirect.api_secret")
    access_token = manager.get_secret("icicidirect.access_token")

    logger.info(f"ICICI Direct API Key: {api_key}")
    logger.info(f"ICICI Direct API Secret: {api_secret}")
    logger.info(f"ICICI Direct Access Token: {access_token}")

# config/secrets_manager.py
import os
from typing import Dict, Any
import yaml
from cryptography.fernet import Fernet

class SecretsManager:
    def __init__(self, environment: str = 'development'):
        """
        Initialize Secrets Manager
        
        Args:
            environment (str): Environment to load secrets for
        """
        self.environment = environment
        self.secrets_path = f'config/.secrets/{environment}.json'
        self.encryption_key = self._get_encryption_key()
        self.cipher_suite = Fernet(self.encryption_key)
    
    def _get_encryption_key(self) -> bytes:
        """
        Retrieve or generate encryption key
        
        Returns:
            bytes: Encryption key
        """
        key = os.getenv('ENCRYPTION_KEY')
        if not key:
            key = Fernet.generate_key()
            os.environ['ENCRYPTION_KEY'] = key.decode()
        return key.encode() if isinstance(key, str) else key
    
    def get_secret(self, secret_path: str) -> Any:
        """
        Retrieve and decrypt a secret
        
        Args:
            secret_path (str): Path to secret in secrets file
        
        Returns:
            Any: Decrypted secret value
        """
        with open(self.secrets_path, 'r') as file:
            secrets = yaml.safe_load(file)
        
        # Navigate through nested dictionary
        keys = secret_path.split('.')
        secret = secrets
        for key in keys:
            secret = secret.get(key)
            if secret is None:
                return None
        
        # Decrypt if encrypted
        if isinstance(secret, str) and secret.startswith('encrypted:'):
            encrypted_value = secret.split(':', 1)[1]
            decrypted_value = self.cipher_suite.decrypt(encrypted_value.encode()).decode()
            return decrypted_value
        
        return secret
import os
import json
import logging
from typing import Dict, Any, Optional, List
from breeze_connect import BreezeConnect
from datetime import datetime, timedelta
from pathlib import Path
from breeze_connect import BreezeConnect
from config.config import BREEZE_API_KEY, BREEZE_API_SECRET, BREEZE_API_BASE_URL


def initialize_breeze():
    breeze = BreezeConnect(api_key=BREEZE_API_KEY)
    breeze.generate_session(api_secret=BREEZE_API_SECRET)
    return breeze

class BreezeConnector:
    """A connector class for the Breeze API with enhanced functionality and error handling."""
    
    VALID_INTERVALS = ['1minute', '5minute', '15minute', '30minute', '1day']
    
    def __init__(self, config_path: str):
        """
        Initialize Breeze API Connection
        
        Args:
            config_path (str): Path to configuration file
            
        Raises:
            FileNotFoundError: If config file doesn't exist
            ValueError: If config file is missing required fields
            ConnectionError: If API connection fails
        """
        self.logger = self._setup_logger()
        self.config_path = Path(config_path)
        self.connected = False
        self._load_config()
        self._initialize_connection()
        
    @staticmethod
    def _setup_logger() -> logging.Logger:
        """Set up logging configuration."""
        logger = logging.getLogger(__name__)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger

    def _load_config(self) -> None:
        """
        Load and validate configuration from secure file
        
        Raises:
            FileNotFoundError: If config file doesn't exist
            ValueError: If config file is missing required fields
        """
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found at {self.config_path}")
            
        try:
            with open(self.config_path, 'r') as config_file:
                self.config = json.load(config_file)
                
            required_fields = ['breeze_api_key', 'session_token']
            missing_fields = [field for field in required_fields 
                            if field not in self.config]
            
            if missing_fields:
                raise ValueError(
                    f"Missing required fields in config: {', '.join(missing_fields)}"
                )
                
            self.logger.info("Configuration loaded successfully")
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in config file: {e}")
            raise ValueError("Config file contains invalid JSON") from e
        except Exception as e:
            self.logger.error(f"Configuration loading failed: {e}")
            raise

    def _initialize_connection(self) -> None:
        """
        Initialize Breeze API connection
        
        Raises:
            ConnectionError: If API connection fails
        """
        try:
            self.api = BreezeConnect(
                api_key=self.config['breeze_api_key']
            )
            self.api.generate_session(
                api_key=self.config['breeze_api_key'],
                session_token=self.config['session_token']
            )
            self.connected = True
            self.logger.info("Breeze API connection established successfully")
            
        except Exception as e:
            self.logger.error(f"API Connection Failed: {e}")
            raise ConnectionError(f"Failed to connect to Breeze API: {e}")

    def _validate_dates(
        self,
        start_date: Optional[datetime],
        end_date: Optional[datetime]
    ) -> tuple[datetime, datetime]:
        """
        Validate and process date parameters
        
        Args:
            start_date: Start date for data retrieval
            end_date: End date for data retrieval
            
        Returns:
            tuple[datetime, datetime]: Processed start and end dates
            
        Raises:
            ValueError: If dates are invalid
        """
        if not start_date:
            start_date = datetime.now() - timedelta(days=365)
        if not end_date:
            end_date = datetime.now()
            
        if start_date > end_date:
            raise ValueError("Start date cannot be after end date")
            
        if start_date > datetime.now():
            raise ValueError("Start date cannot be in the future")
            
        return start_date, end_date

    def _validate_interval(self, interval: str) -> None:
        """
        Validate the time interval
        
        Args:
            interval: Time interval for data
            
        Raises:
            ValueError: If interval is invalid
        """
        if interval not in self.VALID_INTERVALS:
            raise ValueError(
                f"Invalid interval. Must be one of: {', '.join(self.VALID_INTERVALS)}"
            )

    def fetch_historical_data(
        self, 
        stock_code: str, 
        start_date: Optional[datetime] = None, 
        end_date: Optional[datetime] = None,
        interval: str = '1day'
    ) -> Dict[str, Any]:
        """
        Fetch historical stock data
        
        Args:
            stock_code: Stock symbol
            start_date: Start date for data retrieval
            end_date: End date for data retrieval
            interval: Data interval ('1minute', '5minute', '15minute', '30minute', '1day')
        
        Returns:
            Dict[str, Any]: Historical market data
            
        Raises:
            ConnectionError: If not connected to API
            ValueError: If parameters are invalid
        """
        if not self.connected:
            raise ConnectionError("Not connected to Breeze API")
            
        if not stock_code:
            raise ValueError("Stock code cannot be empty")
            
        try:
            # Validate parameters
            self._validate_interval(interval)
            start_date, end_date = self._validate_dates(start_date, end_date)
            
            # Fetch data
            self.logger.info(
                f"Fetching data for {stock_code} from {start_date.date()} "
                f"to {end_date.date()} ({interval})"
            )
            
            historical_data = self.api.get_historical_data(
                stock_code=stock_code,
                interval=interval,
                from_date=start_date.strftime('%Y-%m-%d'),
                to_date=end_date.strftime('%Y-%m-%d'),
                exchange="NSE"  # Can be made configurable if needed
            )
            
            if not historical_data:
                self.logger.warning(f"No data received for {stock_code}")
                return {}
                
            return historical_data
            
        except Exception as e:
            self.logger.error(f"Data fetch error for {stock_code}: {e}")
            return {}

    def get_quote(self, stock_code: str) -> Dict[str, Any]:
        """
        Get current market quote for a stock
        
        Args:
            stock_code: Stock symbol
            
        Returns:
            Dict[str, Any]: Current market quote
        """
        if not self.connected:
            raise ConnectionError("Not connected to Breeze API")
            
        try:
            quote = self.api.get_quotes(
                stock_code=stock_code,
                exchange="NSE"  # Can be made configurable if needed
            )
            return quote or {}
        except Exception as e:
            self.logger.error(f"Quote fetch error for {stock_code}: {e}")
            return {}

    def disconnect(self) -> None:
        """
        Safely disconnect from the Breeze API
        """
        if self.connected:
            try:
                self.api.logout()
                self.connected = False
                self.logger.info("Disconnected from Breeze API")
            except Exception as e:
                self.logger.error(f"Error during disconnect: {e}")

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.disconnect()
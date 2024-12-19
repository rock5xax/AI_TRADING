import asyncio
import logging
from .breeze_connector import BreezeConnector
from .data_fetcher import DataFetcher
from .preprocessor import DataPreprocessor
from .storage import DataStorage

class DataService:
    def __init__(self, config_path: str, mongodb_uri: str):
        """
        Initialize Data Service
        
        Args:
            config_path (str): Path to configuration file
            mongodb_uri (str): MongoDB connection string
        """
        self.breeze_connector = BreezeConnector(config_path)
        self.data_fetcher = DataFetcher(self.breeze_connector)
        self.storage = DataStorage(mongodb_uri)
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    async def run_data_pipeline(self, stock_codes: list):
        """
        Complete data processing pipeline
        
        Args:
            stock_codes (list): List of stock symbols
        """
        try:
            # Fetch raw data
            raw_data = self.data_fetcher.fetch_multiple_stocks(stock_codes)
            
            # Preprocess data
            processed_data = DataPreprocessor.preprocess_stock_data(raw_data)
            
            # Store processed data
            await self.storage.store_processed_data(processed_data)
            
            self.logger.info("Data pipeline completed successfully")
        except Exception as e:
            self.logger.error(f"Data pipeline failed: {e}")

def main():
    config_path = 'common/config/secrets.json'
    mongodb_uri = 'mongodb://localhost:27017'
    stock_codes = ['RELIANCE', 'NIFTY', 'INFY', 'HDFCBANK']
    
    service = DataService(config_path, mongodb_uri)
    
    # Run async event loop
    asyncio.run(service.run_data_pipeline(stock_codes))

if __name__ == "__main__":
    main()
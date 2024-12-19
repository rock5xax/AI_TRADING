# data_fetcher.py

import pandas as pd
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import logging
import sys
import os

# Add the parent directory to sys.path to enable absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.breeze_connector import BreezeConnector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataFetcher:
    def __init__(self, breeze_connector: BreezeConnector):
        self.connector = breeze_connector

    def fetch_multiple_stocks(
        self,
        stock_codes: List[str],
        interval: str = "1minute",
        days: int = 30,
        include_today: bool = True
    ) -> Dict[str, Optional[pd.DataFrame]]:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        stock_data = {}
        for stock in stock_codes:
            try:
                logger.info(f"Fetching data for {stock}")
                raw_data = self.connector.get_historical_data(
                    stock_code=stock,
                    interval=interval,
                    from_date=start_date.strftime("%Y-%m-%d"),
                    to_date=end_date.strftime("%Y-%m-%d")
                )
                
                if raw_data:
                    stock_data[stock] = pd.DataFrame(raw_data)
                else:
                    logger.warning(f"No data received for {stock}")
                    stock_data[stock] = None
                    
            except Exception as e:
                logger.error(f"Error fetching data for {stock}: {str(e)}")
                stock_data[stock] = None
                
        return stock_data

def main():
    # Example usage
    breeze = BreezeConnector()
    fetcher = DataFetcher(breeze)
    
    try:
        # Example stocks
        stocks = ["RELIANCE", "TCS", "INFY"]
        
        # Fetch data
        data = fetcher.fetch_multiple_stocks(stocks, days=5)
        
        # Print results
        for stock, df in data.items():
            if df is not None:
                print(f"\n{stock} data shape: {df.shape}")
            else:
                print(f"\nNo data available for {stock}")
                
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")

if __name__ == "__main__":
    main()
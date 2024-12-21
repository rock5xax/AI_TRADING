import logging
import sys
import os
from pathlib import Path
from typing import List, Dict, Optional

# Add the project root directory to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from services.data_service.src.breeze_connector import BreezeConnector
from services.data_service.src.data_fetcher import DataFetcher
from services.data_service.src.data_processor import DataProcessor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        # Initialize components
        connector = BreezeConnector()
        fetcher = DataFetcher(connector)
        
        # List of stocks to analyze
        stocks = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK"]
        
        # Fetch data
        logger.info("Fetching stock data...")
        stock_data = fetcher.fetch_multiple_stocks(stocks)
        
        # Process data
        logger.info("Processing stock data...")
        processed_data = DataProcessor.process_stock_data(stock_data)
        
        # Analyze each stock
        for stock, df in processed_data.items():
            if df is not None and not df.empty:
                logger.info(f"\nAnalyzing {stock}:")
                
                # Get last closing price
                last_close = df['close'].iloc[-1]
                logger.info(f"Last Close: {last_close:.2f}")
                
                # Get trading signals
                signals = DataProcessor.get_last_signals(df)
                logger.info("Trading Signals:")
                for indicator, signal in signals.items():
                    logger.info(f"  {indicator}: {signal}")
            else:
                logger.warning(f"No data available for {stock}")
        
    except Exception as e:
        logger.error(f"Error in main: {e}")
    finally:
        if 'connector' in locals():
            connector.disconnect()

if __name__ == "__main__":
    main()
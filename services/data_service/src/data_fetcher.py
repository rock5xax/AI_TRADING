import pandas as pd
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import logging


# Local imports
from src.breeze_connector import BreezeConnector

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class DataFetcher:
    def __init__(self, breeze_connector: BreezeConnector):
        self.connector = breeze_connector

    @staticmethod
    def format_date(date: datetime) -> str:
        """
        Format a datetime object to a string in 'YYYY-MM-DD' format.
        """
        return date.strftime("%Y-%m-%d")

    def fetch_multiple_stocks(
        self,
        stock_codes: List[str],
        interval: str = "1minute",
        days: int = 30,
        include_today: bool = True,
    ) -> Dict[str, Optional[pd.DataFrame]]:
        """
        Fetch historical data for multiple stocks.

        Args:
            stock_codes (List[str]): List of stock codes to fetch data for.
            interval (str): Time interval for historical data (e.g., '1minute', '1day').
            days (int): Number of days of data to fetch.
            include_today (bool): Whether to include today's data.

        Returns:
            Dict[str, Optional[pd.DataFrame]]: Dictionary with stock codes as keys and DataFrames as values.
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        stock_data = {}
        for stock in stock_codes:
            try:
                logger.info(f"Fetching data for {stock}")
                raw_data = self.connector.get_historical_data(
                    stock_code=stock,
                    interval=interval,
                    from_date=self.format_date(start_date),
                    to_date=self.format_date(end_date),
                )

                if raw_data:
                    stock_data[stock] = pd.DataFrame(raw_data)
                    logger.info(f"Data for {stock} fetched successfully: {len(raw_data)} rows")
                else:
                    logger.warning(f"No data received for {stock}")
                    stock_data[stock] = None
            except Exception as e:
                logger.error(f"Error fetching data for {stock}: {str(e)}")
                stock_data[stock] = None

        return stock_data


def main():
    """
    Main function for standalone execution.
    """
    breeze = BreezeConnector()  # Ensure credentials are set up in BreezeConnector
    fetcher = DataFetcher(breeze)

    try:
        # Example stocks
        stocks = ["RELIANCE", "TCS", "INFY"]

        # Fetch data
        data = fetcher.fetch_multiple_stocks(stocks, interval="1day", days=5)

        # Print results
        for stock, df in data.items():
            if df is not None:
                print(f"\n{stock} data shape: {df.shape}")
                print(df.head())  # Preview first few rows
            else:
                print(f"\nNo data available for {stock}")
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")


if __name__ == "__main__":
    main()

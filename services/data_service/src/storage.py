import os
import motor.motor_asyncio
import pandas as pd
from typing import Dict

class DataStorage:
    def __init__(self, mongodb_uri: str, database_name: str = 'trading_data'):
        """
        Initialize MongoDB connection
        
        Args:
            mongodb_uri (str): MongoDB connection string
            database_name (str): Database name
        """
        self.client = motor.motor_asyncio.AsyncIOMotorClient(mongodb_uri)
        self.db = self.client[database_name]

    async def store_processed_data(self, processed_data: Dict[str, pd.DataFrame]):
        """
        Store processed stock data in MongoDB
        
        Args:
            processed_data (Dict[str, pd.DataFrame]): Processed stock data
        """
        for symbol, df in processed_data.items():
            collection = self.db[f'processed_{symbol}']
            records = df.to_dict('records')
            await collection.insert_many(records)
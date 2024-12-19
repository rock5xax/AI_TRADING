import pandas as pd
import numpy as np
from typing import Dict

class DataPreprocessor:
    @staticmethod
    def preprocess_stock_data(stock_data: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
        """
        Advanced data preprocessing
        
        Args:
            stock_data (Dict[str, pd.DataFrame]): Raw stock data
        
        Returns:
            Dict[str, pd.DataFrame]: Processed stock data
        """
        processed_data = {}
        for symbol, df in stock_data.items():
            processed_df = DataPreprocessor._process_single_stock(df)
            processed_data[symbol] = processed_df
        return processed_data

    @staticmethod
    def _process_single_stock(df: pd.DataFrame) -> pd.DataFrame:
        """
        Process single stock dataframe
        
        Args:
            df (pd.DataFrame): Raw stock dataframe
        
        Returns:
            pd.DataFrame: Processed dataframe
        """
        # Calculate returns
        df['return'] = df['close'].pct_change()
        
        # Technical indicators
        df['ma_50'] = df['close'].rolling(window=50).mean()
        df['ma_200'] = df['close'].rolling(window=200).mean()
        df['rsi'] = DataPreprocessor._calculate_rsi(df['close'])
        
        # Volatility
        df['volatility'] = df['return'].rolling(window=20).std()
        
        return df.dropna()

    @staticmethod
    def _calculate_rsi(prices: pd.Series, periods: int = 14) -> pd.Series:
        """
        Calculate Relative Strength Index (RSI)
        
        Args:
            prices (pd.Series): Price series
            periods (int): RSI calculation period
        
        Returns:
            pd.Series: RSI values
        """
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
"""
DataFetcher class for retrieving financial market data
Supports multiple data sources including Yahoo Finance, Alpha Vantage, etc.
"""
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import logging


class DataFetcher:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def fetch_yahoo_data(self, symbol, start_date=None, end_date=None, interval="1d"):
        """
        Fetch historical data from Yahoo Finance
        
        Args:
            symbol (str): Stock symbol (e.g., 'AAPL', 'GOOGL')
            start_date (str): Start date in 'YYYY-MM-DD' format
            end_date (str): End date in 'YYYY-MM-DD' format
            interval (str): Data interval ('1d', '1wk', '1mo', etc.)
        
        Returns:
            pd.DataFrame: Historical price data
        """
        try:
            if not start_date:
                start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
            if not end_date:
                end_date = datetime.now().strftime('%Y-%m-%d')
                
            ticker = yf.Ticker(symbol)
            data = ticker.history(start=start_date, end=end_date, interval=interval)
            
            if data.empty:
                raise ValueError(f"No data found for symbol {symbol}")
            
            # Add symbol column
            data['Symbol'] = symbol
            
            self.logger.info(f"Fetched {len(data)} records for {symbol} from {start_date} to {end_date}")
            return data
            
        except Exception as e:
            self.logger.error(f"Error fetching data for {symbol}: {str(e)}")
            raise
    
    def fetch_multiple_symbols(self, symbols, start_date=None, end_date=None, interval="1d"):
        """
        Fetch data for multiple symbols
        
        Args:
            symbols (list): List of stock symbols
            start_date (str): Start date in 'YYYY-MM-DD' format
            end_date (str): End date in 'YYYY-MM-DD' format
            interval (str): Data interval
        
        Returns:
            dict: Dictionary with symbol as key and DataFrame as value
        """
        data_dict = {}
        for symbol in symbols:
            data_dict[symbol] = self.fetch_yahoo_data(symbol, start_date, end_date, interval)
        return data_dict

    def get_stock_info(self, symbol):
        """
        Get basic information about a stock
        
        Args:
            symbol (str): Stock symbol
        
        Returns:
            dict: Basic company information
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            return {
                'symbol': symbol,
                'company_name': info.get('longName', info.get('shortName', symbol)),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A'),
                'market_cap': info.get('marketCap', 'N/A'),
                'pe_ratio': info.get('trailingPE', 'N/A')
            }
        except Exception as e:
            self.logger.error(f"Error getting info for {symbol}: {str(e)}")
            return {'symbol': symbol, 'error': str(e)}
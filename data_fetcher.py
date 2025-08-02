import yfinance as yf
import pandas as pd
import logging
import json
from datetime import datetime, timedelta

class DataFetcher:
    def __init__(self, config_file='config.json'):
        """Initialize data fetcher with configuration."""
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        self.stocks = self.config['trading']['stocks']
        self.lookback_days = self.config['trading']['lookback_days']
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def fetch_stock_data(self, symbol):
        """Fetch historical data for a single stock."""
        try:
            self.logger.info(f"Fetching data for {symbol}")
            
            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=self.lookback_days)
            
            # Fetch data using yfinance
            stock = yf.Ticker(symbol)
            data = stock.history(start=start_date, end=end_date)
            
            if data.empty:
                self.logger.warning(f"No data fetched for {symbol}")
                return None
            
            self.logger.info(f"Successfully fetched {len(data)} records for {symbol}")
            return data
            
        except Exception as e:
            self.logger.error(f"Error fetching data for {symbol}: {str(e)}")
            return None
    
    def fetch_all_stocks_data(self):
        """Fetch data for all configured stocks."""
        stock_data = {}
        
        for symbol in self.stocks:
            data = self.fetch_stock_data(symbol)
            if data is not None:
                stock_data[symbol] = data
        
        self.logger.info(f"Fetched data for {len(stock_data)} stocks")
        return stock_data

if __name__ == "__main__":
    # Test the data fetcher
    fetcher = DataFetcher()
    data = fetcher.fetch_all_stocks_data()
    print(f"Fetched data for {len(data)} stocks") 
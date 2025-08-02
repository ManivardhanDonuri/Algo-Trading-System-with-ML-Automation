import yfinance as yf
import pandas as pd
import logging
from datetime import datetime, timedelta
import json

class DataFetcher:
    def __init__(self, config_file='config.json'):
        """Initialize the data fetcher with configuration."""
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
            
            # Download data
            stock = yf.Ticker(symbol)
            data = stock.history(start=start_date, end=end_date)
            
            if data.empty:
                self.logger.warning(f"No data found for {symbol}")
                return None
            
            self.logger.info(f"Successfully fetched {len(data)} records for {symbol}")
            return data
            
        except Exception as e:
            self.logger.error(f"Error fetching data for {symbol}: {str(e)}")
            return None
    
    def fetch_all_stocks_data(self):
        """Fetch data for all configured stocks."""
        all_data = {}
        
        for symbol in self.stocks:
            data = self.fetch_stock_data(symbol)
            if data is not None:
                all_data[symbol] = data
        
        self.logger.info(f"Fetched data for {len(all_data)} stocks")
        return all_data
    
    def get_data_summary(self, data_dict):
        """Get summary statistics for all stocks."""
        summary = {}
        
        for symbol, data in data_dict.items():
            if data is not None and not data.empty:
                summary[symbol] = {
                    'start_date': data.index[0].strftime('%Y-%m-%d'),
                    'end_date': data.index[-1].strftime('%Y-%m-%d'),
                    'total_records': len(data),
                    'current_price': data['Close'].iloc[-1],
                    'price_change': data['Close'].iloc[-1] - data['Close'].iloc[0],
                    'price_change_pct': ((data['Close'].iloc[-1] / data['Close'].iloc[0]) - 1) * 100
                }
        
        return summary

if __name__ == "__main__":
    # Test the data fetcher
    fetcher = DataFetcher()
    data = fetcher.fetch_all_stocks_data()
    summary = fetcher.get_data_summary(data)
    
    print("Data Summary:")
    for symbol, info in summary.items():
        print(f"{symbol}: {info['total_records']} records, "
              f"Price: ₹{info['current_price']:.2f}, "
              f"Change: {info['price_change_pct']:.2f}%") 
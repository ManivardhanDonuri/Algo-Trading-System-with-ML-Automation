import pandas as pd
import pandas_ta as ta
import numpy as np
import logging
import json

class TechnicalIndicators:
    def __init__(self, config_file='config.json'):
        """Initialize technical indicators calculator with configuration."""
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        self.rsi_period = self.config['trading']['rsi_period']
        self.sma_short = self.config['trading']['sma_short']
        self.sma_long = self.config['trading']['sma_long']
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def calculate_indicators(self, data):
        """Calculate RSI and moving averages for given data."""
        if data is None or data.empty:
            self.logger.warning("No data provided for indicator calculation")
            return None
        
        try:
            # Create a copy to avoid modifying original data
            df = data.copy()
            
            # Calculate RSI
            df['RSI'] = ta.rsi(df['Close'], length=self.rsi_period)
            
            # Calculate Simple Moving Averages
            df['SMA_20'] = ta.sma(df['Close'], length=self.sma_short)
            df['SMA_50'] = ta.sma(df['Close'], length=self.sma_long)
            
            # Calculate SMA crossover
            df['SMA_Crossover'] = np.where(df['SMA_20'] > df['SMA_50'], 1, 0)
            df['SMA_Crossover_Change'] = df['SMA_Crossover'].diff()
            
            # Remove NaN values
            df = df.dropna()
            
            self.logger.info(f"Calculated indicators for {len(df)} records")
            return df
            
        except Exception as e:
            self.logger.error(f"Error calculating indicators: {str(e)}")
            return None
    
    def calculate_all_indicators(self, data_dict):
        """Calculate indicators for all stocks."""
        indicators_data = {}
        
        for symbol, data in data_dict.items():
            if data is not None:
                indicators = self.calculate_indicators(data)
                if indicators is not None:
                    indicators_data[symbol] = indicators
        
        self.logger.info(f"Calculated indicators for {len(indicators_data)} stocks")
        return indicators_data
    
    def get_current_indicators(self, indicators_data):
        """Get current indicator values for all stocks."""
        current_indicators = {}
        
        for symbol, data in indicators_data.items():
            if data is not None and not data.empty:
                latest = data.iloc[-1]
                current_indicators[symbol] = {
                    'rsi': latest['RSI'],
                    'sma_20': latest['SMA_20'],
                    'sma_50': latest['SMA_50'],
                    'price': latest['Close'],
                    'volume': latest['Volume'],
                    'sma_crossover': latest['SMA_Crossover'],
                    'date': latest.name.strftime('%Y-%m-%d')
                }
        
        return current_indicators
    
    def validate_indicators(self, indicators_data):
        """Validate that indicators are calculated correctly."""
        validation_results = {}
        
        for symbol, data in indicators_data.items():
            if data is not None:
                # Check for NaN values
                nan_count = data[['RSI', 'SMA_20', 'SMA_50']].isna().sum()
                
                # Check RSI range
                rsi_range = (data['RSI'].min(), data['RSI'].max())
                
                validation_results[symbol] = {
                    'total_records': len(data),
                    'nan_count': nan_count.to_dict(),
                    'rsi_range': rsi_range,
                    'is_valid': nan_count.sum() == 0 and 0 <= rsi_range[0] <= 100 and 0 <= rsi_range[1] <= 100
                }
        
        return validation_results

if __name__ == "__main__":
    # Test the technical indicators
    from data_fetcher import DataFetcher
    
    # Fetch data
    fetcher = DataFetcher()
    data = fetcher.fetch_all_stocks_data()
    
    # Calculate indicators
    indicators = TechnicalIndicators()
    indicators_data = indicators.calculate_all_indicators(data)
    
    # Get current indicators
    current = indicators.get_current_indicators(indicators_data)
    
    print("Current Indicators:")
    for symbol, info in current.items():
        print(f"{symbol}: RSI={info['rsi']:.2f}, "
              f"SMA20=₹{info['sma_20']:.2f}, "
              f"SMA50=₹{info['sma_50']:.2f}, "
              f"Price=₹{info['price']:.2f}") 
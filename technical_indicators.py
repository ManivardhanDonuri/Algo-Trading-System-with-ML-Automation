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
        """Calculate RSI and moving averages for a single stock."""
        try:
            if data is None or data.empty:
                return None
            
            # Calculate RSI
            data['RSI'] = ta.rsi(data['Close'], length=self.rsi_period)
            
            # Calculate Simple Moving Averages
            data['SMA_20'] = ta.sma(data['Close'], length=self.sma_short)
            data['SMA_50'] = ta.sma(data['Close'], length=self.sma_long)
            
            # Calculate SMA crossover signals
            data['SMA_Crossover'] = np.where(
                (data['SMA_20'] > data['SMA_50']) & 
                (data['SMA_20'].shift(1) <= data['SMA_50'].shift(1)), 
                1,  # Bullish crossover
                np.where(
                    (data['SMA_20'] < data['SMA_50']) & 
                    (data['SMA_20'].shift(1) >= data['SMA_50'].shift(1)), 
                    -1,  # Bearish crossover
                    0   # No crossover
                )
            )
            
            # Remove NaN values
            data = data.dropna()
            
            self.logger.info(f"Calculated indicators for {len(data)} records")
            return data
            
        except Exception as e:
            self.logger.error(f"Error calculating indicators: {str(e)}")
            return None
    
    def calculate_all_indicators(self, stock_data):
        """Calculate indicators for all stocks."""
        indicators_data = {}
        
        for symbol, data in stock_data.items():
            indicators = self.calculate_indicators(data)
            if indicators is not None:
                indicators_data[symbol] = indicators
        
        self.logger.info(f"Calculated indicators for {len(indicators_data)} stocks")
        return indicators_data
    
    def get_current_indicators(self, indicators_data):
        """Get current indicator values for signal generation."""
        current_indicators = {}
        
        for symbol, data in indicators_data.items():
            if data is not None and not data.empty:
                latest = data.iloc[-1]
                current_indicators[symbol] = {
                    'rsi': latest['RSI'],
                    'sma_20': latest['SMA_20'],
                    'sma_50': latest['SMA_50'],
                    'close': latest['Close'],
                    'date': latest.name.strftime('%Y-%m-%d')
                }
        
        return current_indicators

if __name__ == "__main__":
    # Test the technical indicators
    import yfinance as yf
    from datetime import datetime, timedelta
    
    # Get sample data
    stock = yf.Ticker("RELIANCE.NS")
    data = stock.history(start=datetime.now() - timedelta(days=180), end=datetime.now())
    
    # Calculate indicators
    indicators = TechnicalIndicators()
    result = indicators.calculate_indicators(data)
    
    if result is not None:
        print(f"Calculated indicators for {len(result)} records")
        print(f"Latest RSI: {result.iloc[-1]['RSI']:.2f}")
        print(f"Latest SMA_20: {result.iloc[-1]['SMA_20']:.2f}")
        print(f"Latest SMA_50: {result.iloc[-1]['SMA_50']:.2f}") 
import pandas as pd
import logging
import json
from datetime import datetime

class SignalGenerator:
    def __init__(self, config_file='config.json'):
        """Initialize signal generator with configuration."""
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        self.rsi_oversold = self.config['trading']['rsi_oversold']
        self.rsi_overbought = self.config['trading']['rsi_overbought']
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def generate_signals(self, indicators_data):
        """Generate trading signals for all stocks."""
        all_signals = {}
        
        for symbol, data in indicators_data.items():
            if data is not None and not data.empty:
                signals = self._generate_stock_signals(symbol, data)
                if signals:
                    all_signals[symbol] = signals
        
        self.logger.info(f"Generated signals for {len(all_signals)} stocks")
        return all_signals
    
    def _generate_stock_signals(self, symbol, data):
        """Generate signals for a single stock."""
        signals = []
        
        for i in range(1, len(data)):  # Start from 1 to check crossovers
            current = data.iloc[i]
            previous = data.iloc[i-1]
            
            # Check for BUY signal
            if (current['RSI'] < self.rsi_oversold and 
                current['SMA_Crossover'] == 1):
                
                signal = {
                    'type': 'BUY',
                    'date': current.name.strftime('%Y-%m-%d'),
                    'price': current['Close'],
                    'rsi': current['RSI'],
                    'sma_20': current['SMA_20'],
                    'sma_50': current['SMA_50'],
                    'reason': f"RSI oversold ({current['RSI']:.2f}) and SMA crossover bullish"
                }
                signals.append(signal)
            
            # Check for SELL signal
            elif (current['RSI'] > self.rsi_overbought and 
                  current['SMA_Crossover'] == -1):
                
                signal = {
                    'type': 'SELL',
                    'date': current.name.strftime('%Y-%m-%d'),
                    'price': current['Close'],
                    'rsi': current['RSI'],
                    'sma_20': current['SMA_20'],
                    'sma_50': current['SMA_50'],
                    'reason': f"RSI overbought ({current['RSI']:.2f}) and SMA crossover bearish"
                }
                signals.append(signal)
        
        return signals
    
    def check_current_signals(self, current_indicators):
        """Check for current trading signals."""
        current_signals = {}
        
        for symbol, indicators in current_indicators.items():
            rsi = indicators['rsi']
            sma_20 = indicators['sma_20']
            sma_50 = indicators['sma_50']
            close = indicators['close']
            date = indicators['date']
            
            # Check for BUY signal
            if rsi < self.rsi_oversold and sma_20 > sma_50:
                current_signals[symbol] = {
                    'type': 'BUY',
                    'date': date,
                    'price': close,
                    'rsi': rsi,
                    'reason': f"RSI oversold ({rsi:.2f}) and SMA crossover bullish"
                }
            
            # Check for SELL signal
            elif rsi > self.rsi_overbought and sma_20 < sma_50:
                current_signals[symbol] = {
                    'type': 'SELL',
                    'date': date,
                    'price': close,
                    'rsi': rsi,
                    'reason': f"RSI overbought ({rsi:.2f}) and SMA crossover bearish"
                }
        
        return current_signals

if __name__ == "__main__":
    # Test the signal generator
    import yfinance as yf
    from datetime import datetime, timedelta
    from technical_indicators import TechnicalIndicators
    
    # Get sample data
    stock = yf.Ticker("RELIANCE.NS")
    data = stock.history(start=datetime.now() - timedelta(days=180), end=datetime.now())
    
    # Calculate indicators
    indicators = TechnicalIndicators()
    indicators_data = indicators.calculate_indicators(data)
    
    # Generate signals
    signal_gen = SignalGenerator()
    signals = signal_gen._generate_stock_signals("RELIANCE.NS", indicators_data)
    
    print(f"Generated {len(signals)} signals")
    for signal in signals:
        print(f"{signal['type']} at {signal['date']}: ₹{signal['price']:.2f} - {signal['reason']}") 
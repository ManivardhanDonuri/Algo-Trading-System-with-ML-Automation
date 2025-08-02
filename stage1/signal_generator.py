import pandas as pd
import numpy as np
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
        
        try:
            for i in range(1, len(data)):  # Start from 1 to compare with previous day
                current = data.iloc[i]
                previous = data.iloc[i-1]
                
                # Check for buy signal: RSI < 30 AND 20-DMA crosses above 50-DMA
                buy_condition = (
                    current['RSI'] < self.rsi_oversold and
                    previous['SMA_Crossover'] == 0 and
                    current['SMA_Crossover'] == 1
                )
                
                # Check for sell signal: RSI > 70 AND 20-DMA crosses below 50-DMA
                sell_condition = (
                    current['RSI'] > self.rsi_overbought and
                    previous['SMA_Crossover'] == 1 and
                    current['SMA_Crossover'] == 0
                )
                
                if buy_condition:
                    signal = {
                        'date': current.name.strftime('%Y-%m-%d'),
                        'type': 'BUY',
                        'price': current['Close'],
                        'rsi': current['RSI'],
                        'sma_20': current['SMA_20'],
                        'sma_50': current['SMA_50'],
                        'volume': current['Volume']
                    }
                    signals.append(signal)
                    self.logger.info(f"BUY signal for {symbol} on {signal['date']} at ₹{signal['price']:.2f}")
                
                elif sell_condition:
                    signal = {
                        'date': current.name.strftime('%Y-%m-%d'),
                        'type': 'SELL',
                        'price': current['Close'],
                        'rsi': current['RSI'],
                        'sma_20': current['SMA_20'],
                        'sma_50': current['SMA_50'],
                        'volume': current['Volume']
                    }
                    signals.append(signal)
                    self.logger.info(f"SELL signal for {symbol} on {signal['date']} at ₹{signal['price']:.2f}")
        
        except Exception as e:
            self.logger.error(f"Error generating signals for {symbol}: {str(e)}")
        
        return signals
    
    def get_recent_signals(self, all_signals, days=7):
        """Get signals from the last N days."""
        recent_signals = {}
        cutoff_date = datetime.now().date() - pd.Timedelta(days=days)
        
        for symbol, signals in all_signals.items():
            recent = []
            for signal in signals:
                signal_date = datetime.strptime(signal['date'], '%Y-%m-%d').date()
                if signal_date >= cutoff_date:
                    recent.append(signal)
            
            if recent:
                recent_signals[symbol] = recent
        
        return recent_signals
    
    def get_signal_summary(self, all_signals):
        """Get summary statistics for all signals."""
        summary = {}
        
        for symbol, signals in all_signals.items():
            buy_signals = [s for s in signals if s['type'] == 'BUY']
            sell_signals = [s for s in signals if s['type'] == 'SELL']
            
            summary[symbol] = {
                'total_signals': len(signals),
                'buy_signals': len(buy_signals),
                'sell_signals': len(sell_signals),
                'last_buy': buy_signals[-1] if buy_signals else None,
                'last_sell': sell_signals[-1] if sell_signals else None,
                'avg_buy_price': np.mean([s['price'] for s in buy_signals]) if buy_signals else 0,
                'avg_sell_price': np.mean([s['price'] for s in sell_signals]) if sell_signals else 0
            }
        
        return summary
    
    def check_current_signals(self, current_indicators):
        """Check if current market conditions meet signal criteria."""
        current_signals = {}
        
        for symbol, indicators in current_indicators.items():
            signal = None
            
            # Check for buy signal
            if (indicators['rsi'] < self.rsi_oversold and 
                indicators['sma_crossover'] == 1):
                signal = {
                    'type': 'BUY',
                    'reason': f"RSI oversold ({indicators['rsi']:.2f}) and SMA crossover bullish"
                }
            
            # Check for sell signal
            elif (indicators['rsi'] > self.rsi_overbought and 
                  indicators['sma_crossover'] == 0):
                signal = {
                    'type': 'SELL',
                    'reason': f"RSI overbought ({indicators['rsi']:.2f}) and SMA crossover bearish"
                }
            
            if signal:
                signal.update({
                    'symbol': symbol,
                    'price': indicators['price'],
                    'rsi': indicators['rsi'],
                    'sma_20': indicators['sma_20'],
                    'sma_50': indicators['sma_50'],
                    'date': indicators['date']
                })
                current_signals[symbol] = signal
        
        return current_signals

if __name__ == "__main__":
    # Test the signal generator
    from data_fetcher import DataFetcher
    from technical_indicators import TechnicalIndicators
    
    # Fetch data and calculate indicators
    fetcher = DataFetcher()
    data = fetcher.fetch_all_stocks_data()
    
    indicators = TechnicalIndicators()
    indicators_data = indicators.calculate_all_indicators(data)
    
    # Generate signals
    signal_gen = SignalGenerator()
    all_signals = signal_gen.generate_signals(indicators_data)
    
    # Get summary
    summary = signal_gen.get_signal_summary(all_signals)
    
    print("Signal Summary:")
    for symbol, info in summary.items():
        print(f"{symbol}: {info['total_signals']} signals "
              f"({info['buy_signals']} buy, {info['sell_signals']} sell)")
    
    # Check current signals
    current_indicators = indicators.get_current_indicators(indicators_data)
    current_signals = signal_gen.check_current_signals(current_indicators)
    
    if current_signals:
        print("\nCurrent Signals:")
        for symbol, signal in current_signals.items():
            print(f"{symbol}: {signal['type']} - {signal['reason']}")
    else:
        print("\nNo current signals") 
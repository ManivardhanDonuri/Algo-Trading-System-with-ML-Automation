import pandas as pd
import numpy as np
import logging
import json
from datetime import datetime

class Backtester:
    def __init__(self, config_file='config.json'):
        """Initialize backtester with configuration."""
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def run_backtest(self, indicators_data, signals_data):
        """Run backtest for all stocks."""
        backtest_results = {}
        
        for symbol in indicators_data.keys():
            if symbol in signals_data and indicators_data[symbol] is not None:
                result = self._backtest_stock(symbol, indicators_data[symbol], signals_data[symbol])
                if result:
                    backtest_results[symbol] = result
        
        self.logger.info(f"Completed backtest for {len(backtest_results)} stocks")
        return backtest_results
    
    def _backtest_stock(self, symbol, data, signals):
        """Run backtest for a single stock."""
        try:
            trades = []
            position = None
            entry_price = 0
            entry_date = None
            
            # Sort signals by date
            sorted_signals = sorted(signals, key=lambda x: x['date'])
            
            for signal in sorted_signals:
                if signal['type'] == 'BUY' and position is None:
                    # Open long position
                    position = 'LONG'
                    entry_price = signal['price']
                    entry_date = signal['date']
                    self.logger.info(f"BUY {symbol} at ₹{entry_price:.2f} on {entry_date}")
                
                elif signal['type'] == 'SELL' and position == 'LONG':
                    # Close long position
                    exit_price = signal['price']
                    exit_date = signal['date']
                    
                    # Calculate trade metrics
                    pnl = exit_price - entry_price
                    pnl_pct = (pnl / entry_price) * 100
                    holding_days = (datetime.strptime(exit_date, '%Y-%m-%d') - 
                                  datetime.strptime(entry_date, '%Y-%m-%d')).days
                    
                    trade = {
                        'symbol': symbol,
                        'entry_date': entry_date,
                        'exit_date': exit_date,
                        'entry_price': entry_price,
                        'exit_price': exit_price,
                        'pnl': pnl,
                        'pnl_pct': pnl_pct,
                        'holding_days': holding_days,
                        'is_win': pnl > 0
                    }
                    trades.append(trade)
                    
                    self.logger.info(f"SELL {symbol} at ₹{exit_price:.2f} on {exit_date}, "
                                   f"P&L: ₹{pnl:.2f} ({pnl_pct:.2f}%)")
                    
                    # Reset position
                    position = None
                    entry_price = 0
                    entry_date = None
            
            # Calculate performance metrics
            if trades:
                return self._calculate_performance_metrics(trades)
            else:
                self.logger.warning(f"No completed trades for {symbol}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error in backtest for {symbol}: {str(e)}")
            return None
    
    def _calculate_performance_metrics(self, trades):
        """Calculate performance metrics for completed trades."""
        total_trades = len(trades)
        winning_trades = len([t for t in trades if t['is_win']])
        losing_trades = total_trades - winning_trades
        
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        
        total_pnl = sum(t['pnl'] for t in trades)
        total_pnl_pct = sum(t['pnl_pct'] for t in trades)
        
        avg_win = np.mean([t['pnl'] for t in trades if t['is_win']]) if winning_trades > 0 else 0
        avg_loss = np.mean([t['pnl'] for t in trades if not t['is_win']]) if losing_trades > 0 else 0
        
        max_win = max([t['pnl'] for t in trades]) if trades else 0
        max_loss = min([t['pnl'] for t in trades]) if trades else 0
        
        avg_holding_days = np.mean([t['holding_days'] for t in trades])
        
        # Calculate cumulative returns
        cumulative_pnl = 0
        cumulative_returns = []
        for trade in trades:
            cumulative_pnl += trade['pnl']
            cumulative_returns.append(cumulative_pnl)
        
        return {
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate': win_rate,
            'total_pnl': total_pnl,
            'total_pnl_pct': total_pnl_pct,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'max_win': max_win,
            'max_loss': max_loss,
            'avg_holding_days': avg_holding_days,
            'cumulative_returns': cumulative_returns,
            'trades': trades
        }
    
    def get_portfolio_summary(self, backtest_results):
        """Calculate portfolio-wide performance metrics."""
        if not backtest_results:
            return None
        
        all_trades = []
        for symbol, result in backtest_results.items():
            all_trades.extend(result['trades'])
        
        if not all_trades:
            return None
        
        # Portfolio metrics
        total_trades = len(all_trades)
        winning_trades = len([t for t in all_trades if t['is_win']])
        total_pnl = sum(t['pnl'] for t in all_trades)
        total_pnl_pct = sum(t['pnl_pct'] for t in all_trades)
        
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        avg_pnl_per_trade = total_pnl / total_trades if total_trades > 0 else 0
        
        # Calculate Sharpe ratio (simplified)
        returns = [t['pnl_pct'] for t in all_trades]
        sharpe_ratio = np.mean(returns) / np.std(returns) if np.std(returns) > 0 else 0
        
        return {
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'win_rate': win_rate,
            'total_pnl': total_pnl,
            'total_pnl_pct': total_pnl_pct,
            'avg_pnl_per_trade': avg_pnl_per_trade,
            'sharpe_ratio': sharpe_ratio,
            'symbols_traded': len(backtest_results)
        }
    
    def export_trades_to_dataframe(self, backtest_results):
        """Export all trades to a pandas DataFrame."""
        all_trades = []
        
        for symbol, result in backtest_results.items():
            for trade in result['trades']:
                all_trades.append(trade)
        
        if all_trades:
            df = pd.DataFrame(all_trades)
            df['entry_date'] = pd.to_datetime(df['entry_date'])
            df['exit_date'] = pd.to_datetime(df['exit_date'])
            return df
        else:
            return pd.DataFrame()

if __name__ == "__main__":
    # Test the backtester
    from data_fetcher import DataFetcher
    from technical_indicators import TechnicalIndicators
    from signal_generator import SignalGenerator
    
    # Fetch data and calculate indicators
    fetcher = DataFetcher()
    data = fetcher.fetch_all_stocks_data()
    
    indicators = TechnicalIndicators()
    indicators_data = indicators.calculate_all_indicators(data)
    
    # Generate signals
    signal_gen = SignalGenerator()
    all_signals = signal_gen.generate_signals(indicators_data)
    
    # Run backtest
    backtester = Backtester()
    results = backtester.run_backtest(indicators_data, all_signals)
    
    # Print results
    print("Backtest Results:")
    for symbol, result in results.items():
        print(f"\n{symbol}:")
        print(f"  Total Trades: {result['total_trades']}")
        print(f"  Win Rate: {result['win_rate']:.2f}%")
        print(f"  Total P&L: ₹{result['total_pnl']:.2f} ({result['total_pnl_pct']:.2f}%)")
        print(f"  Avg Win: ₹{result['avg_win']:.2f}")
        print(f"  Avg Loss: ₹{result['avg_loss']:.2f}")
    
    # Portfolio summary
    portfolio_summary = backtester.get_portfolio_summary(results)
    if portfolio_summary:
        print(f"\nPortfolio Summary:")
        print(f"  Total Trades: {portfolio_summary['total_trades']}")
        print(f"  Portfolio Win Rate: {portfolio_summary['win_rate']:.2f}%")
        print(f"  Total P&L: ₹{portfolio_summary['total_pnl']:.2f}")
        print(f"  Sharpe Ratio: {portfolio_summary['sharpe_ratio']:.2f}") 
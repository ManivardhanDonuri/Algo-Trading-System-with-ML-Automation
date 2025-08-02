import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import logging
from datetime import datetime
import json

class Visualizer:
    def __init__(self, config_file='config.json'):
        """Initialize visualizer with configuration."""
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Set style
        plt.style.use('seaborn-v0_8')
    
    def plot_stock_with_signals(self, symbol, data, signals, save_path=None):
        """Plot stock price with buy/sell signals."""
        try:
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10), height_ratios=[3, 1])
            
            # Plot price and moving averages
            ax1.plot(data.index, data['Close'], label='Close Price', linewidth=2, color='black')
            ax1.plot(data.index, data['SMA_20'], label='20-DMA', linewidth=1.5, color='blue', alpha=0.7)
            ax1.plot(data.index, data['SMA_50'], label='50-DMA', linewidth=1.5, color='red', alpha=0.7)
            
            # Plot buy signals
            buy_signals = [s for s in signals if s['type'] == 'BUY']
            if buy_signals:
                buy_dates = [datetime.strptime(s['date'], '%Y-%m-%d') for s in buy_signals]
                buy_prices = [s['price'] for s in buy_signals]
                ax1.scatter(buy_dates, buy_prices, color='green', marker='^', s=100, 
                           label='Buy Signal', zorder=5)
            
            # Plot sell signals
            sell_signals = [s for s in signals if s['type'] == 'SELL']
            if sell_signals:
                sell_dates = [datetime.strptime(s['date'], '%Y-%m-%d') for s in sell_signals]
                sell_prices = [s['price'] for s in sell_signals]
                ax1.scatter(sell_dates, sell_prices, color='red', marker='v', s=100, 
                           label='Sell Signal', zorder=5)
            
            ax1.set_title(f'{symbol} - Price Chart with Trading Signals', fontsize=14, fontweight='bold')
            ax1.set_ylabel('Price (₹)', fontsize=12)
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            
            # Plot RSI
            ax2.plot(data.index, data['RSI'], label='RSI', linewidth=2, color='purple')
            ax2.axhline(y=70, color='red', linestyle='--', alpha=0.7, label='Overbought (70)')
            ax2.axhline(y=30, color='green', linestyle='--', alpha=0.7, label='Oversold (30)')
            ax2.fill_between(data.index, 70, 100, alpha=0.3, color='red')
            ax2.fill_between(data.index, 0, 30, alpha=0.3, color='green')
            
            ax2.set_title('RSI Indicator', fontsize=12, fontweight='bold')
            ax2.set_ylabel('RSI', fontsize=12)
            ax2.set_xlabel('Date', fontsize=12)
            ax2.legend()
            ax2.grid(True, alpha=0.3)
            ax2.set_ylim(0, 100)
            
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                self.logger.info(f"Chart saved to {save_path}")
            
            plt.show()
            
        except Exception as e:
            self.logger.error(f"Error plotting stock chart: {str(e)}")
    
    def plot_portfolio_performance(self, backtest_results, save_path=None):
        """Plot portfolio performance metrics."""
        try:
            if not backtest_results:
                self.logger.warning("No backtest results to plot")
                return
            
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
            
            # Extract data
            symbols = list(backtest_results.keys())
            total_pnl = [backtest_results[s]['total_pnl'] for s in symbols]
            win_rates = [backtest_results[s]['win_rate'] for s in symbols]
            total_trades = [backtest_results[s]['total_trades'] for s in symbols]
            avg_holding_days = [backtest_results[s]['avg_holding_days'] for s in symbols]
            
            # Plot 1: Total P&L by symbol
            colors = ['green' if pnl >= 0 else 'red' for pnl in total_pnl]
            bars1 = ax1.bar(symbols, total_pnl, color=colors, alpha=0.7)
            ax1.set_title('Total P&L by Symbol', fontsize=12, fontweight='bold')
            ax1.set_ylabel('P&L (₹)', fontsize=10)
            ax1.tick_params(axis='x', rotation=45)
            
            # Add value labels on bars
            for bar, pnl in zip(bars1, total_pnl):
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height,
                        f'₹{pnl:.0f}', ha='center', va='bottom' if height >= 0 else 'top')
            
            # Plot 2: Win Rate by symbol
            bars2 = ax2.bar(symbols, win_rates, color='skyblue', alpha=0.7)
            ax2.set_title('Win Rate by Symbol', fontsize=12, fontweight='bold')
            ax2.set_ylabel('Win Rate (%)', fontsize=10)
            ax2.tick_params(axis='x', rotation=45)
            ax2.set_ylim(0, 100)
            
            # Add value labels on bars
            for bar, rate in zip(bars2, win_rates):
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height,
                        f'{rate:.1f}%', ha='center', va='bottom')
            
            # Plot 3: Total Trades by symbol
            bars3 = ax3.bar(symbols, total_trades, color='orange', alpha=0.7)
            ax3.set_title('Total Trades by Symbol', fontsize=12, fontweight='bold')
            ax3.set_ylabel('Number of Trades', fontsize=10)
            ax3.tick_params(axis='x', rotation=45)
            
            # Add value labels on bars
            for bar, trades in zip(bars3, total_trades):
                height = bar.get_height()
                ax3.text(bar.get_x() + bar.get_width()/2., height,
                        f'{trades}', ha='center', va='bottom')
            
            # Plot 4: Average Holding Days by symbol
            bars4 = ax4.bar(symbols, avg_holding_days, color='purple', alpha=0.7)
            ax4.set_title('Average Holding Days by Symbol', fontsize=12, fontweight='bold')
            ax4.set_ylabel('Days', fontsize=10)
            ax4.tick_params(axis='x', rotation=45)
            
            # Add value labels on bars
            for bar, days in zip(bars4, avg_holding_days):
                height = bar.get_height()
                ax4.text(bar.get_x() + bar.get_width()/2., height,
                        f'{days:.1f}', ha='center', va='bottom')
            
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                self.logger.info(f"Portfolio performance chart saved to {save_path}")
            
            plt.show()
            
        except Exception as e:
            self.logger.error(f"Error plotting portfolio performance: {str(e)}")
    
    def plot_cumulative_returns(self, backtest_results, save_path=None):
        """Plot cumulative returns over time."""
        try:
            if not backtest_results:
                self.logger.warning("No backtest results to plot")
                return
            
            fig, ax = plt.subplots(figsize=(15, 8))
            
            for symbol, result in backtest_results.items():
                if result['cumulative_returns']:
                    # Create x-axis (trade numbers)
                    trade_numbers = list(range(1, len(result['cumulative_returns']) + 1))
                    
                    # Plot cumulative returns
                    ax.plot(trade_numbers, result['cumulative_returns'], 
                           label=symbol, linewidth=2, marker='o', markersize=4)
            
            ax.set_title('Cumulative Returns Over Time', fontsize=14, fontweight='bold')
            ax.set_xlabel('Trade Number', fontsize=12)
            ax.set_ylabel('Cumulative P&L (₹)', fontsize=12)
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            # Add horizontal line at zero
            ax.axhline(y=0, color='black', linestyle='--', alpha=0.5)
            
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                self.logger.info(f"Cumulative returns chart saved to {save_path}")
            
            plt.show()
            
        except Exception as e:
            self.logger.error(f"Error plotting cumulative returns: {str(e)}")
    
    def plot_win_loss_distribution(self, backtest_results, save_path=None):
        """Plot win/loss distribution."""
        try:
            if not backtest_results:
                self.logger.warning("No backtest results to plot")
                return
            
            # Collect all P&L values
            all_pnl = []
            for result in backtest_results.values():
                all_pnl.extend([trade['pnl'] for trade in result['trades']])
            
            if not all_pnl:
                self.logger.warning("No trades to plot")
                return
            
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
            
            # Plot 1: Histogram of P&L distribution
            ax1.hist(all_pnl, bins=20, color='skyblue', alpha=0.7, edgecolor='black')
            ax1.set_title('P&L Distribution', fontsize=12, fontweight='bold')
            ax1.set_xlabel('P&L (₹)', fontsize=10)
            ax1.set_ylabel('Frequency', fontsize=10)
            ax1.axvline(x=0, color='red', linestyle='--', alpha=0.7, label='Break-even')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            
            # Plot 2: Box plot of P&L by symbol
            pnl_by_symbol = []
            symbol_labels = []
            
            for symbol, result in backtest_results.items():
                if result['trades']:
                    pnl_values = [trade['pnl'] for trade in result['trades']]
                    pnl_by_symbol.append(pnl_values)
                    symbol_labels.append(symbol)
            
            if pnl_by_symbol:
                box_plot = ax2.boxplot(pnl_by_symbol, labels=symbol_labels, patch_artist=True)
                
                # Color boxes based on median value
                for patch, pnl_list in zip(box_plot['boxes'], pnl_by_symbol):
                    median_val = np.median(pnl_list)
                    patch.set_facecolor('green' if median_val >= 0 else 'red')
                    patch.set_alpha(0.7)
                
                ax2.set_title('P&L Distribution by Symbol', fontsize=12, fontweight='bold')
                ax2.set_ylabel('P&L (₹)', fontsize=10)
                ax2.tick_params(axis='x', rotation=45)
                ax2.axhline(y=0, color='black', linestyle='--', alpha=0.5)
                ax2.grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                self.logger.info(f"Win/loss distribution chart saved to {save_path}")
            
            plt.show()
            
        except Exception as e:
            self.logger.error(f"Error plotting win/loss distribution: {str(e)}")

if __name__ == "__main__":
    # Test the visualizer
    import yfinance as yf
    from datetime import datetime, timedelta
    from technical_indicators import TechnicalIndicators
    from signal_generator import SignalGenerator
    
    # Get sample data
    stock = yf.Ticker("RELIANCE.NS")
    data = stock.history(start=datetime.now() - timedelta(days=180), end=datetime.now())
    
    # Calculate indicators
    indicators = TechnicalIndicators()
    indicators_data = indicators.calculate_indicators(data)
    
    # Generate signals
    signal_gen = SignalGenerator()
    signals = signal_gen._generate_stock_signals("RELIANCE.NS", indicators_data)
    
    # Test visualization
    visualizer = Visualizer()
    visualizer.plot_stock_with_signals("RELIANCE.NS", indicators_data, signals) 
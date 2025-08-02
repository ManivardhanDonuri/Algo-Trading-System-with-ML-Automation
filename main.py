import logging
import json
import sys
from datetime import datetime
import traceback

# Import all modules
from data_fetcher import DataFetcher
from technical_indicators import TechnicalIndicators
from signal_generator import SignalGenerator
from backtester import Backtester
from google_sheets_logger import GoogleSheetsLogger
from telegram_alerts import TelegramAlerts
from visualizer import Visualizer

class TradingSystem:
    def __init__(self, config_file='config.json'):
        """Initialize the complete trading system."""
        self.config_file = config_file
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('trading_system.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.data_fetcher = DataFetcher(config_file)
        self.indicators = TechnicalIndicators(config_file)
        self.signal_generator = SignalGenerator(config_file)
        self.backtester = Backtester(config_file)
        self.sheets_logger = GoogleSheetsLogger(config_file)
        self.telegram_alerts = TelegramAlerts(config_file)
        self.visualizer = Visualizer(config_file)
        
        self.logger.info("Trading system initialized successfully")
    
    def run_complete_analysis(self):
        """Run the complete trading analysis pipeline."""
        try:
            self.logger.info("Starting complete trading analysis...")
            
            # Step 1: Fetch historical data
            self.logger.info("Step 1: Fetching historical data...")
            stock_data = self.data_fetcher.fetch_all_stocks_data()
            
            if not stock_data:
                self.logger.error("No stock data fetched. Exiting.")
                return False
            
            # Step 2: Calculate technical indicators
            self.logger.info("Step 2: Calculating technical indicators...")
            indicators_data = self.indicators.calculate_all_indicators(stock_data)
            
            if not indicators_data:
                self.logger.error("No indicators calculated. Exiting.")
                return False
            
            # Step 3: Generate trading signals
            self.logger.info("Step 3: Generating trading signals...")
            all_signals = self.signal_generator.generate_signals(indicators_data)
            
            # Step 4: Run backtest
            self.logger.info("Step 4: Running backtest...")
            backtest_results = self.backtester.run_backtest(indicators_data, all_signals)
            
            # Step 5: Get current signals
            self.logger.info("Step 5: Checking current signals...")
            current_indicators = self.indicators.get_current_indicators(indicators_data)
            current_signals = self.signal_generator.check_current_signals(current_indicators)
            
            # Step 6: Get portfolio summary
            portfolio_summary = self.backtester.get_portfolio_summary(backtest_results)
            
            # Step 7: Log results to Google Sheets
            self.logger.info("Step 7: Logging to Google Sheets...")
            self._log_to_sheets(backtest_results, current_signals, portfolio_summary)
            
            # Step 8: Send Telegram alerts
            self.logger.info("Step 8: Sending Telegram alerts...")
            self._send_telegram_alerts(current_signals, portfolio_summary, backtest_results)
            
            # Step 9: Generate visualizations
            self.logger.info("Step 9: Generating visualizations...")
            self._generate_visualizations(backtest_results, indicators_data, all_signals)
            
            # Step 10: Print summary
            self._print_summary(backtest_results, current_signals, portfolio_summary)
            
            self.logger.info("Complete trading analysis finished successfully!")
            return True
            
        except Exception as e:
            self.logger.error(f"Error in complete analysis: {str(e)}")
            self.logger.error(traceback.format_exc())
            
            # Send error alert
            try:
                self.telegram_alerts.send_error_alert(str(e))
            except:
                pass
            
            return False
    
    def _log_to_sheets(self, backtest_results, current_signals, portfolio_summary):
        """Log all results to Google Sheets."""
        try:
            # Log trades
            if backtest_results:
                self.sheets_logger.log_trades(backtest_results)
                self.sheets_logger.log_pnl_summary(backtest_results)
            
            # Log portfolio summary
            if portfolio_summary:
                self.sheets_logger.log_portfolio_summary(portfolio_summary)
            
            # Log current signals
            if current_signals:
                self.sheets_logger.log_current_signals(current_signals)
                
        except Exception as e:
            self.logger.error(f"Error logging to sheets: {str(e)}")
    
    def _send_telegram_alerts(self, current_signals, portfolio_summary, backtest_results):
        """Send Telegram alerts."""
        try:
            # Send current signals
            for signal in current_signals.values():
                self.telegram_alerts.send_signal_alert(signal)
            
            # Send portfolio update
            if portfolio_summary:
                self.telegram_alerts.send_portfolio_update(portfolio_summary)
            
            # Send daily summary
            self.telegram_alerts.send_daily_summary(backtest_results, current_signals)
            
        except Exception as e:
            self.logger.error(f"Error sending Telegram alerts: {str(e)}")
    
    def _generate_visualizations(self, backtest_results, indicators_data, all_signals):
        """Generate and save visualizations."""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            # Portfolio performance
            if backtest_results:
                self.visualizer.plot_portfolio_performance(
                    backtest_results, 
                    f'portfolio_performance_{timestamp}.png'
                )
                
                # Cumulative returns
                self.visualizer.plot_cumulative_returns(
                    backtest_results, 
                    f'cumulative_returns_{timestamp}.png'
                )
                
                # Win/loss distribution
                self.visualizer.plot_win_loss_distribution(
                    backtest_results, 
                    f'win_loss_distribution_{timestamp}.png'
                )
            
            # Individual stock charts
            for symbol in indicators_data.keys():
                if symbol in all_signals and indicators_data[symbol] is not None:
                    self.visualizer.plot_stock_with_signals(
                        symbol,
                        indicators_data[symbol],
                        all_signals[symbol],
                        f'{symbol}_signals_{timestamp}.png'
                    )
                    
        except Exception as e:
            self.logger.error(f"Error generating visualizations: {str(e)}")
    
    def _print_summary(self, backtest_results, current_signals, portfolio_summary):
        """Print analysis summary to console."""
        print("\n" + "="*60)
        print("TRADING SYSTEM ANALYSIS SUMMARY")
        print("="*60)
        
        # Current signals
        if current_signals:
            print(f"\n🔔 CURRENT SIGNALS ({len(current_signals)}):")
            for symbol, signal in current_signals.items():
                print(f"  {symbol}: {signal['type']} at ₹{signal['price']:.2f} - {signal['reason']}")
        else:
            print("\n🔔 CURRENT SIGNALS: None")
        
        # Backtest results
        if backtest_results:
            print(f"\n📊 BACKTEST RESULTS ({len(backtest_results)} symbols):")
            for symbol, result in backtest_results.items():
                print(f"  {symbol}: {result['total_trades']} trades, "
                      f"Win Rate: {result['win_rate']:.1f}%, "
                      f"P&L: ₹{result['total_pnl']:.2f}")
        
        # Portfolio summary
        if portfolio_summary:
            print(f"\n💰 PORTFOLIO SUMMARY:")
            print(f"  Total Trades: {portfolio_summary['total_trades']}")
            print(f"  Win Rate: {portfolio_summary['win_rate']:.2f}%")
            print(f"  Total P&L: ₹{portfolio_summary['total_pnl']:.2f}")
            print(f"  Sharpe Ratio: {portfolio_summary['sharpe_ratio']:.2f}")
        
        print("\n" + "="*60)
    
    def run_daily_monitoring(self):
        """Run daily monitoring for current signals."""
        try:
            self.logger.info("Running daily monitoring...")
            
            # Fetch latest data
            stock_data = self.data_fetcher.fetch_all_stocks_data()
            indicators_data = self.indicators.calculate_all_indicators(stock_data)
            
            # Check current signals
            current_indicators = self.indicators.get_current_indicators(indicators_data)
            current_signals = self.signal_generator.check_current_signals(current_indicators)
            
            # Send alerts for new signals
            for signal in current_signals.values():
                self.telegram_alerts.send_signal_alert(signal)
            
            self.logger.info(f"Daily monitoring completed. Found {len(current_signals)} signals.")
            return True
            
        except Exception as e:
            self.logger.error(f"Error in daily monitoring: {str(e)}")
            return False

def main():
    """Main function to run the trading system."""
    print("🤖 NIFTY 50 Rule-Based Trading System")
    print("="*50)
    
    # Initialize trading system
    trading_system = TradingSystem()
    
    # Check command line arguments
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        
        if mode == 'daily':
            print("Running daily monitoring...")
            success = trading_system.run_daily_monitoring()
        elif mode == 'analysis':
            print("Running complete analysis...")
            success = trading_system.run_complete_analysis()
        else:
            print("Invalid mode. Use 'daily' or 'analysis'")
            return
    else:
        # Default: run complete analysis
        print("Running complete analysis...")
        success = trading_system.run_complete_analysis()
    
    if success:
        print("\n✅ Trading system completed successfully!")
    else:
        print("\n❌ Trading system encountered errors. Check logs for details.")

if __name__ == "__main__":
    main() 
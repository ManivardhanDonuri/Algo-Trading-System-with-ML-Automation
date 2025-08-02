import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import logging
import json
from datetime import datetime

class GoogleSheetsLogger:
    def __init__(self, config_file='config.json'):
        """Initialize Google Sheets logger with configuration."""
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        self.spreadsheet_id = self.config['google_sheets']['spreadsheet_id']
        self.service_account_file = self.config['google_sheets']['service_account_file']
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Initialize Google Sheets connection
        self._setup_connection()
    
    def _setup_connection(self):
        """Setup connection to Google Sheets."""
        try:
            # Define the scope
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]
            
            # Authenticate using service account
            creds = Credentials.from_service_account_file(
                self.service_account_file, scopes=scope
            )
            
            # Create client
            self.client = gspread.authorize(creds)
            
            # Open spreadsheet
            self.spreadsheet = self.client.open_by_key(self.spreadsheet_id)
            
            self.logger.info("Successfully connected to Google Sheets")
            
        except Exception as e:
            self.logger.error(f"Error connecting to Google Sheets: {str(e)}")
            self.client = None
            self.spreadsheet = None
    
    def log_trades(self, backtest_results):
        """Log all trades to Google Sheets."""
        if not self.spreadsheet:
            self.logger.error("Google Sheets not connected")
            return False
        
        try:
            # Get or create trades worksheet
            try:
                worksheet = self.spreadsheet.worksheet('Trade Log')
            except:
                worksheet = self.spreadsheet.add_worksheet(title='Trade Log', rows=1000, cols=10)
            
            # Prepare data for logging
            all_trades = []
            for symbol, result in backtest_results.items():
                for trade in result['trades']:
                    all_trades.append([
                        trade['symbol'],
                        trade['entry_date'],
                        trade['exit_date'],
                        trade['entry_price'],
                        trade['exit_price'],
                        trade['pnl'],
                        trade['pnl_pct'],
                        trade['holding_days'],
                        'WIN' if trade['is_win'] else 'LOSS'
                    ])
            
            if all_trades:
                # Clear existing data
                worksheet.clear()
                
                # Add headers
                headers = [
                    'Symbol', 'Entry Date', 'Exit Date', 'Entry Price', 
                    'Exit Price', 'P&L', 'P&L %', 'Holding Days', 'Result'
                ]
                worksheet.append_row(headers)
                
                # Add trade data
                for trade in all_trades:
                    worksheet.append_row(trade)
                
                self.logger.info(f"Logged {len(all_trades)} trades to Google Sheets")
                return True
            else:
                self.logger.warning("No trades to log")
                return False
                
        except Exception as e:
            self.logger.error(f"Error logging trades: {str(e)}")
            return False
    
    def log_pnl_summary(self, backtest_results):
        """Log P&L summary to Google Sheets."""
        if not self.spreadsheet:
            self.logger.error("Google Sheets not connected")
            return False
        
        try:
            # Get or create P&L summary worksheet
            try:
                worksheet = self.spreadsheet.worksheet('P&L Summary')
            except:
                worksheet = self.spreadsheet.add_worksheet(title='P&L Summary', rows=100, cols=10)
            
            # Prepare summary data
            summary_data = []
            for symbol, result in backtest_results.items():
                summary_data.append([
                    symbol,
                    result['total_trades'],
                    result['winning_trades'],
                    result['losing_trades'],
                    f"{result['win_rate']:.2f}%",
                    result['total_pnl'],
                    f"{result['total_pnl_pct']:.2f}%",
                    result['avg_win'],
                    result['avg_loss'],
                    result['max_win'],
                    result['max_loss'],
                    f"{result['avg_holding_days']:.1f}"
                ])
            
            if summary_data:
                # Clear existing data
                worksheet.clear()
                
                # Add headers
                headers = [
                    'Symbol', 'Total Trades', 'Winning Trades', 'Losing Trades',
                    'Win Rate', 'Total P&L', 'Total P&L %', 'Avg Win', 'Avg Loss',
                    'Max Win', 'Max Loss', 'Avg Holding Days'
                ]
                worksheet.append_row(headers)
                
                # Add summary data
                for row in summary_data:
                    worksheet.append_row(row)
                
                self.logger.info(f"Logged P&L summary for {len(summary_data)} symbols")
                return True
            else:
                self.logger.warning("No P&L data to log")
                return False
                
        except Exception as e:
            self.logger.error(f"Error logging P&L summary: {str(e)}")
            return False
    
    def log_portfolio_summary(self, portfolio_summary):
        """Log portfolio summary to Google Sheets."""
        if not self.spreadsheet or not portfolio_summary:
            self.logger.error("Google Sheets not connected or no portfolio data")
            return False
        
        try:
            # Get or create portfolio summary worksheet
            try:
                worksheet = self.spreadsheet.worksheet('Portfolio Summary')
            except:
                worksheet = self.spreadsheet.add_worksheet(title='Portfolio Summary', rows=50, cols=10)
            
            # Clear existing data
            worksheet.clear()
            
            # Add portfolio summary
            summary_data = [
                ['Metric', 'Value'],
                ['Total Trades', portfolio_summary['total_trades']],
                ['Winning Trades', portfolio_summary['winning_trades']],
                ['Win Rate', f"{portfolio_summary['win_rate']:.2f}%"],
                ['Total P&L', portfolio_summary['total_pnl']],
                ['Total P&L %', f"{portfolio_summary['total_pnl_pct']:.2f}%"],
                ['Avg P&L per Trade', portfolio_summary['avg_pnl_per_trade']],
                ['Sharpe Ratio', f"{portfolio_summary['sharpe_ratio']:.2f}"],
                ['Symbols Traded', portfolio_summary['symbols_traded']],
                ['Last Updated', datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
            ]
            
            for row in summary_data:
                worksheet.append_row(row)
            
            self.logger.info("Logged portfolio summary to Google Sheets")
            return True
            
        except Exception as e:
            self.logger.error(f"Error logging portfolio summary: {str(e)}")
            return False
    
    def log_current_signals(self, current_signals):
        """Log current trading signals to Google Sheets."""
        if not self.spreadsheet:
            self.logger.error("Google Sheets not connected")
            return False
        
        try:
            # Get or create current signals worksheet
            try:
                worksheet = self.spreadsheet.worksheet('Current Signals')
            except:
                worksheet = self.spreadsheet.add_worksheet(title='Current Signals', rows=100, cols=10)
            
            # Clear existing data
            worksheet.clear()
            
            # Add headers
            headers = [
                'Symbol', 'Signal Type', 'Price', 'RSI', 'SMA 20', 'SMA 50', 
                'Reason', 'Date'
            ]
            worksheet.append_row(headers)
            
            # Add signal data
            for symbol, signal in current_signals.items():
                row = [
                    symbol,
                    signal['type'],
                    signal['price'],
                    f"{signal['rsi']:.2f}",
                    f"{signal['sma_20']:.2f}",
                    f"{signal['sma_50']:.2f}",
                    signal['reason'],
                    signal['date']
                ]
                worksheet.append_row(row)
            
            self.logger.info(f"Logged {len(current_signals)} current signals")
            return True
            
        except Exception as e:
            self.logger.error(f"Error logging current signals: {str(e)}")
            return False

if __name__ == "__main__":
    # Test the Google Sheets logger
    # Note: This requires proper Google Sheets API setup
    print("Google Sheets Logger Test")
    print("Note: Requires service_account.json file and proper Google Sheets API setup")
    
    try:
        logger = GoogleSheetsLogger()
        if logger.client:
            print("Successfully connected to Google Sheets")
        else:
            print("Failed to connect to Google Sheets")
    except Exception as e:
        print(f"Error: {str(e)}") 
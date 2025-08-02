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
        
        self.service_account_file = self.config['google_sheets']['service_account_file']
        self.spreadsheet_id = self.config['google_sheets']['spreadsheet_id']
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Initialize Google Sheets connection
        self._connect_to_sheets()
    
    def _connect_to_sheets(self):
        """Connect to Google Sheets."""
        try:
            # Check if service account file exists
            import os
            if not os.path.exists(self.service_account_file):
                self.logger.warning(f"Service account file '{self.service_account_file}' not found. Google Sheets logging will be disabled.")
                self.client = None
                self.spreadsheet = None
                return
            
            # Define the scope
            scope = ['https://spreadsheets.google.com/feeds',
                    'https://www.googleapis.com/auth/drive']
            
            # Load credentials
            creds = Credentials.from_service_account_file(
                self.service_account_file, scopes=scope
            )
            
            # Authorize the clientsheet
            self.client = gspread.authorize(creds)
            
            # Open the spreadsheet
            self.spreadsheet = self.client.open_by_key(self.spreadsheet_id)
            
            self.logger.info("Successfully connected to Google Sheets")
            
        except Exception as e:
            self.logger.warning(f"Google Sheets connection failed: {str(e)}. Google Sheets logging will be disabled.")
            self.client = None
            self.spreadsheet = None
    
    def log_trades(self, backtest_results):
        """Log all trades to Google Sheets."""
        if not self.spreadsheet:
            self.logger.info("Google Sheets not available - skipping trade logging")
            return
        
        try:
            # Get or create the Trade Log worksheet
            try:
                worksheet = self.spreadsheet.worksheet('Trade Log')
            except:
                worksheet = self.spreadsheet.add_worksheet(title='Trade Log', rows=1000, cols=10)
            
            # Clear existing data (except header)
            if worksheet.row_count > 1:
                worksheet.delete_rows(2, worksheet.row_count)
            
            # Prepare data
            rows = []
            for symbol, result in backtest_results.items():
                for trade in result['trades']:
                    row = [
                        trade['entry_date'],
                        symbol,
                        'BUY',
                        trade['entry_price'],
                        trade['exit_date'],
                        symbol,
                        'SELL',
                        trade['exit_price'],
                        trade['pnl'],
                        trade['pnl_pct'],
                        trade['holding_days'],
                        trade['result']
                    ]
                    rows.append(row)
            
            # Add data to worksheet
            if rows:
                worksheet.append_rows(rows)
                self.logger.info(f"Logged {len(rows)} trades to Google Sheets")
            
        except Exception as e:
            self.logger.error(f"Error logging trades: {str(e)}")
    
    def log_pnl_summary(self, backtest_results):
        """Log P&L summary to Google Sheets."""
        if not self.spreadsheet:
            self.logger.info("Google Sheets not available - skipping P&L summary logging")
            return
        
        try:
            # Get or create the P&L Summary worksheet
            try:
                worksheet = self.spreadsheet.worksheet('P&L Summary')
            except:
                worksheet = self.spreadsheet.add_worksheet(title='P&L Summary', rows=100, cols=10)
            
            # Clear existing data (except header)
            if worksheet.row_count > 1:
                worksheet.delete_rows(2, worksheet.row_count)
            
            # Prepare data
            rows = []
            for symbol, result in backtest_results.items():
                row = [
                    symbol,
                    result['total_trades'],
                    result['winning_trades'],
                    result['losing_trades'],
                    result['win_rate'],
                    result['total_pnl'],
                    result['total_pnl_pct'],
                    result['avg_pnl_per_trade'],
                    result['max_win'],
                    result['max_loss'],
                    result['avg_holding_days'],
                    result['sharpe_ratio']
                ]
                rows.append(row)
            
            # Add data to worksheet
            if rows:
                worksheet.append_rows(rows)
                self.logger.info(f"Logged P&L summary for {len(rows)} symbols")
            
        except Exception as e:
            self.logger.error(f"Error logging P&L summary: {str(e)}")
    
    def log_portfolio_summary(self, portfolio_summary):
        """Log portfolio summary to Google Sheets."""
        if not self.spreadsheet:
            self.logger.info("Google Sheets not available - skipping portfolio summary logging")
            return
        
        try:
            # Get or create the Portfolio Summary worksheet
            try:
                worksheet = self.spreadsheet.worksheet('Portfolio Summary')
            except:
                worksheet = self.spreadsheet.add_worksheet(title='Portfolio Summary', rows=10, cols=10)
            
            # Clear existing data (except header)
            if worksheet.row_count > 1:
                worksheet.delete_rows(2, worksheet.row_count)
            
            # Add portfolio summary
            row = [
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                portfolio_summary['total_trades'],
                portfolio_summary['winning_trades'],
                portfolio_summary['losing_trades'],
                portfolio_summary['win_rate'],
                portfolio_summary['total_pnl'],
                portfolio_summary['total_pnl_pct'],
                portfolio_summary['avg_pnl_per_trade'],
                portfolio_summary['sharpe_ratio'],
                ', '.join(portfolio_summary['symbols_traded'])
            ]
            
            worksheet.append_row(row)
            self.logger.info("Logged portfolio summary to Google Sheets")
            
        except Exception as e:
            self.logger.error(f"Error logging portfolio summary: {str(e)}")
    
    def log_current_signals(self, current_signals):
        """Log current signals to Google Sheets."""
        if not self.spreadsheet:
            self.logger.info("Google Sheets not available - skipping current signals logging")
            return
        
        try:
            # Get or create the Current Signals worksheet
            try:
                worksheet = self.spreadsheet.worksheet('Current Signals')
            except:
                worksheet = self.spreadsheet.add_worksheet(title='Current Signals', rows=10, cols=10)
            
            # Clear existing data (except header)
            if worksheet.row_count > 1:
                worksheet.delete_rows(2, worksheet.row_count)
            
            # Add current signals
            for symbol, signal in current_signals.items():
                row = [
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    symbol,
                    signal['type'],
                    signal['price'],
                    signal['rsi'],
                    signal['reason']
                ]
                worksheet.append_row(row)
            
            if current_signals:
                self.logger.info(f"Logged {len(current_signals)} current signals to Google Sheets")
            
        except Exception as e:
            self.logger.error(f"Error logging current signals: {str(e)}")

if __name__ == "__main__":
    # Test the Google Sheets logger
    logger = GoogleSheetsLogger()
    
    # Test with sample data
    sample_backtest = {
        'RELIANCE.NS': {
            'total_trades': 5,
            'winning_trades': 3,
            'losing_trades': 2,
            'win_rate': 60.0,
            'total_pnl': 500.0,
            'total_pnl_pct': 5.0,
            'avg_pnl_per_trade': 100.0,
            'max_win': 200.0,
            'max_loss': -50.0,
            'avg_holding_days': 15.0,
            'sharpe_ratio': 1.2,
            'trades': [
                {'entry_date': '2023-01-01', 'exit_date': '2023-01-15', 
                 'entry_price': 100, 'exit_price': 120, 'pnl': 20, 'pnl_pct': 20,
                 'holding_days': 14, 'result': 'WIN'}
            ]
        }
    }
    
    logger.log_trades(sample_backtest)
    logger.log_pnl_summary(sample_backtest) 
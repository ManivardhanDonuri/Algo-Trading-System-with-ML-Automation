import requests
import logging
import json
from datetime import datetime

class TelegramAlerts:
    def __init__(self, config_file='config.json'):
        """Initialize Telegram alerts with configuration."""
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        self.bot_token = self.config['telegram']['bot_token']
        self.chat_id = self.config['telegram']['chat_id']
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def send_message(self, message):
        """Send a message via Telegram bot."""
        try:
            url = f"{self.base_url}/sendMessage"
            data = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(url, data=data)
            
            if response.status_code == 200:
                self.logger.info("Message sent successfully via Telegram")
                return True
            else:
                self.logger.error(f"Failed to send message: {response.text}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error sending Telegram message: {str(e)}")
            return False
    
    def send_signal_alert(self, signal):
        """Send a trading signal alert."""
        try:
            symbol = signal['symbol']
            signal_type = signal['type']
            price = signal['price']
            rsi = signal['rsi']
            reason = signal['reason']
            date = signal['date']
            
            # Create emoji based on signal type
            emoji = "🟢" if signal_type == "BUY" else "🔴"
            
            message = f"""
{emoji} <b>TRADING SIGNAL ALERT</b> {emoji}

📈 <b>Symbol:</b> {symbol}
🎯 <b>Signal:</b> {signal_type}
💰 <b>Price:</b> ₹{price:.2f}
📊 <b>RSI:</b> {rsi:.2f}
📅 <b>Date:</b> {date}
💡 <b>Reason:</b> {reason}

⏰ <i>Alert Time:</i> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """.strip()
            
            return self.send_message(message)
            
        except Exception as e:
            self.logger.error(f"Error sending signal alert: {str(e)}")
            return False
    
    def send_portfolio_update(self, portfolio_summary):
        """Send portfolio performance update."""
        try:
            message = f"""
📊 <b>PORTFOLIO PERFORMANCE UPDATE</b>

📈 <b>Total Trades:</b> {portfolio_summary['total_trades']}
✅ <b>Winning Trades:</b> {portfolio_summary['winning_trades']}
❌ <b>Losing Trades:</b> {portfolio_summary['losing_trades']}
🎯 <b>Win Rate:</b> {portfolio_summary['win_rate']:.2f}%

💰 <b>Total P&L:</b> ₹{portfolio_summary['total_pnl']:.2f}
📊 <b>Total P&L %:</b> {portfolio_summary['total_pnl_pct']:.2f}%
📈 <b>Avg P&L per Trade:</b> ₹{portfolio_summary['avg_pnl_per_trade']:.2f}
⚡ <b>Sharpe Ratio:</b> {portfolio_summary['sharpe_ratio']:.2f}

🏢 <b>Symbols Traded:</b> {portfolio_summary['symbols_traded']}

⏰ <i>Last Updated:</i> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """.strip()
            
            return self.send_message(message)
            
        except Exception as e:
            self.logger.error(f"Error sending portfolio update: {str(e)}")
            return False
    
    def send_daily_summary(self, backtest_results, current_signals):
        """Send daily trading summary."""
        try:
            # Count signals by type
            buy_signals = len([s for s in current_signals.values() if s['type'] == 'BUY'])
            sell_signals = len([s for s in current_signals.values() if s['type'] == 'SELL'])
            
            # Get top performers
            if backtest_results:
                top_performers = sorted(
                    backtest_results.items(), 
                    key=lambda x: x[1]['total_pnl'], 
                    reverse=True
                )[:3]
            else:
                top_performers = []
            
            message = f"""
📅 <b>DAILY TRADING SUMMARY</b>

🎯 <b>Current Signals:</b>
🟢 Buy Signals: {buy_signals}
🔴 Sell Signals: {sell_signals}

📊 <b>Top Performers (Last 6 Months):</b>
"""
            
            for i, (symbol, result) in enumerate(top_performers, 1):
                message += f"{i}. {symbol}: ₹{result['total_pnl']:.2f} ({result['total_pnl_pct']:.2f}%)\n"
            
            if not top_performers:
                message += "No completed trades in the period.\n"
            
            message += f"\n⏰ <i>Report Time:</i> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            return self.send_message(message)
            
        except Exception as e:
            self.logger.error(f"Error sending daily summary: {str(e)}")
            return False
    
    def send_error_alert(self, error_message):
        """Send error alert."""
        try:
            message = f"""
⚠️ <b>SYSTEM ERROR ALERT</b>

❌ <b>Error:</b> {error_message}

⏰ <i>Time:</i> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """.strip()
            
            return self.send_message(message)
            
        except Exception as e:
            self.logger.error(f"Error sending error alert: {str(e)}")
            return False
    
    def test_connection(self):
        """Test Telegram bot connection."""
        try:
            url = f"{self.base_url}/getMe"
            response = requests.get(url)
            
            if response.status_code == 200:
                bot_info = response.json()
                self.logger.info(f"Telegram bot connected: {bot_info['result']['username']}")
                return True
            else:
                self.logger.error(f"Failed to connect to Telegram bot: {response.text}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error testing Telegram connection: {str(e)}")
            return False

if __name__ == "__main__":
    # Test the Telegram alerts
    print("Telegram Alerts Test")
    print("Note: Requires valid bot token and chat ID in config.json")
    
    try:
        alerts = TelegramAlerts()
        
        # Test connection
        if alerts.test_connection():
            print("Successfully connected to Telegram bot")
            
            # Test message
            test_message = "🤖 Trading Bot Test Message\n\nThis is a test message from your NIFTY 50 trading bot."
            if alerts.send_message(test_message):
                print("Test message sent successfully")
            else:
                print("Failed to send test message")
        else:
            print("Failed to connect to Telegram bot")
            
    except Exception as e:
        print(f"Error: {str(e)}") 
# NIFTY 50 Rule-Based Algo-Trading System

A comprehensive Python-based algorithmic trading system for NIFTY 50 stocks that performs technical analysis, generates trading signals, backtests strategies, and provides real-time alerts.

## 🎯 Features

- **Data Fetching**: Retrieves historical stock data using yfinance
- **Technical Indicators**: Calculates RSI, 20-DMA, and 50-DMA
- **Signal Generation**: Generates buy/sell signals based on RSI and SMA crossover
- **Backtesting**: Simulates trades and calculates performance metrics
- **Google Sheets Integration**: Logs trades and results to Google Sheets
- **Telegram Alerts**: Sends real-time trading signals via Telegram
- **Visualization**: Creates charts and performance graphs
- **Comprehensive Logging**: Detailed logging for debugging and monitoring

## 📋 Requirements

- Python 3.8+
- Internet connection for data fetching
- Google Sheets API credentials (optional)
- Telegram Bot token (optional)

## 🚀 Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the system**:
   - Edit `config.json` with your settings
   - Add Google Sheets service account file (optional)
   - Add Telegram bot credentials (optional)

## ⚙️ Configuration

Edit `config.json` to customize the system:

```json
{
    "telegram": {
        "bot_token": "YOUR_TELEGRAM_BOT_TOKEN",
        "chat_id": "YOUR_CHAT_ID"
    },
    "google_sheets": {
        "service_account_file": "service_account.json",
        "spreadsheet_id": "YOUR_SPREADSHEET_ID"
    },
    "trading": {
        "stocks": ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS"],
        "rsi_period": 14,
        "sma_short": 20,
        "sma_long": 50,
        "rsi_oversold": 30,
        "rsi_overbought": 70,
        "lookback_days": 180
    }
}
```

### Trading Strategy

- **Buy Signal**: RSI < 30 AND 20-DMA crosses above 50-DMA
- **Sell Signal**: RSI > 70 AND 20-DMA crosses below 50-DMA

## 🏃‍♂️ Usage

### Complete Analysis
Run the full trading analysis pipeline:
```bash
python main.py
# or
python main.py analysis
```

### Daily Monitoring
Run daily monitoring for current signals:
```bash
python main.py daily
```

### Individual Components

You can also run individual components for testing:

```bash
# Test data fetching
python data_fetcher.py

# Test technical indicators
python technical_indicators.py

# Test signal generation
python signal_generator.py

# Test backtesting
python backtester.py

# Test visualizations
python visualizer.py
```

## 📊 Output

The system generates:

1. **Console Output**: Real-time analysis summary
2. **Log Files**: Detailed logs in `trading_system.log`
3. **Google Sheets**: Trade logs, P&L summaries, and current signals
4. **Telegram Messages**: Real-time alerts and daily summaries
5. **Charts**: Performance visualizations saved as PNG files

### Sample Output
```
🤖 NIFTY 50 Rule-Based Trading System
==================================================

🔔 CURRENT SIGNALS (2):
  RELIANCE.NS: BUY at ₹2450.50 - RSI oversold (28.45) and SMA crossover bullish
  TCS.NS: SELL at ₹3850.75 - RSI overbought (72.30) and SMA crossover bearish

📊 BACKTEST RESULTS (3 symbols):
  RELIANCE.NS: 8 trades, Win Rate: 62.5%, P&L: ₹1250.50
  TCS.NS: 6 trades, Win Rate: 66.7%, P&L: ₹890.25
  HDFCBANK.NS: 5 trades, Win Rate: 80.0%, P&L: ₹1560.75

💰 PORTFOLIO SUMMARY:
  Total Trades: 19
  Win Rate: 68.4%
  Total P&L: ₹3701.50
  Sharpe Ratio: 1.85
```

## 🔧 Setup Instructions

### Google Sheets Integration

1. Create a Google Cloud Project
2. Enable Google Sheets API
3. Create a service account and download the JSON file
4. Share your Google Sheet with the service account email
5. Update `config.json` with your spreadsheet ID

### Telegram Bot Setup

1. Create a bot using @BotFather on Telegram
2. Get your bot token and chat ID
3. Update `config.json` with your credentials

## 📁 Project Structure

```
├── main.py                 # Main trading system orchestrator
├── data_fetcher.py         # Historical data retrieval
├── technical_indicators.py # RSI and SMA calculations
├── signal_generator.py     # Trading signal generation
├── backtester.py          # Backtesting engine
├── google_sheets_logger.py # Google Sheets integration
├── telegram_alerts.py      # Telegram notifications
├── visualizer.py          # Chart generation
├── config.json            # Configuration file
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 📈 Performance Metrics

The system calculates and tracks:

- **Total Trades**: Number of completed buy/sell cycles
- **Win Rate**: Percentage of profitable trades
- **Total P&L**: Net profit/loss in rupees
- **Average Win/Loss**: Average profit and loss per trade
- **Sharpe Ratio**: Risk-adjusted return measure
- **Holding Period**: Average days per trade

## 🔍 Monitoring

### Log Files
- `trading_system.log`: Comprehensive system logs
- Individual component logs for debugging

### Google Sheets Tabs
- **Trade Log**: All completed trades
- **P&L Summary**: Performance by symbol
- **Portfolio Summary**: Overall performance metrics
- **Current Signals**: Active trading signals

### Telegram Alerts
- Real-time signal notifications
- Daily performance summaries
- Error alerts for system issues

## ⚠️ Important Notes

1. **Paper Trading Only**: This system is for educational and research purposes
2. **Market Risk**: Past performance doesn't guarantee future results
3. **Data Quality**: Depends on yfinance data availability
4. **API Limits**: Respect rate limits for external APIs
5. **Configuration**: Always test with small datasets first

## 🛠️ Troubleshooting

### Common Issues

1. **No data fetched**: Check internet connection and stock symbols
2. **Google Sheets errors**: Verify service account credentials
3. **Telegram errors**: Check bot token and chat ID
4. **Import errors**: Ensure all dependencies are installed

### Debug Mode
Enable detailed logging by modifying the logging level in individual modules.

## 📝 License

This project is for educational purposes. Use at your own risk.

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve the system.

## 📞 Support

For questions or issues, please check the logs and configuration files first. The system includes comprehensive error handling and logging.

---

**Disclaimer**: This trading system is for educational purposes only. Always do your own research and consider consulting with financial advisors before making investment decisions. 
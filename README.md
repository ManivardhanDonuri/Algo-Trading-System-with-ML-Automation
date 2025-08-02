# NIFTY 50 Rule-Based Algo-Trading System

A comprehensive Python-based algorithmic trading system for NIFTY 50 stocks that performs technical analysis, generates trading signals, backtests strategies, and provides real-time alerts.

## 🎯 Features

- **Data Fetching**: Retrieves historical stock data using yfinance
- **Technical Indicators**: Calculates RSI, 20-DMA, and 50-DMA
- **Signal Generation**: Generates buy/sell signals based on RSI and SMA crossover
- **Backtesting**: Simulates trades and calculates performance metrics
- **Google Sheets Integration**: Logs trades and results to Google Sheets
- **Visualization**: Creates charts and performance graphs
- **Comprehensive Logging**: Detailed logging for debugging and monitoring

## 📋 Requirements

- Python 3.8+
- Internet connection for data fetching
- Google Sheets API credentials (optional)

## 🚀 Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the system**:
   - Edit `config.json` with your settings
   - Add Google Sheets service account file (optional)

## ⚙️ Configuration

Edit `config.json` to customize the system:

```json
{
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

### Testing
Test all components:
```bash
python test_system.py
```

## 📊 Output

The system generates:

1. **Console Output**: Real-time analysis summary
2. **Log Files**: Detailed logs in `trading_system.log`
3. **Google Sheets**: Trade logs, P&L summaries, and current signals
4. **Charts**: Performance visualizations saved as PNG files

## 📁 Project Structure

```
├── main.py                 # Main trading system orchestrator
├── data_fetcher.py         # Historical data retrieval
├── technical_indicators.py # RSI and SMA calculations
├── signal_generator.py     # Trading signal generation
├── backtester.py          # Backtesting engine
├── google_sheets_logger.py # Google Sheets integration
├── visualizer.py          # Chart generation
├── config.json            # Configuration file
├── test_system.py         # Component testing
└── README.md             # This file
```

## ⚠️ Important Notes

1. **Paper Trading Only**: This system is for educational and research purposes
2. **Market Risk**: Past performance doesn't guarantee future results
3. **Data Quality**: Depends on yfinance data availability
4. **API Limits**: Respect rate limits for external APIs
5. **Configuration**: Always test with small datasets first

## 📝 License

This project is for educational purposes. Use at your own risk.

---

**Disclaimer**: This trading system is for educational purposes only. Always do your own research and consider consulting with financial advisors before making investment decisions. 
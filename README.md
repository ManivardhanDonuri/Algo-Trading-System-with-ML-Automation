# 🤖 NIFTY 50 Rule-Based Algo-Trading System

A comprehensive Python-based algorithmic trading system for NIFTY 50 stocks that performs technical analysis, generates trading signals, backtests strategies, and provides real-time alerts with Google Sheets integration.

## 🎯 Features

- **📊 Data Fetching**: Retrieves historical stock data using yfinance
- **📈 Technical Indicators**: Calculates RSI, 20-DMA, and 50-DMA
- **🎯 Signal Generation**: Generates buy/sell signals based on RSI and SMA crossover
- **📊 Backtesting**: Simulates trades and calculates performance metrics
- **📋 Google Sheets Integration**: Logs trades and results to Google Sheets
- **📊 Visualization**: Creates charts and performance graphs
- **📝 Comprehensive Logging**: Detailed logging for debugging and monitoring
- **🧪 Testing Framework**: Complete component testing system

## 📋 Requirements

- Python 3.8+
- Internet connection for data fetching
- Google Sheets API credentials (optional)

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/ManivardhanDonuri/Algo-Trading-System-with-ML-Automation.git
cd Algo-Trading-System-with-ML-Automation

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

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

### 3. Google Sheets Setup (Optional)

Follow the detailed guide in `GOOGLE_SHEETS_SETUP.md` to configure Google Sheets integration.

### 4. Run the System

```bash
# Complete analysis
python main.py analysis

# Daily monitoring
python main.py daily

# Test all components
python test_system.py
```

## 📊 Trading Strategy

### Signal Generation Rules

- **🟢 BUY Signal**: RSI < 30 AND 20-DMA crosses above 50-DMA
- **🔴 SELL Signal**: RSI > 70 AND 20-DMA crosses below 50-DMA

### Technical Indicators

- **RSI (Relative Strength Index)**: Momentum oscillator (14-period)
- **SMA_20**: 20-day Simple Moving Average
- **SMA_50**: 50-day Simple Moving Average
- **Crossover Detection**: Identifies trend changes

## 📁 Project Structure

```
├── main.py                 # Main trading system orchestrator
├── data_fetcher.py         # Historical data retrieval
├── technical_indicators.py # RSI and SMA calculations
├── signal_generator.py     # Trading signal generation
├── backtester.py          # Backtesting engine
├── google_sheets_logger.py # Google Sheets integration
├── visualizer.py          # Chart generation
├── test_system.py         # Component testing
├── config.json            # Configuration file
├── requirements.txt        # Python dependencies
├── GOOGLE_SHEETS_SETUP.md # Google Sheets setup guide
└── README.md             # This file
```

## 📈 Output & Results

### Console Output
- Real-time analysis summary
- Current trading signals
- Performance metrics

### Log Files
- Detailed execution logs in `trading_system.log`
- Error tracking and debugging information

### Google Sheets (Optional)
- Trade logs with entry/exit details
- P&L summaries by symbol
- Portfolio performance metrics
- Current signal alerts

### Visualizations
- Stock price charts with buy/sell signals
- Portfolio performance metrics
- Cumulative returns over time
- Win/loss distribution analysis

## 🧪 Testing

Run comprehensive component tests:

```bash
python test_system.py
```

This will test:
- ✅ All required imports
- ✅ Configuration loading
- ✅ Data fetching
- ✅ Technical indicators calculation
- ✅ Signal generation
- ✅ Backtesting engine
- ✅ Visualization components

## ⚙️ Configuration Options

### Trading Parameters
- `stocks`: List of stock symbols to analyze
- `rsi_period`: RSI calculation period (default: 14)
- `sma_short`: Short-term SMA period (default: 20)
- `sma_long`: Long-term SMA period (default: 50)
- `rsi_oversold`: RSI oversold threshold (default: 30)
- `rsi_overbought`: RSI overbought threshold (default: 70)
- `lookback_days`: Historical data period (default: 180)

### Google Sheets Configuration
- `service_account_file`: Path to Google service account JSON
- `spreadsheet_id`: Google Sheets spreadsheet ID

## 🚀 Usage Examples

### Complete Analysis
```bash
python main.py analysis
```
Performs full analysis including:
- Historical data fetching
- Technical indicator calculation
- Signal generation
- Backtesting
- Google Sheets logging
- Visualization generation

### Daily Monitoring
```bash
python main.py daily
```
Checks current market conditions and generates signals for today.

### Component Testing
```bash
python test_system.py
```
Tests all system components without requiring external APIs.

## 📊 Performance Metrics

The system calculates and tracks:
- **Total P&L**: Overall profit/loss
- **Win Rate**: Percentage of profitable trades
- **Sharpe Ratio**: Risk-adjusted returns
- **Average Holding Days**: Typical trade duration
- **Maximum Win/Loss**: Best and worst trades
- **Total Trades**: Number of completed trades

## ⚠️ Important Notes

1. **📚 Educational Purpose**: This system is for educational and research purposes
2. **📈 Market Risk**: Past performance doesn't guarantee future results
3. **📊 Data Quality**: Depends on yfinance data availability
4. **🔒 API Limits**: Respect rate limits for external APIs
5. **⚙️ Configuration**: Always test with small datasets first

## 🆘 Troubleshooting

### Common Issues

1. **"No such file or directory: 'service_account.json'"**
   - Follow the Google Sheets setup guide
   - Or the system will run without Google Sheets integration

2. **"No results" in backtesting**
   - This is normal when market conditions don't meet signal criteria
   - Try different time periods or stocks

3. **Import errors**
   - Run `pip install -r requirements.txt`
   - Check Python version (3.8+ required)

4. **Data fetching issues**
   - Check internet connection
   - Verify stock symbols are correct
   - Try different time periods

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is for educational purposes. Use at your own risk.

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs in `trading_system.log`
3. Test individual components with `test_system.py`
4. Verify configuration in `config.json`

---

**Disclaimer**: This trading system is for educational purposes only. Always do your own research and consider consulting with financial advisors before making investment decisions.

## 🎉 Recent Updates

- ✅ Removed Telegram integration for simplified setup
- ✅ Enhanced Google Sheets integration with better error handling
- ✅ Improved visualization capabilities
- ✅ Added comprehensive testing framework
- ✅ Updated documentation and setup guides
- ✅ Enhanced logging and debugging features

---

**Built with ❤️ for algorithmic trading enthusiasts** 
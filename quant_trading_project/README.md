# Quantitative Trading Project

A modular Python framework for developing, backtesting, and analyzing algorithmic trading strategies.

## Project Structure

```
quant_trading_project/
├── data/                    # Data fetching and management
│   ├── __init__.py
│   └── data_fetcher.py      # Module for retrieving market data
├── backtest/               # Backtesting engine
│   ├── __init__.py
│   └── backtester.py       # Backtesting framework with performance metrics
├── strategies/             # Trading strategy implementations
│   ├── __init__.py
│   └── simple_moving_average.py  # Example strategies
├── utils/                  # Utility functions
│   ├── __init__.py
│   └── logger_config.py    # Logging configuration
├── config/                 # Configuration settings
│   ├── __init__.py
│   └── settings.py         # Global settings and parameters
├── logs/                   # Log files (created automatically)
├── data/                   # Data storage (raw and processed)
│   ├── raw/                # Raw market data
│   └── processed/          # Processed/cleaned data
├── .cache/                 # Temporary cache files
├── main.py                 # Main entry point demonstrating usage
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Features

### 1. Data Fetching (DataFetcher)
- Retrieve historical stock prices from Yahoo Finance
- Support for multiple symbols and custom date ranges
- Basic company information retrieval
- Flexible interval selection (daily, weekly, monthly, etc.)

### 2. Backtesting Engine (Backtester)
- Comprehensive performance evaluation
- Key metrics: total return, Sharpe ratio, max drawdown, volatility, win rate
- Visualizations: equity curves, drawdown charts, return distributions
- Benchmark comparisons against buy-and-hold strategies

### 3. Strategy Library (Strategies)
- Modular strategy design allowing easy addition of new strategies
- Pre-built examples: Simple Moving Average crossover, Mean Reversion
- Standardized interface for strategy functions
- Parameter optimization support

### 4. Utilities (Utils)
- Centralized logging system with file and console output
- Error handling and exception logging
- Configuration management

## Installation

1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

Note: Some packages like TA-Lib may require additional system dependencies. See package documentation for installation instructions.

## Usage

Run the main example:
```bash
python main.py
```

This will:
1. Fetch Apple (AAPL) stock data for 2022
2. Run three different strategies (SMA crossover, buy & hold, mean reversion)
3. Display performance metrics for each strategy
4. Compare results side-by-side

## Key Libraries Used

- **pandas**: Data manipulation and analysis
- **yfinance**: Free Yahoo Finance data API
- **numpy**: Numerical computations
- **matplotlib/seaborn**: Data visualization
- **backtrader**: Advanced backtesting framework (alternative option)
- **ta**: Technical analysis indicators
- **scikit-learn**: Machine learning for advanced strategies

## Getting Started

1. **Customize strategies**: Add your own strategies in the `strategies/` folder
2. **Modify parameters**: Adjust strategy parameters in `config/settings.py`
3. **Test different assets**: Change the symbol in `main.py` to test other stocks
4. **Add risk management**: Implement stop-losses, position sizing, etc.
5. **Extend data sources**: Add more data providers to `data_fetcher.py`

## Risk Warning

Past performance does not guarantee future results. Trading involves substantial risk and may not be suitable for all investors. This framework is for educational purposes only.

## Contributing

Feel free to fork this repository and submit pull requests for improvements. We welcome contributions for:
- New trading strategies
- Additional data sources
- Improved risk management features
- Better visualization tools
- Performance optimizations
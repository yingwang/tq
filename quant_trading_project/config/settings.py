"""
Configuration settings for the quantitative trading project
"""
import os
from pathlib import Path


# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Data directory
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
RAW_DATA_DIR.mkdir(exist_ok=True)
PROCESSED_DATA_DIR.mkdir(exist_ok=True)

# Cache directory
CACHE_DIR = PROJECT_ROOT / ".cache"
CACHE_DIR.mkdir(exist_ok=True)

# API Settings
YAHOO_FINANCE_TIMEOUT = 30  # seconds
ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY', '')
FRED_API_KEY = os.getenv('FRED_API_KEY', '')

# Backtesting settings
DEFAULT_INITIAL_CAPITAL = 10000.0
TRADING_DAYS_PER_YEAR = 252

# Risk management settings
MAX_POSITION_SIZE = 0.1  # Maximum 10% allocation per trade
STOP_LOSS_PERCENTAGE = 0.05  # 5% stop loss
TAKE_PROFIT_PERCENTAGE = 0.10  # 10% take profit

# Technical indicator defaults
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
MACD_FAST_PERIOD = 12
MACD_SLOW_PERIOD = 26
MACD_SIGNAL_PERIOD = 9

# Logging settings
LOG_LEVEL = 'INFO'
LOG_TO_FILE = True
LOG_MAX_SIZE = 10 * 1024 * 1024  # 10 MB

# Data settings
DEFAULT_DATA_INTERVAL = '1d'
SUPPORTED_INTERVALS = ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']

# Symbols to watch
DEFAULT_SYMBOLS = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN']

# Strategy parameters
STRATEGY_PARAMS = {
    'sma_crossover': {
        'short_window': 20,
        'long_window': 50
    },
    'rsi_reversion': {
        'window': 14,
        'oversold': 30,
        'overbought': 70
    },
    'mean_reversion': {
        'window': 20,
        'deviation': 1.0
    }
}

# Performance tracking
METRICS_TO_TRACK = [
    'total_return',
    'annual_return',
    'sharpe_ratio',
    'max_drawdown',
    'volatility',
    'win_rate',
    'profit_factor'
]
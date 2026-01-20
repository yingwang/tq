"""
Main entry point for the quantitative trading project
Demonstrates how to use the different modules together
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.data_fetcher import DataFetcher
from backtest.backtester import Backtester
from strategies.simple_moving_average import SimpleMovingAverageStrategy
from strategies.momentum_strategy import MomentumStrategy
from strategies.bollinger_bands_strategy import BollingerBandsStrategy
from strategies.rsi_strategy import RSIStrategy
from strategies.macd_strategy import MACDStrategy
from strategies.stochastic_oscillator_strategy import StochasticOscillatorStrategy
from strategies.adx_trend_strategy import ADXTrendStrategy
from strategies.vwap_strategy import VWAPStrategy
from utils.logger_config import setup_logger
from config.settings import DEFAULT_SYMBOLS, DEFAULT_INITIAL_CAPITAL


def main():
    # Setup logging
    logger = setup_logger(__name__)
    logger.info("Starting quantitative trading project")
    
    try:
        # Initialize modules
        data_fetcher = DataFetcher()
        backtester = Backtester()
        
        # Fetch data for a sample stock
        symbol = "AAPL"
        logger.info(f"Fetching data for {symbol}")
        data = data_fetcher.fetch_yahoo_data(symbol, start_date="2022-01-01", end_date="2023-01-01")
        
        print(f"Retrieved {len(data)} data points for {symbol}")
        print(f"Date range: {data.index[0].date()} to {data.index[-1].date()}")
        print("\nFirst few rows:")
        print(data.head())
        
        # Define all strategies with their parameters
        strategies = [
            ("Simple Moving Average", SimpleMovingAverageStrategy(symbol, short_window=20, long_window=50)),
            ("Momentum Strategy", MomentumStrategy(symbol, short_window=10, long_window=30)),
            ("Bollinger Bands", BollingerBandsStrategy(symbol, window=20, num_std_dev=2)),
            ("RSI Strategy", RSIStrategy(symbol, rsi_period=14, oversold=30, overbought=70)),
            ("MACD Strategy", MACDStrategy(symbol, fast_period=12, slow_period=26, signal_period=9)),
            ("Stochastic Oscillator", StochasticOscillatorStrategy(symbol, k_period=14, d_period=3, oversold=20, overbought=80)),
            ("ADX Trend Strategy", ADXTrendStrategy(symbol, adx_period=14, adx_threshold=25)),
            ("VWAP Strategy", VWAPStrategy(symbol, lookback_period=20, threshold=0.02))
        ]
        
        results = []
        
        # Run backtest for each strategy
        for strategy_name, strategy in strategies:
            print("\n" + "="*60)
            print(f"RUNNING {strategy_name.upper()} BACKTEST")
            print("="*60)
            
            backtester_instance = Backtester()
            strategy_results = backtester_instance.run_backtest(
                data=data,
                strategy_obj=strategy,
                initial_capital=DEFAULT_INITIAL_CAPITAL
            )
            
            backtester_instance.print_summary()
            results.append((strategy_name, strategy_results))
        
        # Show comprehensive comparison
        print("\n" + "="*60)
        print("COMPREHENSIVE STRATEGY COMPARISON")
        print("="*60)
        print(f"{'Strategy':<20} {'Total Return %':<15} {'Sharpe Ratio':<15} {'Max Drawdown %':<15}")
        print("-"*70)
        for strategy_name, result in results:
            print(f"{strategy_name:<20} {result['total_return']:<15.2f} {result['sharpe_ratio']:<15.2f} {result['max_drawdown']:<15.2f}")
        
        logger.info("All backtests completed successfully")
        
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
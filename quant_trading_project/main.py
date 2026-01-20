"""
Main entry point for the quantitative trading project
Demonstrates how to use the different modules together
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.data_fetcher import DataFetcher
from backtest.backtester import Backtester
from strategies.simple_moving_average import sma_crossover_strategy, buy_hold_strategy, mean_reversion_strategy
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
        
        # Run SMA crossover strategy backtest
        print("\n" + "="*60)
        print("RUNNING SMA CROSSOVER STRATEGY BACKTEST")
        print("="*60)
        
        sma_results = backtester.run_backtest(
            strategy_func=sma_crossover_strategy,
            data=data,
            initial_capital=DEFAULT_INITIAL_CAPITAL,
            short_window=20,
            long_window=50
        )
        
        backtester.print_summary()
        
        # Run buy & hold strategy for comparison
        print("\n" + "="*60)
        print("RUNNING BUY & HOLD STRATEGY BACKTEST (for comparison)")
        print("="*60)
        
        backtester_comparison = Backtester()
        buy_hold_results = backtester_comparison.run_backtest(
            strategy_func=buy_hold_strategy,
            data=data,
            initial_capital=DEFAULT_INITIAL_CAPITAL
        )
        
        backtester_comparison.print_summary()
        
        # Run mean reversion strategy
        print("\n" + "="*60)
        print("RUNNING MEAN REVERSION STRATEGY BACKTEST")
        print("="*60)
        
        backtester_mr = Backtester()
        mr_results = backtester_mr.run_backtest(
            strategy_func=mean_reversion_strategy,
            data=data,
            initial_capital=DEFAULT_INITIAL_CAPITAL,
            window=20,
            deviation=1.0
        )
        
        backtester_mr.print_summary()
        
        # Show comparison
        print("\n" + "="*60)
        print("STRATEGY COMPARISON")
        print("="*60)
        print(f"SMA Crossover:   {sma_results['total_return']:.2f}% return, Sharpe: {sma_results['sharpe_ratio']:.2f}")
        print(f"Buy & Hold:      {buy_hold_results['total_return']:.2f}% return, Sharpe: {buy_hold_results['sharpe_ratio']:.2f}")
        print(f"Mean Reversion:  {mr_results['total_return']:.2f}% return, Sharpe: {mr_results['sharpe_ratio']:.2f}")
        
        logger.info("All backtests completed successfully")
        
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
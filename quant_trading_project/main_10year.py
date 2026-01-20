"""
Main entry point for the quantitative trading project
10-year historical analysis (2015-2024)
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
from datetime import datetime
from data.data_fetcher import DataFetcher
from backtest.backtester import Backtester
from strategies.simple_moving_average import SimpleMovingAverageStrategy
from strategies.momentum_strategy import MomentumStrategy
from strategies.bollinger_bands_strategy import BollingerBandsStrategy
from strategies.rsi_strategy import RSIStrategy
from strategies.macd_strategy import MACDStrategy
from strategies.stochastic_oscillator_strategy import StochasticOscillatorStrategy
from strategies.vwap_strategy import VWAPStrategy
from strategies.dca_strategy import DollarCostAveragingStrategy
from strategies.buy_and_hold_strategy import BuyAndHoldStrategy
from utils.logger_config import setup_logger
from config.settings import DEFAULT_SYMBOLS, DEFAULT_INITIAL_CAPITAL


def create_strategies(symbol):
    """Create all strategy instances for a given symbol"""
    return [
        ("[BENCHMARK] Buy & Hold", BuyAndHoldStrategy(symbol)),
        ("Simple Moving Average", SimpleMovingAverageStrategy(symbol, short_window=20, long_window=50)),
        ("Momentum Strategy", MomentumStrategy(symbol, short_window=10, long_window=30)),
        ("Bollinger Bands", BollingerBandsStrategy(symbol, window=20, num_std_dev=2)),
        ("RSI Strategy", RSIStrategy(symbol, rsi_period=14, oversold=30, overbought=70)),
        ("MACD Strategy", MACDStrategy(symbol, fast_period=12, slow_period=26, signal_period=9)),
        ("Stochastic Oscillator", StochasticOscillatorStrategy(symbol, k_period=14, d_period=3, oversold=20, overbought=80)),
        ("VWAP Strategy", VWAPStrategy(symbol, lookback_period=20, threshold=0.02)),
        ("Dollar-Cost Averaging (DCA)", DollarCostAveragingStrategy(symbol, frequency="monthly"))
    ]


def main():
    # Setup logging
    logger = setup_logger(__name__)
    logger.info("Starting 10-year strategy analysis")
    
    try:
        # Initialize modules
        data_fetcher = DataFetcher()
        
        # Define test cases: (symbol, start_date, end_date, label)
        # Generate past 10 years of data (2015-2024)
        symbols = ["AAPL", "MSFT", "GOOGL"]
        years = list(range(2015, 2025))  # 2015 to 2024
        
        test_cases = []
        for symbol in symbols:
            for year in years:
                start_date = f"{year}-01-01"
                end_date = f"{year}-12-31"
                test_cases.append((symbol, start_date, end_date, str(year)))
        
        # Store all results for final comparison
        all_results = []
        
        # Run backtests for each test case
        print("Starting 10-year backtest analysis...")
        # 动态计算策略数量和总回测数
        num_strategies = len(create_strategies(symbols[0]))
        total_backtests = len(symbols) * len(years) * num_strategies
        print(f"Total test cases: {len(test_cases)} (3 symbols × 10 years × {num_strategies} strategies = {total_backtests} backtests)")
        print()
        
        for idx, (symbol, start_date, end_date, label) in enumerate(test_cases, 1):
            print(f"[{idx:3d}/{len(test_cases)}] {symbol} {label}...", end=" ", flush=True)
            
            try:
                # Fetch data
                data = data_fetcher.fetch_yahoo_data(symbol, start_date=start_date, end_date=end_date)
                
                if len(data) == 0:
                    print("⚠ No data")
                    continue
                
                # Create strategies
                strategies = create_strategies(symbol)
                
                period_results = []
                
                # Run backtest for each strategy
                for strategy_name, strategy in strategies:
                    backtester_instance = Backtester()
                    strategy_results = backtester_instance.run_backtest(
                        data=data,
                        strategy_obj=strategy,
                        initial_capital=DEFAULT_INITIAL_CAPITAL
                    )
                    
                    period_results.append({
                        'symbol': symbol,
                        'year': label,
                        'strategy': strategy_name,
                        'total_return': strategy_results['total_return'],
                        'benchmark_return': strategy_results['benchmark_return'],
                        'excess_return': strategy_results['total_return'] - strategy_results['benchmark_return'],
                        'sharpe_ratio': strategy_results['sharpe_ratio'],
                        'max_drawdown': strategy_results['max_drawdown'],
                        'volatility': strategy_results['volatility'],
                        'win_rate': strategy_results['win_rate']
                    })
                
                all_results.extend(period_results)
                print("✓")
                
            except Exception as e:
                print(f"✗ ({str(e)[:30]})")
                logger.error(f"Error processing {symbol} {label}: {str(e)}")
                continue
        
        # Generate comprehensive summary across all test cases
        if all_results:
            print(f"\n{'='*120}")
            print("10-YEAR STRATEGY PERFORMANCE ANALYSIS (2015-2024)")
            print("="*120)
            
            # Convert to DataFrame for easier analysis
            df = pd.DataFrame(all_results)
            
            # 1. Strategy consistency analysis (summary across all 10 years)
            print("\n" + "="*120)
            print("STRATEGY CONSISTENCY ANALYSIS (All 10 Years, All 3 Symbols)")
            print("="*120)
            
            consistency_stats = []
            for strategy in sorted(df['strategy'].unique()):
                strategy_returns = df[df['strategy'] == strategy]['total_return']
                
                consistency_stats.append({
                    'Strategy': strategy,
                    'Avg Return %': strategy_returns.mean(),
                    'Median Return %': strategy_returns.median(),
                    'Std Dev %': strategy_returns.std(),
                    'Positive Years': (strategy_returns > 0).sum(),
                    'Win Rate %': (strategy_returns > 0).sum() / len(strategy_returns) * 100,
                    'Best Year %': strategy_returns.max(),
                    'Worst Year %': strategy_returns.min()
                })
            
            consistency_df = pd.DataFrame(consistency_stats).sort_values('Avg Return %', ascending=False)
            print(consistency_df.round(2).to_string(index=False))
            
            # 2. Pivot tables: Each stock with yearly performance for each strategy
            print("\n" + "="*120)
            print("DETAILED PERFORMANCE MATRIX: AAPL (2015-2024, Each Row = Strategy)")
            print("="*120)
            aapl_data = df[df['symbol'] == 'AAPL'].sort_values(['strategy', 'year'])
            for strategy in sorted(df['strategy'].unique()):
                strategy_data = aapl_data[aapl_data['strategy'] == strategy][['year', 'total_return', 'sharpe_ratio', 'max_drawdown']].set_index('year').T
                if len(strategy_data) > 0:
                    print(f"\n{strategy}:")
                    print(strategy_data.round(2).to_string())
            
            print("\n" + "="*120)
            print("DETAILED PERFORMANCE MATRIX: MSFT (2015-2024, Each Row = Strategy)")
            print("="*120)
            msft_data = df[df['symbol'] == 'MSFT'].sort_values(['strategy', 'year'])
            for strategy in sorted(df['strategy'].unique()):
                strategy_data = msft_data[msft_data['strategy'] == strategy][['year', 'total_return', 'sharpe_ratio', 'max_drawdown']].set_index('year').T
                if len(strategy_data) > 0:
                    print(f"\n{strategy}:")
                    print(strategy_data.round(2).to_string())
            
            print("\n" + "="*120)
            print("DETAILED PERFORMANCE MATRIX: GOOGL (2015-2024, Each Row = Strategy)")
            print("="*120)
            googl_data = df[df['symbol'] == 'GOOGL'].sort_values(['strategy', 'year'])
            for strategy in sorted(df['strategy'].unique()):
                strategy_data = googl_data[googl_data['strategy'] == strategy][['year', 'total_return', 'sharpe_ratio', 'max_drawdown']].set_index('year').T
                if len(strategy_data) > 0:
                    print(f"\n{strategy}:")
                    print(strategy_data.round(2).to_string())
            
            # 3. Pivot table view: Returns only
            print("\n" + "="*120)
            print("QUICK REFERENCE: TOTAL RETURNS (%) BY STOCK AND STRATEGY")
            print("="*120)
            
            for symbol in sorted(symbols):
                symbol_data = df[df['symbol'] == symbol]
                pivot_return = symbol_data.pivot_table(
                    index='strategy',
                    columns='year',
                    values='total_return',
                    aggfunc='first'
                )
                print(f"\n{symbol}:")
                print(pivot_return.round(1).to_string())
            
            # 4. Best and worst performing combinations
            print("\n" + "="*120)
            print("TOP 20 BEST PERFORMING COMBINATIONS (by Total Return)")
            print("="*120)
            top_20 = df.nlargest(20, 'total_return')[['symbol', 'year', 'strategy', 'total_return', 'sharpe_ratio', 'max_drawdown']]
            print(top_20.to_string(index=False))
            
            print("\n" + "="*120)
            print("BOTTOM 20 WORST PERFORMING COMBINATIONS (by Total Return)")
            print("="*120)
            bottom_20 = df.nsmallest(20, 'total_return')[['symbol', 'year', 'strategy', 'total_return', 'sharpe_ratio', 'max_drawdown']]
            print(bottom_20.to_string(index=False))
            
            # 5. Year-by-year summary
            print("\n" + "="*120)
            print("YEARLY SUMMARY: AVERAGE PERFORMANCE ACROSS ALL STRATEGIES AND STOCKS")
            print("="*120)
            yearly_summary = df.groupby('year')[['total_return', 'benchmark_return', 'sharpe_ratio', 'max_drawdown']].mean()
            print(yearly_summary.round(2).to_string())
            
            # Save results to CSV
            csv_filename = f"backtest_10year_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            df.to_csv(csv_filename, index=False)
            print(f"\n✓ Detailed results saved to: {csv_filename}")
        
        logger.info("All backtests completed successfully")
        
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    main()

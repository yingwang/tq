"""
Backtester class for evaluating trading strategies
Provides performance metrics and visualization capabilities
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import logging
from typing import Dict, List, Tuple


class Backtester:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.results = {}
    
    def run_backtest(self, strategy_func, data: pd.DataFrame, initial_capital: float = 10000.0, **kwargs):
        """
        Run backtest for a given strategy
        
        Args:
            strategy_func: Strategy function that takes data and returns signals
            data: Price data with OHLCV columns
            initial_capital: Starting capital for simulation
            **kwargs: Additional arguments for strategy function
        
        Returns:
            dict: Backtest results including equity curve, metrics, etc.
        """
        try:
            # Generate trading signals
            signals = strategy_func(data, **kwargs)
            
            # Combine signals with price data
            df = data.copy()
            if isinstance(signals, pd.DataFrame):
                df = df.join(signals, how='left')
            else:
                df['signal'] = signals
            
            # Initialize portfolio variables
            df['position'] = df['signal'].fillna(0).replace({-1: 0}).astype(int)  # Convert short signals to 0
            df['position'] = df['position'].shift(1).fillna(0)  # Positions are applied next day
            df['returns'] = df['Close'].pct_change()
            df['strategy_returns'] = df['position'] * df['returns']
            df['equity_curve'] = (1 + df['strategy_returns']).cumprod() * initial_capital
            df['benchmark_curve'] = (1 + df['returns']).cumprod() * initial_capital
            
            # Calculate drawdowns
            df['rolling_max'] = df['equity_curve'].expanding().max()
            df['drawdown'] = (df['equity_curve'] - df['rolling_max']) / df['rolling_max']
            
            # Calculate performance metrics
            total_return = (df['equity_curve'].iloc[-1] / initial_capital - 1) * 100
            benchmark_return = (df['benchmark_curve'].iloc[-1] / initial_capital - 1) * 100
            
            # Sharpe ratio (assuming 252 trading days)
            if df['strategy_returns'].std() != 0:
                sharpe_ratio = df['strategy_returns'].mean() / df['strategy_returns'].std() * np.sqrt(252)
            else:
                sharpe_ratio = 0
                
            max_drawdown = df['drawdown'].min() * 100
            volatility = df['strategy_returns'].std() * np.sqrt(252) * 100
            
            # Win rate calculation
            winning_trades = df[df['strategy_returns'] > 0]['strategy_returns']
            losing_trades = df[df['strategy_returns'] < 0]['strategy_returns']
            win_rate = len(winning_trades) / (len(winning_trades) + len(losing_trades)) * 100 if len(winning_trades) + len(losing_trades) > 0 else 0
            
            results = {
                'total_return': total_return,
                'benchmark_return': benchmark_return,
                'sharpe_ratio': sharpe_ratio,
                'max_drawdown': max_drawdown,
                'volatility': volatility,
                'win_rate': win_rate,
                'data': df,
                'initial_capital': initial_capital
            }
            
            self.results = results
            self.logger.info(f"Backtest completed. Total Return: {total_return:.2f}%, Sharpe Ratio: {sharpe_ratio:.2f}")
            return results
            
        except Exception as e:
            self.logger.error(f"Error running backtest: {str(e)}")
            raise
    
    def calculate_metrics(self, returns: pd.Series) -> Dict[str, float]:
        """
        Calculate performance metrics from returns series
        
        Args:
            returns: Series of period returns
        
        Returns:
            dict: Performance metrics
        """
        total_return = (1 + returns).prod() - 1
        avg_return = returns.mean() * 252  # Annualized
        volatility = returns.std() * np.sqrt(252)  # Annualized
        sharpe_ratio = avg_return / volatility if volatility != 0 else 0
        
        # Max drawdown
        equity_curve = (1 + returns).cumprod()
        rolling_max = equity_curve.expanding().max()
        drawdowns = (equity_curve - rolling_max) / rolling_max
        max_drawdown = drawdowns.min()
        
        # Win rate
        win_rate = (returns > 0).sum() / len(returns) * 100
        
        return {
            'total_return': total_return * 100,
            'annual_return': avg_return * 100,
            'volatility': volatility * 100,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown * 100,
            'win_rate': win_rate
        }
    
    def plot_results(self, figsize=(14, 10)):
        """
        Plot backtest results
        """
        if not self.results:
            self.logger.warning("No results to plot. Run a backtest first.")
            return
            
        df = self.results['data']
        
        fig, axes = plt.subplots(2, 2, figsize=figsize)
        
        # Equity curve
        axes[0, 0].plot(df.index, df['equity_curve'], label='Strategy', linewidth=2)
        axes[0, 0].plot(df.index, df['benchmark_curve'], label='Benchmark (Buy & Hold)', linestyle='--')
        axes[0, 0].set_title('Equity Curve')
        axes[0, 0].legend()
        axes[0, 0].grid(True)
        
        # Drawdown
        axes[0, 1].fill_between(df.index, df['drawdown'] * 100, 0, alpha=0.3, color='red')
        axes[0, 1].set_title('Drawdown (%)')
        axes[0, 1].grid(True)
        
        # Daily returns
        axes[1, 0].bar(df.index, df['strategy_returns'] * 100, width=1, alpha=0.7)
        axes[1, 0].set_title('Daily Strategy Returns (%)')
        axes[1, 0].grid(True)
        
        # Position changes
        position_changes = df['position'].diff().abs()
        axes[1, 1].bar(df.index, position_changes, width=1, alpha=0.5, color='orange')
        axes[1, 1].set_title('Position Changes')
        axes[1, 1].grid(True)
        
        plt.tight_layout()
        plt.show()
    
    def print_summary(self):
        """
        Print summary of backtest results
        """
        if not self.results:
            print("No results to display. Run a backtest first.")
            return
            
        print("="*50)
        print("BACKTEST RESULTS SUMMARY")
        print("="*50)
        print(f"Total Return:      {self.results['total_return']:.2f}%")
        print(f"Benchmark Return:  {self.results['benchmark_return']:.2f}%")
        print(f"Excess Return:     {self.results['total_return'] - self.results['benchmark_return']:.2f}%")
        print(f"Sharpe Ratio:      {self.results['sharpe_ratio']:.2f}")
        print(f"Max Drawdown:      {self.results['max_drawdown']:.2f}%")
        print(f"Volatility:        {self.results['volatility']:.2f}%")
        print(f"Win Rate:          {self.results['win_rate']:.2f}%")
        print(f"Initial Capital:   ${self.results['initial_capital']:,.2f}")
        print(f"Final Capital:     ${self.results['data']['equity_curve'].iloc[-1]:,.2f}")
        print("="*50)
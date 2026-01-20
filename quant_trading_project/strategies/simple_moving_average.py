"""
Simple Moving Average Crossover Strategy
A basic trend-following strategy using moving average crossovers
"""
import pandas as pd
import numpy as np
from .base_strategy import BaseStrategy


class SimpleMovingAverageStrategy(BaseStrategy):
    """
    Simple Moving Average Crossover Strategy
    
    Buy signal when short SMA crosses above long SMA
    Sell signal when short SMA crosses below long SMA
    """
    
    def __init__(self, symbol, short_window=20, long_window=50):
        super().__init__(symbol)
        self.short_window = short_window
        self.long_window = long_window
        
    def generate_signals(self, data):
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0.0
        
        # Calculate moving averages
        signals['SMA_short'] = data['Close'].rolling(window=self.short_window).mean()
        signals['SMA_long'] = data['Close'].rolling(window=self.long_window).mean()
        
        # Generate signals using .loc to avoid index length issues
        condition = (
            (signals['SMA_short'] > signals['SMA_long']) &
            (signals['SMA_short'].shift(1) <= signals['SMA_long'].shift(1))
        )
        signals.loc[self.long_window:, 'signal'] = np.where(
            condition[self.long_window:], 1.0, 0.0
        )
        
        # Generate actual trading signals
        signals['positions'] = signals['signal'].diff()
        
        return signals


def sma_crossover_strategy(data: pd.DataFrame, short_window: int = 20, long_window: int = 50) -> pd.Series:
    """
    Simple Moving Average Crossover Strategy (Legacy function)
    
    Buy signal when short SMA crosses above long SMA
    Sell signal when short SMA crosses below long SMA
    
    Args:
        data: Price data with 'Close' column
        short_window: Period for short-term moving average
        long_window: Period for long-term moving average
    
    Returns:
        pd.Series: Trading signals (1 for buy, 0 for hold, -1 for sell)
    """
    df = data.copy()
    
    # Calculate moving averages
    df['SMA_short'] = df['Close'].rolling(window=short_window).mean()
    df['SMA_long'] = df['Close'].rolling(window=long_window).mean()
    
    # Generate signals
    df['signal'] = 0
    df['signal'][short_window:] = np.where(
        df['SMA_short'][short_window:] > df['SMA_long'][short_window:], 1, 0
    )
    
    # Convert to position changes (hold current position until signal changes)
    df['position'] = df['signal'].diff()
    
    # Return signals (1 for buy, 0 for hold/sell)
    return df['signal']


def buy_hold_strategy(data: pd.DataFrame) -> pd.Series:
    """
    Buy and Hold Strategy (Legacy function)
    
    Simply hold a long position throughout the entire period
    
    Args:
        data: Price data
    
    Returns:
        pd.Series: Trading signals (always 1 for buy/hold)
    """
    df = data.copy()
    df['signal'] = 1  # Always hold long position
    return df['signal']


def mean_reversion_strategy(data: pd.DataFrame, window: int = 20, deviation: float = 1.0) -> pd.Series:
    """
    Mean Reversion Strategy (Legacy function)
    
    Buy when price falls significantly below moving average
    Sell when price rises significantly above moving average
    
    Args:
        data: Price data with 'Close' column
        window: Period for calculating moving average
        deviation: Standard deviation multiplier for entry signals
    
    Returns:
        pd.Series: Trading signals (1 for buy, 0 for hold, -1 for sell)
    """
    df = data.copy()
    
    # Calculate moving average and standard deviation
    df['MA'] = df['Close'].rolling(window=window).mean()
    df['STD'] = df['Close'].rolling(window=window).std()
    
    # Calculate z-score
    df['z_score'] = (df['Close'] - df['MA']) / df['STD']
    
    # Generate signals
    df['signal'] = 0
    df.loc[df['z_score'] < -deviation, 'signal'] = 1  # Buy when oversold
    df.loc[df['z_score'] > deviation, 'signal'] = -1   # Sell when overbought
    
    return df['signal']
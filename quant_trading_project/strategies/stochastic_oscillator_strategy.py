import pandas as pd
import numpy as np
from .base_strategy import BaseStrategy


class StochasticOscillatorStrategy(BaseStrategy):
    """
    随机振荡器策略：基于%K和%D线进行交易
    当%K线从下向上穿越%D线且处于超卖区域时买入，
    当%K线从上向下穿越%D线且处于超买区域时卖出
    """
    
    def __init__(self, symbol, k_period=14, d_period=3, oversold=20, overbought=80):
        super().__init__(symbol)
        self.k_period = k_period
        self.d_period = d_period
        self.oversold = oversold
        self.overbought = overbought
        
    def generate_signals(self, data):
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0.0
        
        # 计算随机振荡器
        low_min = data['Low'].rolling(window=self.k_period).min()
        high_max = data['High'].rolling(window=self.k_period).max()
        
        # 避免除零错误
        denominator = high_max - low_min
        denominator = denominator.replace(0, np.nan)  # 将零替换为NaN以避免除零错误
        k_percent = 100 * ((data['Close'] - low_min) / denominator)
        k_percent = k_percent.fillna(method='bfill')  # 用前向填充处理NaN值
        d_percent = k_percent.rolling(window=self.d_period).mean()
        
        signals['k_percent'] = k_percent
        signals['d_percent'] = d_percent
        
        # 当%K线从下向上穿越%D线且在超卖区时买入
        signals['buy_signal'] = (
            (k_percent > d_percent) &
            (k_percent.shift(1) <= d_percent.shift(1)) &
            (k_percent <= self.oversold)
        )
        
        # 当%K线从上向下穿越%D线且在超买区时卖出
        signals['sell_signal'] = (
            (k_percent < d_percent) &
            (k_percent.shift(1) >= d_percent.shift(1)) &
            (k_percent >= self.overbought)
        )
        
        # 设置交易信号
        signals.loc[signals['buy_signal'], 'signal'] = 1.0
        signals.loc[signals['sell_signal'], 'signal'] = -1.0
        
        # 生成实际交易信号
        signals['positions'] = signals['signal'].diff()
        
        return signals
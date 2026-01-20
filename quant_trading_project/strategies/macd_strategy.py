import pandas as pd
import numpy as np
from .base_strategy import BaseStrategy


class MACDStrategy(BaseStrategy):
    """
    MACD策略：基于移动平均收敛发散指标进行交易
    当MACD线上穿信号线时买入，下穿时卖出
    """
    
    def __init__(self, symbol, fast_period=12, slow_period=26, signal_period=9):
        super().__init__(symbol)
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.signal_period = signal_period
        
    def generate_signals(self, data):
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0.0
        
        # 计算MACD
        exp1 = data['Close'].ewm(span=self.fast_period).mean()
        exp2 = data['Close'].ewm(span=self.slow_period).mean()
        
        macd = exp1 - exp2
        signal = macd.ewm(span=self.signal_period).mean()
        histogram = macd - signal
        
        signals['macd'] = macd
        signals['signal_line'] = signal
        signals['histogram'] = histogram
        
        # 当MACD线上穿信号线时买入
        buy_signal = (
            (macd > signal) &
            (macd.shift(1) <= signal.shift(1))
        )
        
        # 当MACD线下穿信号线时卖出
        sell_signal = (
            (macd < signal) &
            (macd.shift(1) >= signal.shift(1))
        )
        
        # 初始化持仓（持续持仓直到反向信号）
        signal_arr = np.zeros(len(data))
        current_position = 0.0
        
        for i in range(len(data)):
            if buy_signal.iloc[i]:
                current_position = 1.0
            elif sell_signal.iloc[i]:
                current_position = 0.0
            signal_arr[i] = current_position
        
        signals['signal'] = signal_arr
        
        # 生成实际交易信号
        signals['positions'] = signals['signal'].diff()
        
        return signals
import pandas as pd
import numpy as np
from .base_strategy import BaseStrategy


class RSIStrategy(BaseStrategy):
    """
    RSI策略：基于相对强弱指数进行交易
    当RSI超卖时买入，超买时卖出
    """
    
    def __init__(self, symbol, rsi_period=14, oversold=30, overbought=70):
        super().__init__(symbol)
        self.rsi_period = rsi_period
        self.oversold = oversold
        self.overbought = overbought
        
    def generate_signals(self, data):
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0.0
        
        # 计算RSI
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=self.rsi_period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.rsi_period).mean()
        
        # 处理除零情况
        rs = gain / loss
        rs = rs.fillna(0)  # 用0填充NaN值
        rsi = 100 - (100 / (1 + rs))
        
        signals['rsi'] = rsi
        
        # 当RSI从下向上穿越超卖线时买入
        buy_signal = (
            (rsi > self.oversold) &
            (rsi.shift(1) <= self.oversold)
        )
        
        # 当RSI从上向下穿越超买线时卖出
        sell_signal = (
            (rsi < self.overbought) &
            (rsi.shift(1) >= self.overbought)
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
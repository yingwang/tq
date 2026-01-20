import pandas as pd
import numpy as np
from .base_strategy import BaseStrategy


class BollingerBandsStrategy(BaseStrategy):
    """
    布林带策略：基于布林带通道进行交易
    当价格触及下轨时买入，触及上轨时卖出
    """
    
    def __init__(self, symbol, window=20, num_std_dev=2):
        super().__init__(symbol)
        self.window = window
        self.num_std_dev = num_std_dev
        
    def generate_signals(self, data):
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0.0
        
        # 计算布林带
        rolling_mean = data['Close'].rolling(window=self.window).mean()
        rolling_std = data['Close'].rolling(window=self.window).std()
        
        upper_band = rolling_mean + (rolling_std * self.num_std_dev)
        lower_band = rolling_mean - (rolling_std * self.num_std_dev)
        
        signals['upper_band'] = upper_band
        signals['middle_band'] = rolling_mean
        signals['lower_band'] = lower_band
        
        # 当价格从下向上突破下轨时买入
        signals['buy_signal'] = (
            (data['Close'] > lower_band) &
            (data['Close'].shift(1) <= lower_band.shift(1))
        )
        
        # 当价格从上向下突破上轨时卖出
        signals['sell_signal'] = (
            (data['Close'] < upper_band) &
            (data['Close'].shift(1) >= upper_band.shift(1))
        )
        
        # 设置交易信号
        signals.loc[signals['buy_signal'], 'signal'] = 1.0
        signals.loc[signals['sell_signal'], 'signal'] = -1.0
        
        # 生成实际交易信号
        signals['positions'] = signals['signal'].diff()
        
        return signals
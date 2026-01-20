import pandas as pd
import numpy as np
from .base_strategy import BaseStrategy


class VWAPStrategy(BaseStrategy):
    """
    VWAP策略：基于成交量加权平均价格进行交易
    当价格低于VWAP一定比例时买入，高于VWAP一定比例时卖出
    """
    
    def __init__(self, symbol, lookback_period=20, threshold=0.02):  # 2%阈值
        super().__init__(symbol)
        self.lookback_period = lookback_period
        self.threshold = threshold
        
    def generate_signals(self, data):
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0.0
        
        # 计算典型价格
        typical_price = (data['High'] + data['Low'] + data['Close']) / 3
        
        # 计算VWAP
        tp_volume = typical_price * data['Volume']
        vwap_numerator = tp_volume.rolling(window=self.lookback_period).sum()
        vwap_denominator = data['Volume'].rolling(window=self.lookback_period).sum()
        
        vwap = vwap_numerator / vwap_denominator
        signals['vwap'] = vwap
        
        # 计算价格偏离度
        price_deviation = (data['Close'] - vwap) / vwap
        
        # 当价格低于VWAP超过阈值时买入
        signals['buy_signal'] = (
            (price_deviation < -self.threshold) &
            (price_deviation.shift(1) >= -self.threshold)
        )
        
        # 当价格高于VWAP超过阈值时卖出
        signals['sell_signal'] = (
            (price_deviation > self.threshold) &
            (price_deviation.shift(1) <= self.threshold)
        )
        
        # 设置交易信号
        signals.loc[signals['buy_signal'], 'signal'] = 1.0
        signals.loc[signals['sell_signal'], 'signal'] = -1.0
        
        # 生成实际交易信号
        signals['positions'] = signals['signal'].diff()
        
        return signals
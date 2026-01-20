import pandas as pd
import numpy as np
from .base_strategy import BaseStrategy


class MomentumStrategy(BaseStrategy):
    """
    动量策略：基于价格变动方向进行交易
    当价格向上突破时买入，向下突破时卖出
    """
    
    def __init__(self, symbol, short_window=10, long_window=30):
        super().__init__(symbol)
        self.short_window = short_window
        self.long_window = long_window
        
    def generate_signals(self, data):
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0.0
        
        # 计算价格变化率
        signals['price_change_short'] = data['Close'].pct_change(periods=self.short_window)
        signals['price_change_long'] = data['Close'].pct_change(periods=self.long_window)
        
        # 当短期动量大于长期动量且为正时买入
        condition_buy = (
            (signals['price_change_short'] > signals['price_change_long']) &
            (signals['price_change_short'] > 0)
        )
        signals.loc[self.long_window:, 'signal'] = np.where(
            condition_buy[self.long_window:], 1.0, 0.0
        )
        
        # 当短期动量小于长期动量且为负时卖出
        condition_sell = (
            (signals['price_change_short'] < signals['price_change_long']) &
            (signals['price_change_short'] < 0)
        )
        signals.loc[(condition_sell) & (signals['signal'] == 0.0), 'signal'] = -1.0
        
        # 生成实际交易信号
        signals['positions'] = signals['signal'].diff()
        
        return signals
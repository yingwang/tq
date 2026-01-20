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
        
        # 初始化持仓
        signal_arr = np.zeros(len(data))
        current_position = 0.0
        
        for i in range(self.long_window, len(data)):
            # 买入条件：短期动量大于长期动量且为正
            buy_condition = (
                signals['price_change_short'].iloc[i] > signals['price_change_long'].iloc[i] and
                signals['price_change_short'].iloc[i] > 0
            )
            
            # 卖出条件：短期动量小于长期动量且为负
            sell_condition = (
                signals['price_change_short'].iloc[i] < signals['price_change_long'].iloc[i] and
                signals['price_change_short'].iloc[i] < 0
            )
            
            if buy_condition:
                current_position = 1.0
            elif sell_condition:
                current_position = 0.0
            
            signal_arr[i] = current_position
        
        signals['signal'] = signal_arr
        
        # 生成实际交易信号
        signals['positions'] = signals['signal'].diff()
        
        return signals
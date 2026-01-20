import pandas as pd
import numpy as np
from .base_strategy import BaseStrategy


class ADXTrendStrategy(BaseStrategy):
    """
    ADX趋势策略：基于平均趋向指数进行趋势交易
    当ADX显示强劲趋势且+DI上穿-DI时做多，
    当ADX显示强劲趋势且-DI上穿+DI时做空
    """
    
    def __init__(self, symbol, adx_period=14, adx_threshold=25):
        super().__init__(symbol)
        self.adx_period = adx_period
        self.adx_threshold = adx_threshold
        
    def generate_signals(self, data):
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0.0
        
        # 计算真实波幅(TR)
        high_low = data['High'] - data['Low']
        high_close = np.abs(data['High'] - data['Close'].shift())
        low_close = np.abs(data['Low'] - data['Close'].shift())
        
        true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        
        # 计算方向性移动
        up_move = data['High'] - data['High'].shift()
        down_move = data['Low'].shift() - data['Low']
        
        plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0)
        minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0)
        
        # 计算方向性指标
        plus_di_raw = pd.Series(plus_dm).rolling(window=self.adx_period).sum()
        minus_di_raw = pd.Series(minus_dm).rolling(window=self.adx_period).sum()
        tr_sum = true_range.rolling(window=self.adx_period).sum()
        
        # 避免除零错误
        plus_di = 100 * plus_di_raw / np.where(tr_sum == 0, np.nan, tr_sum)
        minus_di = 100 * minus_di_raw / np.where(tr_sum == 0, np.nan, tr_sum)
        
        # 用0填充NaN值
        plus_di = plus_di.fillna(0)
        minus_di = minus_di.fillna(0)
        
        # 计算ADX
        dx = 100 * np.abs(plus_di - minus_di) / np.where((plus_di + minus_di) == 0, np.nan, (plus_di + minus_di))
        dx = dx.fillna(0)  # 用0填充NaN值
        adx = dx.rolling(window=self.adx_period).mean()
        
        signals['plus_di'] = plus_di
        signals['minus_di'] = minus_di
        signals['adx'] = adx
        
        # 当ADX高于阈值且+DI上穿-DI时买入
        signals['buy_signal'] = (
            (adx > self.adx_threshold) &
            (plus_di > minus_di) &
            (plus_di.shift(1) <= minus_di.shift(1))
        )
        
        # 当ADX高于阈值且-DI上穿+DI时卖出
        signals['sell_signal'] = (
            (adx > self.adx_threshold) &
            (minus_di > plus_di) &
            (minus_di.shift(1) <= plus_di.shift(1))
        )
        
        # 设置交易信号
        signals.loc[signals['buy_signal'], 'signal'] = 1.0
        signals.loc[signals['sell_signal'], 'signal'] = -1.0
        
        # 生成实际交易信号
        signals['positions'] = signals['signal'].diff()
        
        return signals
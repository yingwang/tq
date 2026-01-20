import pandas as pd
import numpy as np
from .base_strategy import BaseStrategy


class MeanReversionStrategy(BaseStrategy):
    """
    均值回归策略（长仓）：
    - 使用滚动均线与标准差计算价格的z-score
    - 当z-score低于负阈值（价格显著低于均线）时买入
    - 当z-score回到接近均线（穿越较小负阈值）时平仓
    仅做多，不做空。
    """

    def __init__(self, symbol, window: int = 20, z_entry: float = -1.0, z_exit: float = -0.1):
        super().__init__(symbol)
        self.window = window
        self.z_entry = z_entry
        self.z_exit = z_exit

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0.0

        sma = data['Close'].rolling(window=self.window).mean()
        std = data['Close'].rolling(window=self.window).std()
        z = (data['Close'] - sma) / std

        signals['sma'] = sma
        signals['std'] = std
        signals['zscore'] = z

        signal_arr = np.zeros(len(data))
        position = 0.0

        for i in range(len(data)):
            zi = z.iloc[i]
            # 忽略前期NaN
            if np.isnan(zi):
                signal_arr[i] = position
                continue

            # 进场：zscore低于进场阈值（价格低于均值较多）
            if zi <= self.z_entry:
                position = 1.0
            # 出场：zscore回到接近均值（较小负阈值），锁定回归收益
            elif position == 1.0 and zi >= self.z_exit:
                position = 0.0

            signal_arr[i] = position

        signals['signal'] = signal_arr
        signals['positions'] = signals['signal'].diff()
        return signals

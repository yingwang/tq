import pandas as pd
import numpy as np
from .base_strategy import BaseStrategy


class DollarCostAveragingStrategy(BaseStrategy):
    """
    定投策略（Dollar-Cost Averaging, DCA）
    - 将总仓位在整个期间按固定频率（默认按月）等额买入，逐步从0提升到1。
    - 该实现不引入额外现金流（受当前回测器限制），而是用逐步提高的持仓比例近似定投的平均成本效果。
    - 默认频率：monthly（每月首个交易日增加仓位）。可选 weekly。
    """

    def __init__(self, symbol, frequency: str = "monthly"):
        super().__init__(symbol)
        self.frequency = frequency.lower()

    def _monthly_buy_points(self, index: pd.DatetimeIndex) -> pd.Index:
        # 每月首个交易日
        months = index.to_period('M')
        first_idx = []
        seen = set()
        for i, p in enumerate(months):
            if p not in seen:
                seen.add(p)
                first_idx.append(index[i])
        return pd.Index(first_idx)

    def _weekly_buy_points(self, index: pd.DatetimeIndex) -> pd.Index:
        # 每周首个交易日（ISO 周）
        iso = index.isocalendar()
        weeks = pd.DataFrame({'year': iso.year.values, 'week': iso.week.values})
        first_idx = []
        seen = set()
        for i, (y, w) in enumerate(zip(weeks['year'], weeks['week'])):
            key = (y, w)
            if key not in seen:
                seen.add(key)
                first_idx.append(index[i])
        return pd.Index(first_idx)

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0.0

        idx = data.index
        if self.frequency == 'weekly':
            buy_points = self._weekly_buy_points(idx)
        else:
            buy_points = self._monthly_buy_points(idx)

        periods = len(buy_points)
        if periods <= 0:
            # 无买入期，保持空仓
            signals['positions'] = signals['signal'].diff()
            return signals

        increment = 1.0 / periods
        cumulative = 0.0

        # 构造逐步提升的持仓比例
        for ts in idx:
            if ts in buy_points:
                cumulative = min(1.0, cumulative + increment)
            signals.at[ts, 'signal'] = cumulative

        signals['positions'] = signals['signal'].diff()
        return signals

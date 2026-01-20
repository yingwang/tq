import pandas as pd
import numpy as np
from .base_strategy import BaseStrategy


class BuyAndHoldStrategy(BaseStrategy):
    """
    Buy and Hold Strategy
    Simply buy on the first day and hold until the end
    用作基准对照 (Benchmark)
    """
    
    def __init__(self, symbol):
        super().__init__(symbol)
        
    def generate_signals(self, data):
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0.0
        
        # Set signal to 1.0 for all days (always in position)
        # Backtester will detect this as Buy & Hold and NOT shift
        signals['signal'] = 1.0
        
        # Positions: buy on first day, no more trades
        signals['positions'] = 0.0
        signals.iloc[0, signals.columns.get_loc('positions')] = 1.0  # Buy signal on day 1
        
        return signals

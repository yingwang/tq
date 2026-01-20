"""
Trading strategies module containing various algorithmic strategies
"""

from .base_strategy import BaseStrategy
from .simple_moving_average import SimpleMovingAverageStrategy
from .momentum_strategy import MomentumStrategy
from .bollinger_bands_strategy import BollingerBandsStrategy
from .rsi_strategy import RSIStrategy
from .macd_strategy import MACDStrategy
from .stochastic_oscillator_strategy import StochasticOscillatorStrategy
from .vwap_strategy import VWAPStrategy

__all__ = [
    'BaseStrategy',
    'SimpleMovingAverageStrategy',
    'MomentumStrategy',
    'BollingerBandsStrategy',
    'RSIStrategy',
    'MACDStrategy',
    'StochasticOscillatorStrategy',
    'VWAPStrategy'
]
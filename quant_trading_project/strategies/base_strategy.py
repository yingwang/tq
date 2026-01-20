import pandas as pd


class BaseStrategy:
    """
    策略基类，所有策略都应该继承此类
    """
    
    def __init__(self, symbol):
        self.symbol = symbol
    
    def generate_signals(self, data):
        """
        生成交易信号的抽象方法
        :param data: 包含OHLCV数据的DataFrame
        :return: 包含交易信号的DataFrame
        """
        raise NotImplementedError("子类必须实现generate_signals方法")
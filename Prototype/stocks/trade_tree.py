from stocks.trade import Trade
from typing import List


class Node:
    def __init__(self, trade_value: float, trade: Trade):
        self.key = trade_value
        self.value = [trade]
        self.left = None
        self.right = None


class TradeTree:
    def __init__(self, stock_name: str):
        self.stock_name = stock_name

    def add_trade(self, trade: Trade) -> None:
        pass

    def get_all_trades(self) -> List[Trade]:
        pass

    def get_min_trades(self) -> List[Trade]:
        pass

    def get_max_trades(self) -> List[Trade]:
        pass

    def get_floor_trades(self, low_bound: float) -> List[Trade]:
        pass

    def get_ceil_trades(self, high_bound: float) -> List[Trade]:
        pass

    def get_trades_in_range(self, low_bound: float, high_bound: float) -> List[Trade]:
        pass

from stocks.trade import Trade
from typing import List


class StockTradeLog:
    def __init__(self, stock_name: str):
        pass

    def add_trade(self, trade: Trade) -> None:
        pass

    def get_min_trade(self) -> List[Trade]:
        pass

    def get_max_trade(self) -> List[Trade]:
        pass

    def get_trade_in_range(self, low_bound: float, high_bound: float) -> List[Trade]:
        pass

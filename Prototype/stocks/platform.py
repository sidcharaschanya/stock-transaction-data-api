from stocks.stock_list import STOCKS
from stocks.trade import Trade
from stocks.trade_tree import TradeTree
import typing as t


class StockTradingPlatform:
    def __init__(self) -> None:
        self.trade_trees = {}
        for stock in STOCKS:
            self.trade_trees[stock] = TradeTree(stock)

    def log_transaction(self, transaction_record: list) -> None:
        pass

    def sorted_transactions(self, stock_name: str) -> t.List[Trade]:
        pass

    def min_transactions(self, stock_name: str) -> t.List[Trade]:
        pass

    def max_transactions(self, stock_name: str) -> t.List[Trade]:
        pass

    def floor_transactions(self, stock_name: str, threshold_value: float) -> t.List[Trade]:
        pass

    def ceiling_transactions(self, stock_name: str, threshold_value: float) -> t.List[Trade]:
        pass

    def range_transactions(self, stock_name: str, from_value: float, to_value: float) -> t.List[Trade]:
        pass

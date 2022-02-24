from stocks.trade import Trade
from stocks.stock_list import STOCK_LIST
from stocks.trade_tree import TradeTree
from datetime import datetime
from typing import List

TradeList = List[str, float, int, datetime]


class StockTradingPlatform:
    def __init__(self):
        self.trade_log = {}
        for stock in STOCK_LIST:
            self.trade_log[stock] = TradeTree(stock)

    def log_transaction(self, transaction_record: TradeList) -> None:
        pass

    def sorted_transactions(self, stock_name: str) -> List[Trade]:
        pass

    def min_transactions(self, stock_name: str) -> List[Trade]:
        pass

    def max_transactions(self, stock_name: str) -> List[Trade]:
        pass

    def floor_transactions(self, stock_name: str, threshold_value: float) -> List[Trade]:
        pass

    def ceiling_transactions(self, stock_name: str, threshold_value: float) -> List[Trade]:
        pass

    def range_transactions(self, stock_name: str, from_value: float, to_value: float) -> List[Trade]:
        pass

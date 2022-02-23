from stocks.trade import Trade
from stocks.stock_list import STOCKS
from stocks.stock_trade_log import StockTradeLog
from typing import List


class StockTradingPlatform:

    def __init__(self):
        self.trade_log = {}
        for stock in STOCKS:
            self.trade_log[stock] = StockTradeLog(stock)

    def log_transaction(self, transaction_record: Trade) -> None:
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

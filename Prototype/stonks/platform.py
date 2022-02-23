from stonks.trade import Trade
from stonks.stock_list import STOKCS
from stonks.stock_trade_log import StockTradeLog


class StockTradingPlatform:

    def __init__(self):
        self.trade_log = {}
        for stock in STOKCS:
            self.trade_log[stock] = StockTradeLog(stock)

    def log_transaction(self, transaction_record: Trade) -> None:
        pass

    def sorted_transactions(self, stock_name: str) -> list[Trade]:
        pass

    def min_transactions(self, stock_name: str) -> list[Trade]:
        pass

    def max_transactions(self, stock_name: str) -> list[Trade]:
        pass

    def floor_transactions(self, stock_name: str, threshold_value: float) -> list[Trade]:
        pass

    def ceiling_transactions(self, stock_name: str, threshold_value: float) -> list[Trade]:
        pass

    def range_transactions(self, stock_name: str, from_value: float, to_value: float) -> list[Trade]:
        pass

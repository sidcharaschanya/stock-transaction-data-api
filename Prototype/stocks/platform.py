from stocks.transaction_record import TransactionRecord
from stocks.stock_list import STOCK_LIST
from stocks.stock_trade_log import StockTradeLog
from datetime import datetime
from typing import List

TransactionRecordList = List[str, float, int, datetime]


class StockTradingPlatform:
    def __init__(self):
        self.trade_log = {}
        for stock in STOCK_LIST:
            self.trade_log[stock] = StockTradeLog(stock)

    def log_transaction(self, transaction_record: TransactionRecordList) -> None:
        pass

    def sorted_transactions(self, stock_name: str) -> List[TransactionRecord]:
        pass

    def min_transactions(self, stock_name: str) -> List[TransactionRecord]:
        pass

    def max_transactions(self, stock_name: str) -> List[TransactionRecord]:
        pass

    def floor_transactions(self, stock_name: str, threshold_value: float) -> List[TransactionRecord]:
        pass

    def ceiling_transactions(self, stock_name: str, threshold_value: float) -> List[TransactionRecord]:
        pass

    def range_transactions(self, stock_name: str, from_value: float, to_value: float) -> List[TransactionRecord]:
        pass

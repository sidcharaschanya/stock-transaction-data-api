from datetime import datetime
from typing import Tuple


class TransactionRecord:
    def __init__(self, stock_name: str, stock_price: float, stock_quantity: int, stock_time: datetime) -> None:
        self.stock_name = stock_name
        self.stock_price = stock_price
        self.stock_quantity = stock_quantity
        self.stock_time = stock_time

    def get_trade_val(self) -> float:
        return self.stock_price * self.stock_quantity

    def get_key(self) -> Tuple[float, datetime]:
        return self.get_trade_val(), self.stock_time

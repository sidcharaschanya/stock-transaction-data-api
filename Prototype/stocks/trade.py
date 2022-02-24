import datetime as d


class Trade:
    def __init__(self, name: str, price: float, quantity: int, time: d.datetime) -> None:
        self.name = name
        self.price = price
        self.quantity = quantity
        self.time = time

    def get_trade_val(self) -> float:
        return self.price * self.quantity

    def to_list(self):
        return [self.name, self.price, self.quantity, self.time]

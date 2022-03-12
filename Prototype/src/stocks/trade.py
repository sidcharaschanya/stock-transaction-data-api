# This class models a transaction record.
# It stores all the relevant information associated with a single transaction record.
class Trade:
    def __init__(self, name: str, price: float, quantity: int, time) -> None:
        self.name = name
        self.price = price
        self.quantity = quantity
        self.time = time

    # This helper method makes it easy to retrieve the trade value of a Trade object
    def get_trade_val(self) -> float:
        return self.price * self.quantity

    # Converting to a list makes it easier to work with in some applications and can have performance advantages
    def to_list(self) -> list:
        return [self.name, self.price, self.quantity, self.time]

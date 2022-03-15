# This class models a transaction record
class Trade:
    # Parameterized with all the relevant information associated to a single transaction record
    def __init__(self, name: str, price: float, quantity: int, time) -> None:
        self.name = name
        self.price = price
        self.quantity = quantity
        self.time = time

    # This helper method makes it easy to retrieve the trade value of a Trade object
    def get_trade_val(self) -> float:
        return self.price * self.quantity

    # Converting to a list makes Trade objects easier to work with in some applications
    def to_list(self) -> list:
        return [self.name, self.price, self.quantity, self.time]

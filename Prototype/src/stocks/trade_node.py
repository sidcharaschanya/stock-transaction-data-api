from src.stocks.trade import Trade


# This class models the nodes used in the TradeTree class.
# The trade value is interpreted as the key of a TradeNode object.
# The array of trades is interpreted as the value of a TradeNode object.
class TradeNode:
    RED = True
    BLACK = False

    def __init__(self, trade: Trade) -> None:
        self.trade_val = trade.get_trade_val()

        # Array of all Trade objects with the same trade value
        self.trades = [trade]

        self.left = None
        self.right = None
        self.color = TradeNode.RED

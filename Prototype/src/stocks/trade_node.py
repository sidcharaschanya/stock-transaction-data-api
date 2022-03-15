from src.stocks.trade import Trade


# This class models the nodes used in the TradeTree class
class TradeNode:
    # Constants that represent node color
    RED = True
    BLACK = False

    def __init__(self, trade: Trade) -> None:
        # The trade value is interpreted as the key of a TradeNode object
        self.trade_val = trade.get_trade_val()

        # List of all Trade objects with the same trade value
        self.trades = [trade]

        # References to children nodes
        self.left = None
        self.right = None

        # The color associated to each instance of TradeNode
        self.color = TradeNode.RED

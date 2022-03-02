from stocks.trade import Trade
import typing as t


class TradeNode:
    RED = True
    BLACK = False

    def __init__(self, trade: Trade) -> None:
        self.trade_val = trade.get_trade_val()

        # Array of all nodes with same value
        self.trades = [trade]

        self.left = None
        self.right = None
        self.color = TradeNode.RED

    def to_dict(self) -> t.Dict[float, t.List[list]]:
        # This has a performance advantage over storing the trade as a dictionary; list lookup is much
        # faster than kv lookup and takes better advantage of locality

        # Maps trade value to trade information in list form
        return {self.trade_val: [trade.to_list() for trade in self.trades]}

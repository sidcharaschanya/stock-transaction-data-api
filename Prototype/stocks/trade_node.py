from stocks.trade import Trade
import typing as t


class TradeNode:
    def __init__(self, trade: Trade) -> None:
        self.trade_val = trade.get_trade_val()
        self.trades = [trade]
        self.left = None
        self.right = None

    def to_dict(self) -> t.Dict[float, t.List[list]]:
        return {self.trade_val: [trade.to_list() for trade in self.trades]}

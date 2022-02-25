from stocks.trade_node import TradeNode
from stocks.trade import Trade
import datetime as d
import typing as t


class TradeTree:
    def __init__(self, stock_name: str) -> None:
        self.stock_name = stock_name
        self.root = None

    def put_trade(self, trade: Trade, node: TradeNode = None) -> None:
        if trade.name != self.stock_name:
            print("Invalid stock name")
            return

        if self.root is None:
            self.root = TradeNode(trade)
            return

        if node is None:
            node = self.root

        trade_val = trade.get_trade_val()

        if trade_val == node.trade_val:
            node.trades.append(trade)
        elif trade_val < node.trade_val:
            if node.left is None:
                node.left = TradeNode(trade)
            else:
                self.put_trade(trade, node.left)
        elif trade_val > node.trade_val:
            if node.right is None:
                node.right = TradeNode(trade)
            else:
                self.put_trade(trade, node.right)

    def get_all_trades(self, node: TradeNode = None) -> t.List[Trade]:
        if self.root is None:
            return []

        if node is None:
            node = self.root

        all_trades = []

        if node.left is not None:
            all_trades = self.get_all_trades(node.left)

        all_trades += node.trades

        if node.right is not None:
            all_trades += self.get_all_trades(node.right)

        return all_trades

    def get_min_trades(self) -> t.List[Trade]:
        if self.root is None:
            return []

        node = self.root

        while node.left is not None:
            node = node.left

        return node.trades

    def get_max_trades(self) -> t.List[Trade]:
        if self.root is None:
            return []

        node = self.root

        while node.right is not None:
            node = node.right

        return node.trades

    def get_floor_trades(self, low: float) -> t.List[Trade]:
        pass

    def get_ceil_trades(self, high: float) -> t.List[Trade]:
        pass

    def get_trades_in_range(self, low: float, high: float) -> t.List[Trade]:
        pass


if __name__ == '__main__':
    st = d.datetime.strptime('1/1/2022 1:00:00', '%d/%m/%Y %H:%M:%S')
    t1 = Trade("test_stock", 89.9, 10, st + d.timedelta(seconds = 3))
    t2 = Trade("test_stock", 79.9, 10, st + d.timedelta(seconds = 6))
    t3 = Trade("test_stock", 99.9, 10, st + d.timedelta(seconds = 9))
    t4 = Trade("test_stock", 99.9, 10, st + d.timedelta(seconds = 12))

    tree = TradeTree("test_stock")
    tree.put_trade(t1)
    tree.put_trade(t2)
    tree.put_trade(t3)
    tree.put_trade(t4)

    print(tree.root.left.to_dict())
    print(tree.root.to_dict())
    print(tree.root.right.to_dict())
    print([trade.get_trade_val() for trade in tree.get_all_trades()])
    print(tree.get_all_trades())
    print(tree.get_min_trades())
    print(tree.get_max_trades())

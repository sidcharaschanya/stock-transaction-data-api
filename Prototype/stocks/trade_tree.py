from stocks.trade import Trade
import datetime as d
import typing as t


class Node:
    def __init__(self, trade: Trade):
        self.key = trade.get_trade_val()
        self.value = [trade]
        self.left = None
        self.right = None

    def to_dict(self):
        return {self.key: [trade.to_list() for trade in self.value]}


class TradeTree:
    def __init__(self, stock_name: str):
        self.stock_name = stock_name
        self.root = None

    def put_trade(self, trade: Trade, node: Node = None) -> None:
        if trade.name != self.stock_name:
            print("Invalid stock name")
            return

        if self.root is None:
            self.root = Node(trade)
            return

        if node is None:
            node = self.root

        key = trade.get_trade_val()

        if key == node.key:
            node.value.append(trade)
        elif key < node.key:
            if node.left is None:
                node.left = Node(trade)
            else:
                self.put_trade(trade, node.left)
        elif key > node.key:
            if node.right is None:
                node.right = Node(trade)
            else:
                self.put_trade(trade, node.right)

    def get_all_trades(self, node: Node = None) -> t.List[Trade]:
        if self.root is None:
            return []

        if node is None:
            node = self.root

        trades = []

        if node.left is not None:
            trades = self.get_all_trades(node.left)

        trades += node.value

        if node.right is not None:
            trades += self.get_all_trades(node.right)

        return trades

    def get_min_trades(self) -> t.List[Trade]:
        if self.root is None:
            return []

        node = self.root

        while node.left is not None:
            node = node.left

        return node.value

    def get_max_trades(self) -> t.List[Trade]:
        if self.root is None:
            return []

        node = self.root

        while node.right is not None:
            node = node.right

        return node.value

    def get_floor_trades(self, low_bound: float) -> t.List[Trade]:
        pass

    def get_ceil_trades(self, high_bound: float) -> t.List[Trade]:
        pass

    def get_trades_in_range(self, low_bound: float, high_bound: float) -> t.List[Trade]:
        pass


if __name__ == '__main__':
    st = d.datetime.strptime('1/1/2022 1:00:00', '%d/%m/%Y %H:%M:%S')
    t1 = Trade("test_stock", 89.9, 10, st + d.timedelta(seconds = 3))
    t2 = Trade("test_stock", 79.9, 10, st + d.timedelta(seconds = 6))
    t3 = Trade("test_stock", 99.9, 10, st + d.timedelta(seconds = 9))
    t4 = Trade("test_stock", 99.9, 10, st + d.timedelta(seconds = 12))

    trade_tree = TradeTree("test_stock")
    trade_tree.put_trade(t1)
    trade_tree.put_trade(t2)
    trade_tree.put_trade(t3)
    trade_tree.put_trade(t4)

    print(trade_tree.root.left.to_dict())
    print(trade_tree.root.to_dict())
    print(trade_tree.root.right.to_dict())
    print([trade.get_trade_val() for trade in trade_tree.get_all_trades()])
    print(trade_tree.get_all_trades())
    print(trade_tree.get_min_trades())
    print(trade_tree.get_max_trades())

from trade import Trade
from trade_node import TradeNode
import datetime as d
import typing as t


class TradeTree:
    # TradeTree models all information for a single stock
    # i.e. all trades on a given stock will be stored here
    # This has no model of any other stocks

    def __init__(self, stock_name: str) -> None:
        self.stock_name = stock_name
        self.root = None

    def put_trade(self, trade: Trade) -> None:
        if trade.name != self.stock_name:
            raise ValueError("Invalid stock name")

        self.root = self.__insert(trade, self.root)
        self.root.color = TradeNode.BLACK

    def __insert(self, trade: Trade, node: TradeNode) -> TradeNode:
        if node is None:
            return TradeNode(trade)

        trade_val = trade.get_trade_val()

        if trade_val == node.trade_val:
            node.trades.append(trade)
        elif trade_val < node.trade_val:
            node.left = self.__insert(trade, node.left)
        elif trade_val > node.trade_val:
            node.right = self.__insert(trade, node.right)

        return TradeTree.__balance(node)

    def get_all_trades(self, node: TradeNode = None) -> t.List[Trade]:
        if self.root is None:
            return []

        # Optional node parameter used to display some other tree or some subtree
        if node is None:
            node = self.root

        all_trades = []

        if node.left is not None:
            all_trades = self.get_all_trades(node.left)

        all_trades.extend(node.trades)

        if node.right is not None:
            all_trades.extend(self.get_all_trades(node.right))

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

    def get_trades_in_range(self, low: float, high: float, node: TradeNode = None) -> t.List[Trade]:
        if self.root is None:
            return []

        if node is None:
            node = self.root

        trades_in_range = []

        if low <= node.trade_val <= high:
            if node.left is not None:
                trades_in_range = self.get_trades_in_range(low, high, node.left)

            trades_in_range.extend(node.trades)

            if node.right is not None:
                trades_in_range.extend(self.get_trades_in_range(low, high, node.right))
        elif node.trade_val < low and node.right is not None:
            trades_in_range = self.get_trades_in_range(low, high, node.right)
        elif node.trade_val > high and node.left is not None:
            trades_in_range = self.get_trades_in_range(low, high, node.left)

        return trades_in_range

    @staticmethod
    def __rotate_left(node: TradeNode) -> TradeNode:
        x = node.right
        node.right = x.left
        x.left = node
        x.color = node.color
        node.color = TradeNode.RED
        return x

    @staticmethod
    def __rotate_right(node: TradeNode) -> TradeNode:
        x = node.left
        node.left = x.right
        x.right = node
        x.color = node.color
        node.color = TradeNode.RED
        return x

    @staticmethod
    def __flip_colors(node: TradeNode) -> None:
        node.color = TradeNode.RED
        node.left.color = TradeNode.BLACK
        node.right.color = TradeNode.BLACK

    @staticmethod
    def __is_red(node: TradeNode) -> bool:
        return node.color == TradeNode.RED if node is not None else False

    @staticmethod
    def __balance(node: TradeNode) -> TradeNode:
        if TradeTree.__is_red(node.right) and not TradeTree.__is_red(node.left):
            node = TradeTree.__rotate_left(node)

        if TradeTree.__is_red(node.left) and TradeTree.__is_red(node.left.left):
            node = TradeTree.__rotate_right(node)

        if TradeTree.__is_red(node.left) and TradeTree.__is_red(node.right):
            TradeTree.__flip_colors(node)

        return node


if __name__ == '__main__':
    # TODO: chuck this for final rev.
    st = d.datetime.strptime('1/1/2022 1:00:00', '%d/%m/%Y %H:%M:%S')
    t1 = Trade("test_stock", 79.9, 10, st + d.timedelta(seconds = 3))
    t2 = Trade("test_stock", 89.9, 10, st + d.timedelta(seconds = 6))
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
    print(tree.get_trades_in_range(800, 999))

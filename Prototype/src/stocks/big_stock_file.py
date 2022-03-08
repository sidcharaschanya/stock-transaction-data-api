# ===========================INCLUDE ALL BELOW IN JUPYTER NOTEBOOK===========================

import datetime as d
import typing as t


# This class models a transaction record.
# It stores all the relevant information associated with a single transaction record.
class Trade:
    def __init__(self, name: str, price: float, quantity: int, time: d.datetime) -> None:
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


# This class models all information for a single stock name.
# All trades on a given stock will be stored here.
# This has no model of any other stocks.
# It implements a balanced search tree ADT using a left-leaning red-black binary search tree.
# Each node in the tree is a TradeNode object.
class TradeTree:
    def __init__(self, stock_name: str) -> None:
        self.stock_name = stock_name
        self.root = None

    def put_trade(self, trade: Trade) -> None:
        # Ensure that the Trade object to be inserted matches the stock name of the current TradeTree object
        if trade.name != self.stock_name:
            raise ValueError("Invalid Stock Name")

        self.root = self.__insert(trade, self.root)

        # Maintain invariant of coloring root node black
        self.root.color = TradeNode.BLACK

    def __insert(self, trade: Trade, node: TradeNode) -> TradeNode:
        if node is None:
            return TradeNode(trade)

        # Use trade value as the key for inserting TradeNode objects into the TradeTree
        trade_val = trade.get_trade_val()

        if trade_val == node.trade_val:
            node.trades.append(trade)
        elif trade_val < node.trade_val:
            node.left = self.__insert(trade, node.left)
        elif trade_val > node.trade_val:
            node.right = self.__insert(trade, node.right)

        # Recursively balance the TradeTree to maintain logarithmic height
        return TradeTree.__balance(node)

    def get_all_trades(self, node: TradeNode = None) -> t.List[Trade]:
        # Base case where the root of the TradeTree has not been initialized
        if self.root is None:
            return []

        # Optional node parameter used to display some subtree
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

    def get_floor_trades(self, high: float) -> t.List[Trade]:
        node = self.root
        floor_trades = []

        while node is not None:
            if node.trade_val == high:
                return node.trades
            elif node.trade_val < high:
                floor_trades = node.trades
                node = node.right
            elif node.trade_val > high:
                node = node.left

        return floor_trades

    def get_ceil_trades(self, low: float) -> t.List[Trade]:
        node = self.root
        ceil_trades = []

        while node is not None:
            if node.trade_val == low:
                return node.trades
            elif node.trade_val > low:
                ceil_trades = node.trades
                node = node.left
            elif node.trade_val < low:
                node = node.right

        return ceil_trades

    def get_trades_in_range(self, low: float, high: float, node: TradeNode = None) -> t.List[Trade]:
        # Ensure that the low and high parameters are valid
        if low > high or low < 0:
            raise ValueError("Invalid Range")

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

    # This method maintains the structural invariants of a left-leaning red-black binary search tree
    @staticmethod
    def __balance(node: TradeNode) -> TradeNode:
        if TradeTree.__is_red(node.right) and not TradeTree.__is_red(node.left):
            node = TradeTree.__rotate_left(node)

        if TradeTree.__is_red(node.left) and TradeTree.__is_red(node.left.left):
            node = TradeTree.__rotate_right(node)

        if TradeTree.__is_red(node.left) and TradeTree.__is_red(node.right):
            TradeTree.__flip_colors(node)

        return node
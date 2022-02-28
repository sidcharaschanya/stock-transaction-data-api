from trade import Trade
from trade_tree import TradeTree
import typing as t


class StockTradingPlatform:
    def __init__(self) -> None:
        self.STOCKS = {"Barclays", "HSBA", "Lloyds", "Banking Group", "NatWest Group", "Standard Chartered", "3i",
                       "Abrdn", "Hargreaves Lansdown", "London Stock Exchange Group", "Pershing Square Holdings",
                       "Schroders", "St. James's Place plc."}
        self.__trade_trees = {}

        for stock in self.STOCKS:
            self.__trade_trees[stock] = TradeTree(stock)

    def log_transaction(self, trade: Trade):
        self.__validate_trade(trade)

        self.__trade_trees[trade.name].put_trade(trade)

    def sorted_transactions(self, stock_name: str) -> t.List[Trade]:
        if stock_name not in self.STOCKS:
            raise ValueError("That stock was not found")

        return self.__trade_trees[stock_name].get_all_trades()

    def min_transactions(self, stock_name: str) -> t.List[Trade]:
        if stock_name not in self.STOCKS:
            raise ValueError("MAX: That stock was not found")

        return self.__trade_trees[stock_name].get_min_trades()

    def max_transactions(self, stock_name: str) -> t.List[Trade]:
        if stock_name not in self.STOCKS:
            raise ValueError("MAX: That stock was not found")

        return self.__trade_trees[stock_name].get_max_trades()

    def floor_transactions(self, stock_name: str, threshold_value: float) -> t.List[Trade]:
        if stock_name not in self.STOCKS:
            raise ValueError("FLOOR: That stock was not found")

        if threshold_value < 0:
            raise ValueError("FLOOR: Cannot have negative transactions")

        return self.__trade_trees[stock_name].get_floor_trades(threshold_value)

    def ceiling_transactions(self, stock_name: str, threshold_value: float) -> t.List[Trade]:
        if stock_name not in self.STOCKS:
            raise ValueError("CEILING: That stock was not found")

        if threshold_value < 0:
            raise ValueError("CEILING: Cannot have a negative trade value")

        return self.__trade_trees[stock_name].get_ceil_trades(threshold_value)

    def range_transactions(self, stock_name: str, from_value: float, to_value: float) -> t.List[Trade]:
        if stock_name not in self.STOCKS:
            raise ValueError("RANGE: That stock was not found")

        if from_value > to_value or from_value < 0 or to_value < 0:
            raise ValueError("RANGE: Bad range bounds")

        return self.__trade_trees[stock_name].get_trades_in_range(from_value, to_value)

    def __validate_trade(self, trade: Trade) -> None:
        if trade.name not in self.STOCKS:
            raise ValueError("Bad name " + trade.name)

        if trade.quantity < 1:
            raise ValueError("Bad quantity " + str(trade.quantity))

        if trade.price <= 0.0:
            raise ValueError("Bad price " + str(trade.price))

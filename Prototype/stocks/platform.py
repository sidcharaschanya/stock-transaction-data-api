from trade import Trade
from trade_tree import TradeTree
import typing as t


# noinspection PyPep8Naming
class StockTradingPlatform:
    def __init__(self) -> None:
        # noinspection SpellCheckingInspection
        self.STOCKS = {"Barclays", "HSBA", "Lloyds", "Banking Group", "NatWest Group", "Standard Chartered", "3i",
                       "Abrdn", "Hargreaves Lansdown", "London Stock Exchange Group", "Pershing Square Holdings",
                       "Schroders", "St. James's Place plc."}

        self.__trade_trees = {}

        for stock in self.STOCKS:
            self.__trade_trees[stock] = TradeTree(stock)

    def logTransaction(self, transactionRecord: list) -> None:
        trade = Trade(*transactionRecord)
        self.__validate_trade(trade)
        self.__trade_trees[trade.name].put_trade(trade)

    def sortedTransactions(self, stockName: str) -> t.List[Trade]:
        if stockName not in self.STOCKS:
            raise ValueError("That stock was not found")

        return self.__trade_trees[stockName].get_all_trades()

    def minTransactions(self, stockName: str) -> t.List[Trade]:
        if stockName not in self.STOCKS:
            raise ValueError("MAX: That stock was not found")

        return self.__trade_trees[stockName].get_min_trades()

    def maxTransactions(self, stockName: str) -> t.List[Trade]:
        if stockName not in self.STOCKS:
            raise ValueError("MAX: That stock was not found")

        return self.__trade_trees[stockName].get_max_trades()

    def floorTransactions(self, stockName: str, thresholdValue: float) -> t.List[Trade]:
        if stockName not in self.STOCKS:
            raise ValueError("FLOOR: That stock was not found")

        if thresholdValue < 0:
            raise ValueError("FLOOR: Cannot have negative transactions")

        return self.__trade_trees[stockName].get_floor_trades(thresholdValue)

    def ceilingTransactions(self, stockName: str, thresholdValue: float) -> t.List[Trade]:
        if stockName not in self.STOCKS:
            raise ValueError("CEILING: That stock was not found")

        if thresholdValue < 0:
            raise ValueError("CEILING: Cannot have a negative trade value")

        return self.__trade_trees[stockName].get_ceil_trades(thresholdValue)

    def rangeTransactions(self, stockName: str, fromValue: float, toValue: float) -> t.List[Trade]:
        if stockName not in self.STOCKS:
            raise ValueError("RANGE: That stock was not found")

        if fromValue > toValue or fromValue < 0 or toValue < 0:
            raise ValueError("RANGE: Bad range bounds")

        return self.__trade_trees[stockName].get_trades_in_range(fromValue, toValue)

    def __validate_trade(self, trade: Trade) -> None:
        if trade.name not in self.STOCKS:
            raise ValueError("Bad name " + trade.name)

        if trade.quantity < 1:
            raise ValueError("Bad quantity " + str(trade.quantity))

        if trade.price <= 0.0:
            raise ValueError("Bad price " + str(trade.price))

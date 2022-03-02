from datetime import datetime, timedelta
from random import choice, seed, uniform, randint
from stocks.platform import StockTradingPlatform
from stocks.trade import Trade
from stocks.trade_tree import TradeTree
import typing as t


class TestSets:
    def __init__(self):

        _platform = StockTradingPlatform()
        self.__stocks = tuple(_platform.STOCKS)

        self.__min_trade_value = 500.00
        self.__max_trade_value = 100000.00
        self.__start_date = datetime.strptime('1/1/2022 1:00:00', '%d/%m/%Y %H:%M:%S')
        seed(20221603)
        self.__time_offset = 0

    def __get_value(self, min_val, max_val) -> t.Tuple[int, int]:
        if min_val == max_val:
            return min_val, 1

        if max_val / 5 < min_val:
            return round(uniform(min_val, max_val)), 1

        return round(uniform(min_val, max_val / 5)), randint(1, 5)

    def gen_one_trade(self, stock, min_val, max_val):
        self.__time_offset += 1
        value = self.__get_value(min_val, max_val)

        return Trade(stock,
                     value[0], value[1],
                     self.__start_date + timedelta(seconds = self.__time_offset))

    def trade_gen_many_same_stock(self, stock: str = "HSBA", min_val: int = 1, max_val: int = 100000) -> t.List[Trade]:
        trade_list = []
        self.__time_offset += 1
        trade_list.append(Trade(stock, min_val, 1, self.__start_date + timedelta(seconds = self.__time_offset)))

        for _ in range(98):
            trade_list.append(self.gen_one_trade(stock, min_val, max_val))

        trade_list.append(Trade(stock, max_val, 1, self.__start_date + timedelta(seconds = self.__time_offset)))

        return trade_list

    def trade_gen_many_same_value(self, value: float) -> t.List[Trade]:
        trade_list = []

        for i in range(100):
            trade_list.append(self.gen_one_trade(choice(self.__stocks), value, value))

        return trade_list

    def trade_gen_many(self, min_val: int = 1, max_val: int = 100000) -> t.List[Trade]:
        trade_list = []

        for _ in range(100):
            trade_list.append(self.gen_one_trade(choice(self.__stocks), min_val, max_val))

        return trade_list

    def tree_gen_many_same_val(self, value: float, stock: str = "HSBA") -> TradeTree:
        tree = TradeTree(stock)
        trades = self.trade_gen_many_same_value(value)

        for trade in trades:
            tree.put_trade(trade)

        return tree

    def tree_gen_many(self, min_val: int = 1, max_val: int = 100000, stock: str = "HSBA") -> TradeTree:
        tree = TradeTree(stock)
        trades = self.trade_gen_many_same_stock(stock, min_val, max_val)

        for trade in trades:
            tree.put_trade(trade)

        return tree

    def platform_gen_many_same_stock(self, stock: str, low: int = 1, high: int = 100000) -> StockTradingPlatform:
        platform = StockTradingPlatform()
        trades = self.trade_gen_many_same_stock(stock, low, high)

        for trade in trades:
            platform.logTransaction(trade)

        return platform

    def platform_gen_many_same_val(self, value: float) -> StockTradingPlatform:
        platform = StockTradingPlatform()
        trades = self.trade_gen_many_same_value(value)

        for trade in trades:
            platform.logTransaction(trade)

        return platform

    def platform_gen_many(self, low: int = 1, high: int = 100000) -> StockTradingPlatform:
        platform = StockTradingPlatform()
        trades = self.trade_gen_many(low, high)

        for trade in trades:
            platform.logTransaction(trade)

        return platform

from src.stocks.trade import Trade
from src.stocks.platform import StockTradingPlatform
from src.stocks.trade_tree import TradeTree
from unittest import TestCase, defaultTestLoader, TextTestRunner
from datetime import datetime, timedelta
from random import choice, seed, uniform, randint
import typing as t

SAMPLE_DATE = datetime.strptime('1/1/2022 1:00:00', '%d/%m/%Y %H:%M:%S')
SAMPLE_STOCK = "HSBA"
SAMPLE_MIN_VAL = 100
SAMPLE_MAX_VAL = 100000
SAMPLE_SIZE = 100


class TestSets:
    def __init__(self):

        _platform = StockTradingPlatform()
        self.__stocks = tuple(_platform.STOCKS)
        self.__start_date = datetime.strptime('1/1/2022 1:00:00', '%d/%m/%Y %H:%M:%S')
        seed(20221603)
        self.__time_offset = 0

    @staticmethod
    def __get_value(min_val, max_val) -> t.Tuple[int, int]:
        if min_val == max_val:
            return min_val, 1

        if max_val / 5 < min_val:
            return round(uniform(min_val, max_val)), 1

        return round(uniform(min_val, max_val / 5)), randint(1, 5)

    def gen_one_trade(self, stock, min_val, max_val) -> list:
        self.__time_offset += 1
        value = self.__get_value(min_val, max_val)

        return [stock,
                value[0], value[1],
                self.__start_date + timedelta(seconds = self.__time_offset)]

    def trade_gen_many_same_stock(self, stock: str = SAMPLE_STOCK, min_val: int = SAMPLE_MIN_VAL,
                                  max_val: int = SAMPLE_MAX_VAL, n: int = SAMPLE_SIZE) -> t.List[list]:
        trade_list = []
        self.__time_offset += 1
        trade_list.append([stock, min_val, 1, self.__start_date + timedelta(seconds = self.__time_offset)])

        for _ in range(n - 2):
            trade_list.append(self.gen_one_trade(stock, min_val, max_val))

        trade_list.append([stock, max_val, 1, self.__start_date + timedelta(seconds = self.__time_offset)])

        return trade_list

    def trade_gen_many_same_value(self, value: float, n: int = SAMPLE_SIZE) -> t.List[list]:
        trade_list = []

        for i in range(n):
            trade_list.append(self.gen_one_trade(choice(self.__stocks), value, value))

        return trade_list

    def trade_gen_many(self, min_val: int = SAMPLE_MIN_VAL, max_val: int = SAMPLE_MAX_VAL, n: int = SAMPLE_SIZE) \
            -> t.List[list]:
        trade_list = []

        for _ in range(n):
            trade_list.append(self.gen_one_trade(choice(self.__stocks), min_val, max_val))

        return trade_list

    def tree_gen_many_same_val(self, value: float, stock: str = SAMPLE_STOCK, n: int = SAMPLE_SIZE) \
            -> t.Tuple[TradeTree, t.List[list]]:
        tree = TradeTree(stock)
        trade_list = self.trade_gen_many_same_value(value, n = n)

        for trade in trade_list:
            tree.put_trade(Trade(*trade))

        return tree, trade_list

    def tree_gen_many(self, min_val: int = SAMPLE_MIN_VAL, max_val: int = SAMPLE_MAX_VAL, stock: str = SAMPLE_STOCK,
                      n: int = SAMPLE_SIZE) -> t.Tuple[TradeTree, t.List[list]]:

        tree = TradeTree(stock)
        trade_list = self.trade_gen_many_same_stock(stock, min_val, max_val, n = n)

        for trade in trade_list:
            tree.put_trade(Trade(*trade))

        return tree, trade_list

    def platform_gen_many_same_stock(self, stock: str, low: int = SAMPLE_MIN_VAL, high: int = SAMPLE_MAX_VAL,
                                     n: int = SAMPLE_SIZE) -> t.Tuple[StockTradingPlatform, t.List[list]]:

        platform = StockTradingPlatform()
        trade_list = self.trade_gen_many_same_stock(stock, low, high, n = n)

        for trade in trade_list:
            platform.logTransaction(trade)

        return platform, trade_list

    def platform_gen_many_same_val(self, value: float, n: int = SAMPLE_SIZE) \
            -> t.Tuple[StockTradingPlatform, t.List[list]]:

        platform = StockTradingPlatform()
        trade_list = self.trade_gen_many_same_value(value, n = n)

        for trade in trade_list:
            platform.logTransaction(trade)

        return platform, trade_list

    def platform_gen_many(self, low: int = SAMPLE_MIN_VAL, high: int = SAMPLE_MAX_VAL) \
            -> t.Tuple[StockTradingPlatform, t.List[list]]:

        platform = StockTradingPlatform()
        trade_list = self.trade_gen_many(low, high)

        for trade in trade_list:
            platform.logTransaction(trade)

        return platform, trade_list


test_sets = TestSets()


class TestStockTradingPlatform(TestCase):

    @staticmethod
    def __trades_equal(trade_1: Trade, trade_2: Trade) -> bool:
        return trade_1.name == trade_2.name and trade_1.price == trade_2.price \
               and trade_1.quantity == trade_2.quantity and trade_1.time == trade_2.time

    def test_log_bad_stock(self):
        sut = StockTradingPlatform()
        try:
            sut.logTransaction(["UCL Bank", 1, 1, SAMPLE_DATE])
            self.assertFalse(True)
        except ValueError as e:
            self.assertEqual(e.args[0], "Invalid Stock Name: UCL Bank")
        except:
            self.assertFalse(True)

    def test_log_bad_stock_value(self):
        sut = StockTradingPlatform()
        try:
            sut.logTransaction([SAMPLE_STOCK, 0, 1, SAMPLE_DATE])
        except ValueError as e:
            self.assertEqual("Invalid Stock Price: 0", e.args[0])
        except:
            self.assertFalse(True)

    def test_log_bad_quantity(self):
        sut = StockTradingPlatform()
        try:
            sut.logTransaction([SAMPLE_STOCK, 100, 0, SAMPLE_DATE])
        except ValueError as e:
            self.assertEqual("Invalid Stock Quantity: 0", e.args[0])
        except:
            self.assertFalse(True)

    def test_log_insert_first(self):
        sut = StockTradingPlatform()
        trade = [SAMPLE_STOCK, 100, 2, SAMPLE_DATE]

        sut.logTransaction(trade)

        result = sut.sortedTransactions(SAMPLE_STOCK)

        self.assertEqual(len(result), 1)
        self.assertTrue(self.__trades_equal(result[0], Trade(*trade)))

    def test_log_many_of_one(self):
        # This generates 100 trades for HSBA with a min value equal to SAMPLE_MIN_VAL and a max value of SAMPLE_MAX_VAL
        sut, test_trades = test_sets.platform_gen_many_same_stock(stock = SAMPLE_STOCK,
                                                                  low = SAMPLE_MIN_VAL, high = SAMPLE_MAX_VAL)

        trade_list = sut.sortedTransactions(SAMPLE_STOCK)

        # Assert right number of trades were inserted
        self.assertEqual(len(test_trades), len(trade_list))

        # Assert trade with correct minimum value was inserted
        self.assertEqual(sut.minTransactions(SAMPLE_STOCK)[0].get_trade_val(), SAMPLE_MIN_VAL)

        # Assert trade with correct maximum value was inserted
        self.assertEqual(sut.maxTransactions(SAMPLE_STOCK)[0].get_trade_val(), SAMPLE_MAX_VAL)

    def test_log_one_of_each(self):
        sut = StockTradingPlatform()

        for stock in sut.STOCKS:
            sut.logTransaction(test_sets.gen_one_trade(stock, SAMPLE_MIN_VAL, SAMPLE_MAX_VAL))

        for stock in sut.STOCKS:
            self.assertEqual(len(sut.sortedTransactions(stock)), 1)

    def test_log(self):
        sut = StockTradingPlatform()

        sut.logTransaction(["London Stock Exchange Group",
                            1000, 5,
                            datetime.strptime("2020-02-25T22:00:15", "%Y-%m-%dT%H:%M:%S")])

        self.assertTrue(True)

    def test_log_all_same_trade_val(self):
        sut, trades = test_sets.platform_gen_many_same_val(250)

        for stock in sut.STOCKS:
            self.assertEqual(sut.minTransactions(stock), sut.maxTransactions(stock))

    def test_log_some_conflicts(self):
        trades1 = test_sets.trade_gen_many_same_value(550)
        trades2 = test_sets.trade_gen_many(min_val = SAMPLE_MIN_VAL, max_val = SAMPLE_MAX_VAL)
        sut = StockTradingPlatform()

        for trade in trades1 + trades2:
            sut.logTransaction(trade)

        total_len = 0
        for stock in sut.STOCKS:
            total_len += len(sut.sortedTransactions(stock))

        self.assertEqual(total_len, len(trades1) + len(trades2))

    def test_sorted_transactions_empty(self):
        sut = StockTradingPlatform()

        result = sut.sortedTransactions(SAMPLE_STOCK)

        self.assertEqual(result, [])

    def test_sorted_one(self):
        trade = test_sets.gen_one_trade(SAMPLE_STOCK, min_val = SAMPLE_MIN_VAL, max_val = SAMPLE_MIN_VAL)
        sut = StockTradingPlatform()
        sut.logTransaction(trade)

        result = sut.sortedTransactions(SAMPLE_STOCK)

        self.assertTrue(self.__trades_equal(result[0], Trade(*trade)))

    def test_sorted_many(self):
        sut, trades = test_sets.platform_gen_many_same_stock(SAMPLE_STOCK)
        trades.sort(key = lambda x: x[1] * x[2])

        sorted_trades = sut.sortedTransactions(SAMPLE_STOCK)

        for index, trade in enumerate(trades):
            self.assertTrue(self.__trades_equal(sorted_trades[index], Trade(*trade)))

    def test_sorted_all_one_val(self):
        sut, _ = test_sets.platform_gen_many_same_val(500)

        trade_list = sut.sortedTransactions(SAMPLE_STOCK)

        # Essentially, just make sure nothing breaks
        for trade in trade_list:
            self.assertEqual(trade.get_trade_val(), 500)

    def test_min_transactions_none(self):
        sut = StockTradingPlatform()

        min_t = sut.minTransactions(SAMPLE_STOCK)

        self.assertEqual([], min_t)

    def test_min_transactions_all_same(self):
        sut, _ = test_sets.platform_gen_many_same_val(5000)

        min_trades = sut.minTransactions(SAMPLE_STOCK)

        for trade in min_trades:
            self.assertEqual(trade.get_trade_val(), 5000)

    def test_min_transactions(self):
        sut, _ = test_sets.platform_gen_many_same_stock(low = SAMPLE_MIN_VAL, high = SAMPLE_MAX_VAL,
                                                        stock = SAMPLE_STOCK)

        min_set = sut.minTransactions(SAMPLE_STOCK)

        self.assertEqual(SAMPLE_MIN_VAL, min_set[0].get_trade_val())

    def test_min_transactions_one(self):
        sut = StockTradingPlatform()
        trade = [SAMPLE_STOCK, 500, 2, SAMPLE_DATE]
        sut.logTransaction(trade)

        min_set = sut.minTransactions(SAMPLE_STOCK)

        self.assertEqual(len(min_set), 1)
        self.assertTrue(self.__trades_equal(min_set[0], Trade(*trade)))

    def test_min_bad_name(self):
        sut = StockTradingPlatform()

        try:
            sut.minTransactions("UCL Bank")
            self.assertFalse(True)
        except ValueError as e:
            self.assertEqual(e.args[0], "minTransactions: Invalid Stock Name: UCL Bank")
        except:
            self.assertFalse(True)

    def test_max_transactions_none(self):
        sut = StockTradingPlatform()

        max_t = sut.minTransactions(SAMPLE_STOCK)

        self.assertEqual([], max_t)

    def test_max_transactions_all_same(self):
        sut, _ = test_sets.platform_gen_many_same_val(5000)

        max_trades = sut.maxTransactions(SAMPLE_STOCK)

        for trade in max_trades:
            self.assertEqual(trade.get_trade_val(), 5000)

    def test_max_transactions(self):
        sut, _ = test_sets.platform_gen_many_same_stock(low = SAMPLE_MIN_VAL, high = SAMPLE_MAX_VAL,
                                                        stock = SAMPLE_STOCK)

        max_set = sut.maxTransactions(SAMPLE_STOCK)

        self.assertEqual(SAMPLE_MAX_VAL, max_set[0].get_trade_val())

    def test_max_transactions_one(self):
        sut = StockTradingPlatform()
        trade = [SAMPLE_STOCK, 500, 2, SAMPLE_DATE]
        sut.logTransaction(trade)

        max_set = sut.minTransactions(SAMPLE_STOCK)

        self.assertEqual(len(max_set), 1)
        self.assertTrue(self.__trades_equal(max_set[0], Trade(*trade)))

    def test_max_bad_name(self):
        sut = StockTradingPlatform()

        try:
            sut.maxTransactions("UCL Bank")
            self.assertFalse(True)
        except ValueError as e:
            self.assertEqual(e.args[0], "maxTransactions: Invalid Stock Name: UCL Bank")
        except:
            self.assertFalse(True)

    def test_floor_transactions_empty(self):
        sut = StockTradingPlatform()

        floor = sut.floorTransactions(SAMPLE_STOCK, 100)

        self.assertEqual(floor, [])

    def test_floor_below_min(self):
        sut, _ = test_sets.platform_gen_many_same_stock(SAMPLE_STOCK, low = SAMPLE_MIN_VAL)

        floor = sut.floorTransactions(SAMPLE_STOCK, SAMPLE_MIN_VAL - 1)

        self.assertEqual([], floor)

    def test_floor_above_max(self):
        sut, _ = test_sets.platform_gen_many_same_stock(SAMPLE_STOCK, high = SAMPLE_MAX_VAL)

        floor = sut.floorTransactions(SAMPLE_STOCK, SAMPLE_MAX_VAL + 1)

        self.assertEqual(floor[0].get_trade_val(), SAMPLE_MAX_VAL)

    def test_floor_equal_min(self):
        sut, _ = test_sets.platform_gen_many_same_stock(SAMPLE_STOCK, low = SAMPLE_MIN_VAL)

        floor = sut.floorTransactions(SAMPLE_STOCK, SAMPLE_MIN_VAL)

        self.assertEqual(SAMPLE_MIN_VAL, floor[0].get_trade_val())

    def test_floor_bad_name(self):
        sut = StockTradingPlatform()

        try:
            sut.floorTransactions("UCL Bank", 200)
            self.assertFalse(True)
        except ValueError as e:
            self.assertEqual(e.args[0], "floorTransactions: Invalid Stock Name: UCL Bank")
        except:
            self.assertFalse(True)

    def test_ceiling_transactions_empty(self):
        sut = StockTradingPlatform()  #

        ceiling = sut.ceilingTransactions(SAMPLE_STOCK, SAMPLE_MIN_VAL)

        self.assertEqual(ceiling, [])

    def test_ceiling_above_max(self):
        sut, _ = test_sets.platform_gen_many_same_stock(SAMPLE_STOCK, high = SAMPLE_MAX_VAL)

        ceiling = sut.ceilingTransactions(SAMPLE_STOCK, SAMPLE_MAX_VAL + 1)

        self.assertEqual([], ceiling)

    def test_ceiling_below_min(self):
        sut, _ = test_sets.platform_gen_many_same_stock(SAMPLE_STOCK, low = SAMPLE_MIN_VAL)

        ceiling = sut.ceilingTransactions(SAMPLE_STOCK, SAMPLE_MIN_VAL - 1)

        self.assertEqual(ceiling[0].get_trade_val(), SAMPLE_MIN_VAL)

    def test_ceiling_equal_max(self):
        sut, _ = test_sets.platform_gen_many_same_stock(SAMPLE_STOCK, high = SAMPLE_MAX_VAL)

        ceiling = sut.floorTransactions(SAMPLE_STOCK, SAMPLE_MAX_VAL)

        self.assertEqual(SAMPLE_MAX_VAL, ceiling[0].get_trade_val())

    def test_ceiling_bad_name(self):
        sut = StockTradingPlatform()

        try:
            sut.ceilingTransactions("UCL Bank", SAMPLE_MAX_VAL)
            self.assertFalse(True)
        except ValueError as e:
            self.assertEqual(e.args[0], "ceilingTransactions: Invalid Stock Name: UCL Bank")
        except:
            self.assertFalse(True)

    def test_range_bad_range(self):
        sut = StockTradingPlatform()

        try:
            sut.rangeTransactions(SAMPLE_STOCK, fromValue = 101, toValue = 99)
            self.assertFalse(True)
        except ValueError as e:
            self.assertEqual(e.args[0], "rangeTransactions: Invalid Range Bounds: fromValue: 101 toValue: 99")
        except:
            self.assertFalse(True)

    def test_range_inclusive_below(self):
        sut = StockTradingPlatform()
        sut.logTransaction([SAMPLE_STOCK, 100, 2, SAMPLE_DATE])
        sut.logTransaction([SAMPLE_STOCK, 500, 3, SAMPLE_DATE])
        sut.logTransaction([SAMPLE_STOCK, 1000, 4, SAMPLE_DATE])

        range_set = sut.rangeTransactions(SAMPLE_STOCK, 200, 300)

        self.assertEqual(1, len(range_set))
        self.assertTrue(self.__trades_equal(range_set[0], Trade(*[SAMPLE_STOCK, 100, 2, SAMPLE_DATE])))

    def test_range_inclusive_above(self):
        sut = StockTradingPlatform()
        sut.logTransaction([SAMPLE_STOCK, 100, 2, SAMPLE_DATE])
        sut.logTransaction([SAMPLE_STOCK, 500, 3, SAMPLE_DATE])
        sut.logTransaction([SAMPLE_STOCK, 1000, 4, SAMPLE_DATE])

        range_set = sut.rangeTransactions(SAMPLE_STOCK, 2000, 4000)

        self.assertEqual(1, len(range_set))
        self.assertTrue(self.__trades_equal(range_set[0], Trade(*[SAMPLE_STOCK, 1000, 4, SAMPLE_DATE])))

    def test_range_equal_to_stock(self):
        sut = StockTradingPlatform()
        sut.logTransaction([SAMPLE_STOCK, 100, 2, SAMPLE_DATE])
        sut.logTransaction([SAMPLE_STOCK, 500, 3, SAMPLE_DATE])
        sut.logTransaction([SAMPLE_STOCK, 1000, 4, SAMPLE_DATE])

        range_set = sut.rangeTransactions(SAMPLE_STOCK, 1500, 1500)

        self.assertEqual(1, len(range_set))
        self.assertTrue(self.__trades_equal(range_set[0], Trade(*[SAMPLE_STOCK, 500, 3, SAMPLE_DATE])))

    def test_range_bad_name(self):
        sut = StockTradingPlatform()

        try:
            sut.rangeTransactions("UCL Bank", 200, 500)
            self.assertFalse(True)
        except ValueError as e:
            self.assertEqual(e.args[0], "rangeTransactions: Invalid Stock Name: UCL Bank")
        except:
            self.assertFalse(True)


class TestStockTradeLog(TestCase):

    def __assert_trade_lists_contain_same_elems(self, trade_list_1: t.List[Trade], trade_list_2: t.List[Trade]):
        trade_list_1 = trade_list_1.copy()
        trade_list_2 = trade_list_2.copy()

        trade_list_1.sort(key = lambda x: x.to_list()[1] * x.to_list()[2])
        trade_list_2.sort(key = lambda x: x.to_list()[1] * x.to_list()[2])

        if len(trade_list_1) != len(trade_list_2):
            self.assertTrue(False)
            return

        for i in range(len(trade_list_1)):
            if trade_list_1[i].to_list() != trade_list_2[i].to_list():
                print(trade_list_1[i].to_list(), trade_list_2[i].to_list())
                self.assertTrue(False)
                return

    def _test_trade_add(self, log: TradeTree, trade: Trade):
        log.put_trade(trade)

        self.assertEqual(log.get_trades_in_range(
            trade.get_trade_val(), trade.get_trade_val()), [trade])

    def test_add_trade_empty(self):
        log = TradeTree(SAMPLE_STOCK)
        trade = Trade(SAMPLE_STOCK, 123.4, 3, SAMPLE_DATE)

        self._test_trade_add(log, trade)
        self.assertEqual(log.get_min_trades(), [trade])
        self.assertEqual(log.get_max_trades(), [trade])

    def test_add_trade_busy(self):
        log, _ = test_sets.tree_gen_many(stock = SAMPLE_STOCK)
        trade = Trade(SAMPLE_STOCK, 123.4, 3, SAMPLE_DATE)

        self._test_trade_add(log, trade)

    def test_add_lots_trades(self):
        final_log, trades = test_sets.tree_gen_many(stock = SAMPLE_STOCK)
        test_log = TradeTree(SAMPLE_STOCK)

        for trade in trades:
            test_log.put_trade(Trade(*trade))

        self.__assert_trade_lists_contain_same_elems(test_log.get_all_trades(), final_log.get_all_trades())

    def test_bad_stock(self):
        trade = Trade("Lloyds", 23.4, 1, SAMPLE_DATE)
        log, _ = test_sets.tree_gen_many(stock = SAMPLE_STOCK)

        # Expect failure as we use a stock not used in constructor
        try:
            self._test_trade_add(log, trade)
            self.assertFalse(True)
        except ValueError as e:
            self.assertEqual(e.args[0], "Invalid Stock Name")
        except:
            self.assertFalse(True)

    def test_single_min_trade(self):
        log, _ = test_sets.tree_gen_many(stock = SAMPLE_STOCK, min_val = SAMPLE_MIN_VAL)

        self.assertEqual(log.get_min_trades()[0].get_trade_val(), SAMPLE_MIN_VAL)

    def test_many_min_trade(self):
        log, _ = test_sets.tree_gen_many(stock = SAMPLE_STOCK, min_val = SAMPLE_MIN_VAL)

        min_trade = Trade(SAMPLE_STOCK, SAMPLE_MIN_VAL, 1, SAMPLE_DATE)

        log.put_trade(min_trade)

        self.assertTrue(len(log.get_min_trades()) >= 2)
        self.assertEqual(log.get_min_trades()[0].get_trade_val(), SAMPLE_MIN_VAL)

    def test_single_max_trade(self):
        log = TradeTree(SAMPLE_STOCK)

        log.put_trade(Trade(SAMPLE_STOCK, SAMPLE_MAX_VAL, 1, SAMPLE_DATE))

        self.assertEqual(log.get_max_trades()[0].get_trade_val(), SAMPLE_MAX_VAL)

    def test_many_max_trade(self):
        log, _ = test_sets.tree_gen_many(stock = SAMPLE_STOCK, max_val = SAMPLE_MAX_VAL)

        max_trade = Trade(SAMPLE_STOCK, SAMPLE_MAX_VAL, 1, SAMPLE_DATE)

        log.put_trade(max_trade)

        self.assertTrue(len(log.get_max_trades()) >= 2)
        self.assertEqual(log.get_max_trades()[0].get_trade_val(), SAMPLE_MAX_VAL)

    def test_trade_range_all(self):
        log, trades = test_sets.tree_gen_many(stock = SAMPLE_STOCK, max_val = SAMPLE_MAX_VAL)

        trades = [Trade(*trade) for trade in trades]

        self.__assert_trade_lists_contain_same_elems(log.get_trades_in_range(0, SAMPLE_MAX_VAL), trades)

    def test_trade_range_none(self):
        log, _ = test_sets.tree_gen_many(stock = SAMPLE_STOCK, min_val = SAMPLE_MIN_VAL)

        self.assertEqual(log.get_trades_in_range(0.1, 0.2), [])

    def test_range_bad_min(self):
        log = TradeTree(SAMPLE_STOCK)

        try:
            log.get_trades_in_range(-1, 4)
            self.assertFalse(True)
        except ValueError as e:
            self.assertEqual(e.args[0], "Invalid Range")
        except:
            self.assertFalse(True)

    def test_range_bad_max(self):
        log = TradeTree(SAMPLE_STOCK)

        try:
            log.get_trades_in_range(5, 4)
            self.assertFalse(True)
        except ValueError as e:
            self.assertEqual(e.args[0], "Invalid Range")
        except:
            self.assertFalse(True)

    def test_trade_range_one(self):
        log = TradeTree(SAMPLE_STOCK)
        trade = Trade(SAMPLE_STOCK, 116, 1, SAMPLE_DATE)

        log.put_trade(trade)

        self.assertEqual(log.get_trades_in_range(116, 116), [trade])


class TestTrade(TestCase):
    def test_good_trade_constructor(self):
        # Basically just confirm no errors occur
        trade = Trade(SAMPLE_STOCK, 123.456, 5, SAMPLE_DATE)
        self.assertTrue(trade is not None)

    def test_get_trade_val_single(self):
        trade = Trade(SAMPLE_STOCK, 123, 1, SAMPLE_DATE)
        self.assertEqual(trade.get_trade_val(), 123)

    def test_get_trade_val_multi(self):
        trade = Trade(SAMPLE_STOCK, 123, 3, SAMPLE_DATE)

        self.assertEqual(trade.get_trade_val(), 369)


if __name__ == '__main__':
    platform_tests = defaultTestLoader.loadTestsFromTestCase(TestStockTradingPlatform)
    trade_tests = defaultTestLoader.loadTestsFromTestCase(TestTrade)
    tree_tests = defaultTestLoader.loadTestsFromTestCase(TestStockTradeLog)
    TextTestRunner().run(platform_tests)
    TextTestRunner().run(tree_tests)
    TextTestRunner().run(trade_tests)

from unittest import TestCase
from src.stocks.platform import StockTradingPlatform
from datetime import datetime
from gen_test_sets import TestSets
from src.stocks.trade import Trade

test_sets = TestSets()
SAMPLE_DATE = datetime.strptime('1/1/2022 1:00:00', '%d/%m/%Y %H:%M:%S')


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
            sut.logTransaction(["HSBA", 0, 1, SAMPLE_DATE])
        except ValueError as e:
            self.assertEqual("Invalid Stock Price: 0", e.args[0])
        except:
            self.assertFalse(True)

    def test_log_bad_quantity(self):
        sut = StockTradingPlatform()
        try:
            sut.logTransaction(["HSBA", 100, 0, SAMPLE_DATE])
        except ValueError as e:
            self.assertEqual("Invalid Stock Quantity: 0", e.args[0])
        except:
            self.assertFalse(True)

    def test_log_insert_first(self):
        sut = StockTradingPlatform()
        t = ["HSBA", 100, 2, SAMPLE_DATE]

        sut.logTransaction(t)

        result = sut.sortedTransactions("HSBA")

        self.assertEqual(len(result), 1)
        self.assertTrue(self.__trades_equal(result[0], Trade(*t)))

    def test_log_many_of_one(self):
        # This generates 100 trades for HSBA with a min value of 100 and a max value of 100000
        # It is guaranteed that at least one trade exists with a value of 100 and one exists with a value of 100000
        sut, test_trades = test_sets.platform_gen_many_same_stock(stock = "HSBA", low = 100, high = 100000)

        trade_list = sut.sortedTransactions("HSBA")

        # Assert right number of trades were inserted
        self.assertEqual(len(test_trades), len(trade_list))

        # Assert trade with correct minimum value was inserted
        self.assertEqual(sut.minTransactions("HSBA")[0].get_trade_val(), 100)

        # Assert trade with correct maximum value was inserted
        self.assertEqual(sut.maxTransactions("HSBA")[0].get_trade_val(), 100000)

    def test_log_one_of_each(self):
        sut = StockTradingPlatform()

        for stock in sut.STOCKS:
            sut.logTransaction(test_sets.gen_one_trade(stock, 1000, 100000))

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
        trades2 = test_sets.trade_gen_many(min_val = 1000, max_val = 100000)
        sut = StockTradingPlatform()

        for trade in trades1 + trades2:
            sut.logTransaction(trade)

        total_len = 0
        for stock in sut.STOCKS:
            total_len += len(sut.sortedTransactions(stock))

        self.assertEqual(total_len, len(trades1) + len(trades2))

    def test_sorted_transactions_empty(self):
        sut = StockTradingPlatform()

        result = sut.sortedTransactions("HSBA")

        self.assertEqual(result, [])

    def test_sorted_one(self):
        t = test_sets.gen_one_trade("HSBA", 100, 100)
        sut = StockTradingPlatform()
        sut.logTransaction(t)

        result = sut.sortedTransactions("HSBA")

        self.assertTrue(self.__trades_equal(result[0], Trade(*t)))

    def test_sorted_many(self):
        sut, trades = test_sets.platform_gen_many_same_stock("HSBA")
        trades.sort(key = lambda x: x[1] * x[2])

        sorted_trades = sut.sortedTransactions("HSBA")

        for index, trade in enumerate(trades):
            self.assertTrue(self.__trades_equal(sorted_trades[index], Trade(*trade)))

    def test_sorted_all_one_val(self):
        sut, _ = test_sets.platform_gen_many_same_val(500)

        trade_list = sut.sortedTransactions("HSBA")

        # Essentially, just make sure nothing breaks
        for trade in trade_list:
            self.assertEqual(trade.get_trade_val(), 500)

    def test_min_transactions_none(self):
        sut = StockTradingPlatform()

        min_t = sut.minTransactions("HSBA")

        self.assertEqual([], min_t)

    def test_min_transactions_all_same(self):
        sut, _ = test_sets.platform_gen_many_same_val(5000)

        min_trades = sut.minTransactions("HSBA")

        for trade in min_trades:
            self.assertEqual(trade.get_trade_val(), 5000)

    def test_min_transactions(self):
        sut, _ = test_sets.platform_gen_many_same_stock(low = 100, high = 100000, stock = "HSBA")

        min_set = sut.minTransactions("HSBA")

        self.assertEqual(100, min_set[0].get_trade_val())

    def test_min_transactions_one(self):
        sut = StockTradingPlatform()
        t = ["HSBA", 500, 2, SAMPLE_DATE]
        sut.logTransaction(t)

        min_set = sut.minTransactions("HSBA")

        self.assertEqual(len(min_set), 1)
        self.assertTrue(self.__trades_equal(min_set[0], Trade(*t)))

    def test_max_transactions_none(self):
        sut = StockTradingPlatform()

        max_t = sut.minTransactions("HSBA")

        self.assertEqual([], max_t)

    def test_max_transactions_all_same(self):
        sut, _ = test_sets.platform_gen_many_same_val(5000)

        max_trades = sut.maxTransactions("HSBA")

        for trade in max_trades:
            self.assertEqual(trade.get_trade_val(), 5000)

    def test_max_transactions(self):
        sut, _ = test_sets.platform_gen_many_same_stock(low = 100, high = 100000, stock = "HSBA")

        max_set = sut.maxTransactions("HSBA")

        self.assertEqual(100000, max_set[0].get_trade_val())

    def test_max_transactions_one(self):
        sut = StockTradingPlatform()
        t = ["HSBA", 500, 2, SAMPLE_DATE]
        sut.logTransaction(t)

        max_set = sut.minTransactions("HSBA")

        self.assertEqual(len(max_set), 1)
        self.assertTrue(self.__trades_equal(max_set[0], Trade(*t)))

    def test_floor_transactions_empty(self):
        pass

    def test_floor_below_min(self):
        pass

    def test_floor_above_max(self):
        pass

    def test_floor_equal_min(self):
        pass

    def test_floor_halfway(self):
        pass

    def test_ceiling_transactions_empty(self):
        pass

    def test_ceiling_above_max(self):
        pass

    def test_ceiling_below_min(self):
        pass

    def test_ceiling_equal_max(self):
        pass

    def test_ceiling_halfway(self):
        pass

    def test_range_bad_range(self):
        pass

    def test_range_zero_range_not_equal(self):
        pass

    def test_range_zero_equal_to_stock(self):
        pass

    def test_range_below_min(self):
        pass

    def test_range_above_max(self):
        pass

    def test_range_bad_name(self):
        pass

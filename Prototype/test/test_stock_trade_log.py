from sys import maxsize
from unittest import TestCase
from stocks.trade_tree import TradeTree
from stocks.trade import Trade
from random import Random
from datetime import datetime

SAMPLE_DATE = datetime.strptime("2021-01-01T13:47:00", "%Y-%m-%dT%H:%M:%S")
LOW_TRADE = Trade("Barclays", 5, 3, SAMPLE_DATE)
HIGH_TRADE = Trade("Barclays", 12341234, 34, SAMPLE_DATE)
STOCK = "Barclays"
STOCK_LIST = [Trade(STOCK, 47, 5, SAMPLE_DATE),
              Trade(STOCK, 116, 1, SAMPLE_DATE),
              Trade(STOCK, 333, 3, SAMPLE_DATE)]

FULL_LIST = [LOW_TRADE,
             Trade(STOCK, 47, 5, SAMPLE_DATE),
             Trade(STOCK, 116, 1, SAMPLE_DATE),
             Trade(STOCK, 333, 3, SAMPLE_DATE),
             HIGH_TRADE]


def busy_constructor() -> TradeTree:
    log = TradeTree(STOCK)
    log.put_trade(LOW_TRADE)
    log.put_trade(HIGH_TRADE)

    for stock in STOCK_LIST:
        log.put_trade(stock)

    return log


class TestStockTradeLog(TestCase):

    def __assert_trade_lists_are_equal(self, trade_list_1: list[Trade], trade_list_2: list[Trade]):
        trade_list_1 = trade_list_1.copy()
        trade_list_2 = trade_list_2.copy()

        trade_list_1.sort(key=lambda x: x.to_list()[1] * x.to_list()[2])
        trade_list_2.sort(key=lambda x: x.to_list()[1] * x.to_list()[2])

        if len(trade_list_1) != len(trade_list_2):
            self.assertTrue(False)
            return

        for i in range(len(trade_list_1)):
            if trade_list_1[i].to_list() != trade_list_2[i].to_list():
                print(trade_list_1[i].to_list(), trade_list_2[i].to_list())
                self.assertTrue(False)
                return

    def _check_constructed(self, log: TradeTree):
        self.assertEqual(log.get_min_trades(), [LOW_TRADE])
        self.assertEqual(log.get_max_trades(), [HIGH_TRADE])

    def _test_trade_add(self, log: TradeTree, t: Trade):
        log.put_trade(t)

        self.assertEqual(log.get_trades_in_range(
            t.get_trade_val(), t.get_trade_val()), [t])

    def test_add_trade_empty(self):
        log = TradeTree(STOCK)
        t = Trade("Barclays", 123.4, 3, SAMPLE_DATE)

        self._test_trade_add(log, t)
        self.assertEqual(log.get_min_trades(), [t])
        self.assertEqual(log.get_max_trades(), [t])

    def test_add_trade_busy(self):
        log = busy_constructor()
        t = Trade("Barclays", 123.4, 3, SAMPLE_DATE)

        self._test_trade_add(log, t)
        self._check_constructed(log)

    def test_add_lots_trades(self):
        r = Random()
        log = busy_constructor()

        for _ in range(100):
            t = Trade("Barclays", r.random() * 100 + 50, r.randint(2, 10), SAMPLE_DATE)

            self._test_trade_add(log, t)
            self._check_constructed(log)

    def test_bad_stock(self):
        t = Trade("Lloyds", 23.4, 1, SAMPLE_DATE)
        log = busy_constructor()

        try:
            self._test_trade_add(log, t)
            self.assertFalse(True)
        except ValueError as e:
            self.assertEqual(e.args[0], "Invalid Stock Name")
        except:
            self.assertFalse(True)

    def test_single_min_trade(self):
        log = busy_constructor()

        self.assertEqual(log.get_min_trades(), [LOW_TRADE])

    def test_many_min_trade(self):
        log = busy_constructor()

        log.put_trade(LOW_TRADE)

        self.assertEqual(log.get_min_trades(), [LOW_TRADE, LOW_TRADE])

    def test_single_max_trade(self):
        log = busy_constructor()

        self.assertEqual(log.get_max_trades(), [HIGH_TRADE])

    def test_many_max_trade(self):
        log = busy_constructor()

        log.put_trade(HIGH_TRADE)

        self.assertEqual(log.get_max_trades(), [HIGH_TRADE, HIGH_TRADE])

    def test_trade_range_all(self):
        log = busy_constructor()

        self.__assert_trade_lists_are_equal(log.get_trades_in_range(0, maxsize), FULL_LIST)

    def test_trade_range_none(self):
        log = busy_constructor()

        self.assertEqual(log.get_trades_in_range(0.1, 0.2), [])

    def test_trade_range(self):
        log = busy_constructor()

        self.__assert_trade_lists_are_equal(log.get_trades_in_range(100, 1000), STOCK_LIST)

    def test_range_bad_min(self):
        log = busy_constructor()

        try:
            log.get_trades_in_range(-1, 4)
            self.assertFalse(True)
        except ValueError as e:
            self.assertEqual(e.args[0]
                             , "Invalid Range")
        except:
            self.assertFalse(True)

    def test_range_bad_max(self):
        log = busy_constructor()

        try:
            log.get_trades_in_range(5, 4)
            self.assertFalse(True)
        except ValueError as e:
            self.assertEqual(e.args[0]
                             , "Invalid Range")
        except:
            self.assertFalse(True)

    def test_trade_range_one(self):
        log = busy_constructor()

        self.assertEqual(log.get_trades_in_range(116, 116), [STOCK_LIST[1]])

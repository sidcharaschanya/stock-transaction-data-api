from sys import maxsize
from unittest import TestCase
from src.stocks.trade_tree import TradeTree
from src.stocks.trade import Trade
from random import Random

LOW_TRADE = Trade("Barclays", 5, 3, "2021-01-01T13:47:00.00")
HIGH_TRADE = Trade("Barclays", 12341234, 34, "2022-03-01T17:28:29.00")
STOCK = "Barclays"
STOCK_LIST = [Trade(STOCK, 47, 5, "2021-01-01T11:21:00.00"),
              Trade(STOCK, 116, 1, "2021-01-01T11:21:00.00"),
              Trade(STOCK, 333, 3, "2021-01-01T11:21:00.00")]

FULL_LIST = [LOW_TRADE,
             Trade(STOCK, 47, 5, "2021-01-01T11:21:00.00"),
             Trade(STOCK, 116, 1, "2021-01-01T11:21:00.00"),
             Trade(STOCK, 333, 3, "2021-01-01T11:21:00.00"),
             HIGH_TRADE]


def __construct_helper(t, log):
    STOCK_LIST.append(t)
    log.add_trade(t)


def busy_constructor() -> TradeTree:
    log = TradeTree(STOCK)
    log.add_trade(LOW_TRADE)
    log.add_trade(HIGH_TRADE)

    for stock in STOCK_LIST:
        log.add_trade(stock)

    return log


class TestStockTradeLog(TestCase):

    def _check_constructed(self, log: TradeTree):
        self.assertEqual(log.get_min_trade(), [LOW_TRADE])
        self.assertEqual(log.get_max_trade(), [HIGH_TRADE])

    def _test_trade_add(self, log: TradeTree, t: Trade):
        log.add_trade(t)

        self.assertEqual(log.get_trade_in_range(
            t.get_trade_val(), t.get_trade_val()), [t])

    def test_add_trade_empty(self):
        log = TradeTree(STOCK)
        t = Trade("Barclays", 123.4, 3, "2022-02-22T17:28:04.00")

        self._test_trade_add(log, t)
        self.assertEqual(log.get_min_trade(), [t])
        self.assertEqual(log.get_max_trade(), [t])

    def test_add_trade_busy(self):
        log = busy_constructor()
        t = Trade("Barclays", 123.4, 3, "2022-02-22T17:28:04.00")

        self._test_trade_add(log, t)
        self._check_constructed(log)

    def test_add_lots_trades(self):
        r = Random()
        log = busy_constructor()

        for _ in range(100):
            t = Trade("Barclays", r.random() * 100 + 50, r.randint(2, 10), "2021-06-13T05:37:00.00")

            self._test_trade_add(log, t)
            self._check_constructed(log)

    def test_bad_stock(self):
        t = Trade("Lloyds", 23.4, 1, "2021-01-01T00:00:01.01")
        log = busy_constructor()

        try:
            self._test_trade_add(log, t)
            self.assertFalse(True)
        except ValueError as e:
            self.assertEqual(e.args[0], "ERROR: Stock name is not consistent")
        except:
            self.assertFalse(True)

    def test_single_min_trade(self):
        log = busy_constructor()

        self.assertEqual(log.get_min_trade(), [LOW_TRADE])

    def test_many_min_trade(self):
        log = busy_constructor()

        log.add_trade(LOW_TRADE)

        self.assertEqual(log.get_min_trade(), [LOW_TRADE, LOW_TRADE])

    def test_single_max_trade(self):
        log = busy_constructor()

        self.assertEqual(log.get_max_trade(), [HIGH_TRADE])

    def test_many_max_trade(self):
        log = busy_constructor()

        log.add_trade(HIGH_TRADE)

        self.assertEqual(log.get_max_trade(), [HIGH_TRADE, HIGH_TRADE])

    def test_trade_range_all(self):
        log = busy_constructor()

        self.assertEqual(log.get_trade_in_range(0, maxsize)
                         , FULL_LIST)

    def test_trade_range_none(self):
        log = busy_constructor()

        self.assertEqual(log.get_trade_in_range(0.1, 0.2), [])

    def test_trade_range(self):
        log = busy_constructor()

        self.assertEqual(log.get_trade_in_range(100, 1000), STOCK_LIST)

    def test_range_bad_min(self):
        log = busy_constructor()

        try:
            log.get_trade_in_range(-1, 4)
            self.assertFalse(True)
        except ValueError as e:
            self.assertEqual(e.args[0]
                             , "ERROR, lower bound must be at least zero")
        except:
            self.assertFalse(True)

    def test_range_bad_max(self):
        log = busy_constructor()

        try:
            log.get_trade_in_range(5, 4)
            self.assertFalse(True)
        except ValueError as e:
            self.assertEqual(e.args[0]
                             , "ERROR, upper bound must be greater than or equal to the lower bound")
        except:
            self.assertFalse(True)

    def test_trade_range_one(self):
        log = busy_constructor()

        self.assertEqual(log.get_trade_in_range(116, 116), [STOCK_LIST[1]])

from unittest import TestCase
from src.Stocks import Trade


class TestTrade(TestCase):
    def test_good_trade_constructor(self):
        t = Trade("Barclays", 123.456, 5, "2022-02-22T17:28:00.00")
        self.assertTrue()

    def test_bad_stock_name(self):
        try:
            t = Trade("asdf", 123.456, 5, "2022-02-22T17:28:00.00")
            self.assertFalse()
        except ValueError as e:
            self.assertEqual(e.args[0], "ERROR: Stock name not recognised")
        except:
            self.assertFalse()

    def test_bad_stock_value(self):
        try:
            t = Trade("Barclays", -1, 5, "2022-02-22T17:28:00.00")
            self.assertFalse()
        except ValueError as e:
            self.assertEqual(e.args[0], "ERROR: Stock value cannot be negative")
        except:
            self.assertFalse()

    def test_bad_stock_qnty(self):
        try:
            t = Trade("Barclays", 123, 0, "2022-02-22T17:28:00.00")
            self.assertFalse()
        except ValueError as e:
            self.assertEqual(e.args[0], "ERROR: Must buy at least one stock")
        except:
            self.assertFalse()

    def test_get_trade_val_single(self):
        t = Trade("Barclays", 123, 1, "2022-02-22T17:28:00.00")
        self.assertEqual(t.get_trade_val(), 123)

    def test_get_trade_val_multi(self):
        t = Trade("Barclays", 123, 3, "2022-02-22T17:28:00.00")

        self.assertEqual(t.get_trade_val(), 246)

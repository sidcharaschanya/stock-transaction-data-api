from unittest import TestCase
from stocks.trade import Trade
from datetime import datetime


class TestTrade(TestCase):
    def test_good_trade_constructor(self):
        t = Trade("Barclays", 123.456, 5, datetime.strptime("2022-02-22T17:28:00", '%Y-%m-%dT%H:%M:%S'))

    def test_good_val(self):
        t = Trade("Barclays", 123.456, 5, datetime.strptime("2022-02-22T17:28:00", '%Y-%m-%dT%H:%M:%S'))

        self.assertEqual(123.456*5, t.get_trade_val())

    def test_good_to_list(self):
        t = Trade("Barclays", 123.456, 5, datetime.strptime("2022-02-22T17:28:00", '%Y-%m-%dT%H:%M:%S'))

        self.assertEqual(t.to_list(), ["Barclays", 123.456, 5, datetime.strptime("2022-02-22T17:28:00", '%Y-%m-%dT%H:%M:%S')])

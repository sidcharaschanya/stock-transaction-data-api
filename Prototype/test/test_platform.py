from unittest import TestCase
from platform import StockTradingPlatform
from datetime import datetime
from trade import Trade

SAMPLE_DATE = datetime.strptime('1/1/2022 1:00:00', '%d/%m/%Y %H:%M:%S')


class TestStockTradingPlatform(TestCase):

    def test_log_bad_stock(self):
        sut = StockTradingPlatform()
        try:
            sut.log_transaction(Trade("UCL Bank", 1, 1, SAMPLE_DATE))
            self.assertFalse(True)
        except ValueError as e:
            self.assertEqual(e.args[0], "Bad trade information")
        except:
            self.assertFalse(True)

    def test_log_bad_stock_value(self):
        sut = StockTradingPlatform()
        try:
            sut.log_transaction(Trade("HSBC", 0, 1, SAMPLE_DATE))
        except ValueError as e:
            self.assertEqual("Bad trade information", e.args[0])
        except:
            self.assertFalse(True)

    def test_log_bad_quantity(self):
        sut = StockTradingPlatform()
        try:
            sut.log_transaction(Trade("HSBC", 100, 0, SAMPLE_DATE))
        except ValueError as e:
            self.assertEqual("Bad trade information", e.args[0])
        except:
            self.assertFalse(True)

    def test_log_insert_first(self):
        sut = StockTradingPlatform()
        t = Trade("HSBA", 100, 2, SAMPLE_DATE)

        sut.log_transaction(t)

        result = sut.sorted_transactions("HSBA")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], t)

    def test_log_many_of_one(self):
        pass

    def test_log_one_of_each(self):
        pass

    def test_log(self):
        pass

    def test_log_all_same_trade_val(self):
        pass

    def test_log_some_conflicts(self):
        pass

    def test_sorted_transactions_empty(self):
        pass

    def test_sorted_one(self):
        pass

    def test_sorted_many(self):
        pass

    def test_sorted_all_one_val(self):
        pass

    def test_sorted(self):
        pass

    def test_min_transactions_none(self):
        pass

    def test_min_transactions_all_same(self):
        pass

    def test_min_transactions(self):
        pass

    def test_min_transactions_one(self):
        pass

    def test_min_bad_name(self):
        pass

    def test_max_transactions_none(self):
        pass

    def test_max_transactions_all_same(self):
        pass

    def test_max_transactions(self):
        pass

    def test_max_transactions_one(self):
        pass

    def test_max_bad_name(self):
        pass

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

    def test_floor_bad_name(self):
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

    def test_ceiling_bad_name(self):
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

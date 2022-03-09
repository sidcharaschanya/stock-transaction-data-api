class TestStockTradingPlatform(TestCase):

    def test_log_bad_stock(self):

        assert False
        assert a == b

        sut = StockTradingPlatform()
        try:
            sut.log_transaction(["UCL Bank", 1, 1, SAMPLE_DATE])
            self.assertFalse(True)
        except ValueError as e:
            self.assertEqual(e.args[0], "Bad Name UCL Bank")
        except:
            self.assertFalse(True)

    def test_log_bad_stock_value(self):
        sut = StockTradingPlatform()
        try:
            sut.log_transaction(Trade("HSBA", 0, 1, SAMPLE_DATE))
        except ValueError as e:
            self.assertEqual("Bad Price 0", e.args[0])
        except:
            self.assertFalse(True)

    def test_log_bad_quantity(self):
        sut = StockTradingPlatform()
        try:
            sut.log_transaction(Trade("HSBA", 100, 0, SAMPLE_DATE))
        except ValueError as e:
            self.assertEqual("Bad quantity 0", e.args[0])
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
        # This generates 100 trades for HSBA with a min value of 100 and a max value of 100000
        # It is guaranteed that at least one trade exists with a value of 100 and one exists with a value of 100000
        test_trades = test_sets.trade_gen_many_same_stock(stock = "HSBA", min_val = 100, max_val = 100000)

        sut = StockTradingPlatform()

        for trade in test_trades:
            sut.log_transaction(trade)

        trade_list = sut.sorted_transactions("HSBA")

        # Assert right number of trades were inserted
        self.assertEqual(len(test_trades), len(trade_list))

        # Assert trade with correct minimum value was inserted
        self.assertEqual(sut.min_transactions("HSBA")[0].get_trade_val(), 100)

        # Assert trade with correct maximum value was inserted
        self.assertEqual(sut.max_transactions("HSBA")[0].get_trade_val(), 100000)

    def test_log_one_of_each(self):
        sut = StockTradingPlatform()

        for stock in sut.STOCKS:
            sut.log_transaction(test_sets.gen_one_trade(stock, 1000, 100000))

        for stock in sut.STOCKS:
            self.assertEqual(len(sut.sorted_transactions(stock)), 1)

    def test_log(self):
        sut = StockTradingPlatform()

        sut.log_transaction(Trade("London Stock Exchange Group",
                                  1000, 5,
                                  datetime.strptime("2020-02-25T22:00:15", "%Y-%m-%dT%H:%M:%S")))

        self.assertTrue(True)

    def test_log_all_same_trade_val(self):
        trades = test_sets.trade_gen_many_same_value(250)
        sut = StockTradingPlatform()

        for trade in trades:
            sut.log_transaction(trade)

        for stock in sut.STOCKS:
            self.assertEqual(sut.min_transactions(stock), sut.max_transactions(stock))

    def test_log_some_conflicts(self):
        trades1 = test_sets.trade_gen_many_same_value(550)
        trades2 = test_sets.trade_gen_many(min_val = 1000, max_val = 100000)
        sut = StockTradingPlatform()

        for trade in trades1 + trades2:
            sut.log_transaction(trade)

        total_len = 0
        for stock in sut.STOCKS:
            total_len += len(sut.sorted_transactions(stock))

        self.assertEqual(total_len, len(trades1) + len(trades2))

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


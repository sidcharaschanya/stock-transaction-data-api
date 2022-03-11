from src.exp.transaction_data_generator import TransactionDataGenerator
from src.stocks.platform import StockTradingPlatform
import datetime as d
import enum as e
import random as r
import timeit
import typing as t


class Case(e.Enum):
    LOG_RANDOM = e.auto()
    LOG_SORTED = e.auto()
    SORTED = e.auto()
    MIN = e.auto()
    MAX = e.auto()
    FLOOR_RANDOM = e.auto()
    FLOOR_EXISTING = e.auto()
    CEILING_RANDOM = e.auto()
    CEILING_EXISTING = e.auto()
    RANGE_RANDOM = e.auto()
    RANGE_ALL = e.auto()


class ExperimentalFramework:
    def __init__(self, n_transactions: int, n_step: int, n_trials: int) -> None:
        self.__n_transactions = n_transactions
        self.__n_step = n_step
        self.__n_trials = n_trials
        self.__generator = TransactionDataGenerator()
        self.__times = {case: {i: [] for i in self.get_n_transactions_list()} for case in Case}
        r.seed(d.datetime.now())

    @staticmethod
    def __trade_value(transaction: list) -> float:
        return transaction[1] * transaction[2]

    def __gen_stock_name(self) -> str:
        return r.choice(self.__generator.stockNames)

    def __gen_trade_value(self) -> float:
        return round(r.uniform(self.__generator.minTradeValue, self.__generator.maxTradeValue), 2)

    def __gen_transactions_same_stock(self, case: Case) -> t.Tuple[t.List[list], str]:
        transactions = self.__generator.generateTransactionData(self.__n_transactions)

        if case == Case.LOG_SORTED:
            transactions.sort(key = ExperimentalFramework.__trade_value, reverse = True)

        stock_name = self.__gen_stock_name()

        for i in range(len(transactions)):
            transactions[i][0] = stock_name

        return transactions, stock_name

    def __test_ordered_op(self, n_curr: int, func: callable, case: Case, args: list) -> list:
        start = timeit.default_timer()
        trade = func(*args)
        end = timeit.default_timer()
        self.__times[case][n_curr].append(end - start)
        return trade

    def __test_all_ordered_ops(self, n_curr: int, platform: StockTradingPlatform, stock_name: str) -> None:
        sorted_trades = self.__test_ordered_op(n_curr, platform.sortedTransactions, Case.SORTED, [
            stock_name
        ])

        self.__test_ordered_op(n_curr, platform.minTransactions, Case.MIN, [
            stock_name
        ])

        self.__test_ordered_op(n_curr, platform.maxTransactions, Case.MAX, [
            stock_name
        ])

        self.__test_ordered_op(n_curr, platform.floorTransactions, Case.FLOOR_RANDOM, [
            stock_name, self.__gen_trade_value()
        ])

        self.__test_ordered_op(n_curr, platform.floorTransactions, Case.FLOOR_EXISTING, [
            stock_name, r.choice(sorted_trades).get_trade_val()
        ])

        self.__test_ordered_op(n_curr, platform.ceilingTransactions, Case.CEILING_RANDOM, [
            stock_name, self.__gen_trade_value()
        ])

        self.__test_ordered_op(n_curr, platform.ceilingTransactions, Case.CEILING_EXISTING, [
            stock_name, r.choice(sorted_trades).get_trade_val()
        ])

        range_random_args = [stock_name]
        range_random_args.extend(sorted([self.__gen_trade_value(), self.__gen_trade_value()]))
        self.__test_ordered_op(n_curr, platform.rangeTransactions, Case.RANGE_RANDOM, range_random_args)

        range_all_args = [stock_name]
        range_all_args.extend(sorted([self.__generator.minTradeValue, self.__generator.maxTradeValue]))
        self.__test_ordered_op(n_curr, platform.rangeTransactions, Case.RANGE_ALL, range_all_args)

    def __test_log(self, case: Case) -> None:
        for _ in range(self.__n_trials):
            platform = StockTradingPlatform()
            transactions, stock_name = self.__gen_transactions_same_stock(case)

            for i, transaction in enumerate(transactions):
                start = timeit.default_timer()
                platform.logTransaction(transaction)
                end = timeit.default_timer()
                n_curr = i + 1

                if n_curr % self.__n_step == 0:
                    self.__times[case][n_curr].append(end - start)

                    if case == Case.LOG_RANDOM:
                        self.__test_all_ordered_ops(n_curr, platform, stock_name)

    def __output_times(self):
        [print(f"{case.name} = {self.__times[case]}") for case in Case]

    def run_tests(self) -> None:
        self.__test_log(Case.LOG_RANDOM)
        self.__test_log(Case.LOG_SORTED)
        self.__output_times()

    def get_n_transactions_list(self) -> list:
        return list(range(self.__n_step, self.__n_transactions + 1, self.__n_step))

    def get_times(self, case: Case) -> list:
        times = self.__times[case].values()
        return [sum(time) / len(time) for time in times]
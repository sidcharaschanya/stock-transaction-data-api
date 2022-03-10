from src.exp.transaction_data_generator import TransactionDataGenerator
from src.stocks.platform import StockTradingPlatform
import datetime as d
import enum as e
import matplotlib.pyplot as plt
import random as r
import timeit
import typing as t


class Cases(e.Enum):
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
        self.__times = {case: {i: [] for i in self.get_n_transactions_list()} for case in Cases}

    @staticmethod
    def __trade_value(transaction: list) -> float:
        return transaction[1] * transaction[2]

    def __gen_stock_name(self) -> str:
        r.seed(d.datetime.now())
        return r.choice(self.__generator.stockNames)

    def __gen_trade_value(self) -> float:
        r.seed(d.datetime.now())
        return round(r.uniform(self.__generator.minTradeValue, self.__generator.maxTradeValue), 2)

    def __gen_transactions_same_stock(self, case: Cases) -> t.Tuple[t.List[list], str]:
        transactions = self.__generator.generateTransactionData(self.__n_transactions)

        if case == Cases.LOG_SORTED:
            transactions.sort(key = ExperimentalFramework.__trade_value, reverse = True)

        stock_name = self.__gen_stock_name()

        for i in range(len(transactions)):
            transactions[i][0] = stock_name

        return transactions, stock_name

    def __test_ordered_op(self, n_curr: int, func: callable, case: Cases, args: list) -> None:
        start = timeit.default_timer()
        func(*args)
        end = timeit.default_timer()
        self.__times[case][n_curr].append(end - start)

    def __test_all_ordered_ops(self, n_curr: int, platform: StockTradingPlatform, stock_name: str) -> None:
        self.__test_ordered_op(n_curr, platform.sortedTransactions, Cases.SORTED, [stock_name])
        self.__test_ordered_op(n_curr, platform.minTransactions, Cases.MIN, [stock_name])
        self.__test_ordered_op(n_curr, platform.maxTransactions, Cases.MAX, [stock_name])

    def __test_log(self, case: Cases) -> None:
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

                    if case == Cases.LOG_RANDOM:
                        self.__test_all_ordered_ops(n_curr, platform, stock_name)

    def run_tests(self) -> None:
        self.__test_log(Cases.LOG_RANDOM)
        self.__test_log(Cases.LOG_SORTED)

    def get_n_transactions_list(self) -> list:
        return list(range(self.__n_step, self.__n_transactions + 1, self.__n_step))

    def get_times(self, case: Cases) -> list:
        times = self.__times[case].values()
        return [sum(time) / len(time) for time in times]


ef = ExperimentalFramework(10000, 50, 2)
ef.run_tests()
plt.plot(ef.get_n_transactions_list(), ef.get_times(Cases.MIN), ".")
plt.ylim([0.0000005, 0.0000015])
plt.show()

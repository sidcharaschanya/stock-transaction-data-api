from src.exp.transaction_data_generator import TransactionDataGenerator
from src.stocks.platform import StockTradingPlatform
import random
import timeit


class ExperimentalFramework:
    LOG_RANDOM = 0
    LOG_SORTED = 1
    SORTED = 2
    MIN = 3
    MAX = 4
    FLOOR_RANDOM = 5
    FLOOR_EXISTING = 6
    CEILING_RANDOM = 7
    CEILING_EXISTING = 8
    RANGE_RANDOM = 9
    RANGE_ALL = 10

    def __init__(self, n_transactions: int, n_step: int, n_trials: int) -> None:
        self.__n_transactions = n_transactions
        self.__n_step = n_step
        self.__n_trials = n_trials
        self.__generator = TransactionDataGenerator()
        self.__times = {case: {i: [] for i in self.get_n_transactions_list()} for case in range(11)}

    @staticmethod
    def __trade_value(transaction: list) -> float:
        return transaction[1] * transaction[2]

    def __gen_transactions_same_stock(self, case: int) -> list:
        transactions = self.__generator.generateTransactionData(self.__n_transactions)

        if case == ExperimentalFramework.LOG_SORTED:
            transactions.sort(key = ExperimentalFramework.__trade_value, reverse = True)

        stock_name = self.__generator.getStockName()

        for i in range(len(transactions)):
            transactions[i][0] = stock_name

        return transactions

    def __test_ordered_op(self, n_curr: int, func: callable, case: int, args: list) -> list:
        start = timeit.default_timer()
        trades = func(*args)
        end = timeit.default_timer()
        self.__times[case][n_curr].append(end - start)
        return trades

    def __test_all_ordered_ops(self, n_curr: int, platform: StockTradingPlatform, stock_name: str) -> None:
        sorted_trades = self.__test_ordered_op(n_curr, platform.sortedTransactions, ExperimentalFramework.SORTED, [
            stock_name
        ])

        self.__test_ordered_op(n_curr, platform.minTransactions, ExperimentalFramework.MIN, [
            stock_name
        ])

        self.__test_ordered_op(n_curr, platform.maxTransactions, ExperimentalFramework.MAX, [
            stock_name
        ])

        self.__test_ordered_op(n_curr, platform.floorTransactions, ExperimentalFramework.FLOOR_RANDOM, [
            stock_name, self.__generator.getTradeValue()
        ])

        self.__test_ordered_op(n_curr, platform.floorTransactions, ExperimentalFramework.FLOOR_EXISTING, [
            stock_name, random.choice(sorted_trades).get_trade_val()
        ])

        self.__test_ordered_op(n_curr, platform.ceilingTransactions, ExperimentalFramework.CEILING_RANDOM, [
            stock_name, self.__generator.getTradeValue()
        ])

        self.__test_ordered_op(n_curr, platform.ceilingTransactions, ExperimentalFramework.CEILING_EXISTING, [
            stock_name, random.choice(sorted_trades).get_trade_val()
        ])

        range_random_args = [stock_name]
        range_random_args.extend(sorted([self.__generator.getTradeValue(), self.__generator.getTradeValue()]))
        self.__test_ordered_op(
            n_curr, platform.rangeTransactions, ExperimentalFramework.RANGE_RANDOM, range_random_args
        )

        range_all_args = [stock_name]
        range_all_args.extend(sorted([self.__generator.minTradeValue, self.__generator.maxTradeValue]))
        self.__test_ordered_op(
            n_curr, platform.rangeTransactions, ExperimentalFramework.RANGE_ALL, range_all_args
        )

    def __test_log(self, case: int) -> None:
        for _ in range(self.__n_trials):
            transactions = self.__gen_transactions_same_stock(case)
            platform = StockTradingPlatform()

            for i, transaction in enumerate(transactions):
                start = timeit.default_timer()
                platform.logTransaction(transaction)
                end = timeit.default_timer()

                if (i + 1) % self.__n_step == 0:
                    self.__times[case][i + 1].append(end - start)

                    if case == ExperimentalFramework.LOG_RANDOM:
                        self.__test_all_ordered_ops(i + 1, platform, transaction[0])

    def __output_times(self) -> None:
        print("CASE #i = {num_trades_1: [trial_1, ..., trial_n], ..., num_trades_n: [trial_1, ..., trial_n]}\n")
        [print(f"CASE #{case} = {self.__times[case]}\n") for case in range(11)]

    def run_tests(self) -> None:
        self.__test_log(ExperimentalFramework.LOG_RANDOM)
        self.__test_log(ExperimentalFramework.LOG_SORTED)
        self.__output_times()

    def get_n_transactions_list(self) -> list:
        return list(range(self.__n_step, self.__n_transactions + 1, self.__n_step))

    def get_times(self, case: int) -> list:
        return [sum(time) / self.__n_trials for time in self.__times[case].values()]


if __name__ == '__main__':
    ef = ExperimentalFramework(10000, 100, 20)
    ef.run_tests()

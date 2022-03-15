from src.exp.transaction_data_generator import TransactionDataGenerator
from src.stocks.platform import StockTradingPlatform
import random
import timeit


# This class manages the process of creating and testing instances of the StockTradingPlatform class
class ExperimentalFramework:
    # Constants that represent different cases to be examined
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

    # Parameterized with the maximum number of transactions to be logged, the step size, and the number of trials
    def __init__(self, n_transactions: int, n_step: int, n_trials: int) -> None:
        self.__n_transactions = n_transactions
        self.__n_step = n_step
        self.__n_trials = n_trials
        self.__generator = TransactionDataGenerator()
        self.__times = {case: {i: [] for i in self.get_n_transactions_list()} for case in range(11)}

    @staticmethod
    def __trade_value(transaction: list) -> float:
        return transaction[1] * transaction[2]

    # Generates random transactions and reassigns the stock names to be uniform
    def __gen_transactions_same_stock(self, case: int) -> list:
        transactions = self.__generator.generateTransactionData(self.__n_transactions)
        stock_name = self.__generator.getStockName()

        # Assign a particular randomly chosen stock name to each transaction
        for i in range(len(transactions)):
            transactions[i][0] = stock_name

        # Sort the generated transactions by trade value in the appropriate case
        if case == ExperimentalFramework.LOG_SORTED:
            transactions.sort(key = ExperimentalFramework.__trade_value, reverse = True)

        return transactions

    # Tests the execution time of a general API operation func with arguments *args
    def __test_ordered_op(self, n_curr: int, func: callable, case: int, args: list) -> list:
        start = timeit.default_timer()
        trades = func(*args)
        end = timeit.default_timer()
        self.__times[case][n_curr].append(end - start)
        return trades

    # A sequence of calls to __test_ordered_op() that examine the performance of all ordered API operations
    def __test_all_ordered_ops(self, n_curr: int, platform: StockTradingPlatform, stock_name: str) -> None:
        # Testing the sorted transactions operation
        sorted_trades = self.__test_ordered_op(n_curr, platform.sortedTransactions, ExperimentalFramework.SORTED, [
            stock_name
        ])

        # Testing the min transactions operation
        self.__test_ordered_op(n_curr, platform.minTransactions, ExperimentalFramework.MIN, [
            stock_name
        ])

        # Testing the max transactions operation
        self.__test_ordered_op(n_curr, platform.maxTransactions, ExperimentalFramework.MAX, [
            stock_name
        ])

        # Testing the floor transactions operation
        self.__test_ordered_op(n_curr, platform.floorTransactions, ExperimentalFramework.FLOOR_RANDOM, [
            stock_name, self.__generator.getTradeValue()
        ])
        self.__test_ordered_op(n_curr, platform.floorTransactions, ExperimentalFramework.FLOOR_EXISTING, [
            stock_name, random.choice(sorted_trades).get_trade_val()
        ])

        # Testing the ceiling transactions operation
        self.__test_ordered_op(n_curr, platform.ceilingTransactions, ExperimentalFramework.CEILING_RANDOM, [
            stock_name, self.__generator.getTradeValue()
        ])
        self.__test_ordered_op(n_curr, platform.ceilingTransactions, ExperimentalFramework.CEILING_EXISTING, [
            stock_name, random.choice(sorted_trades).get_trade_val()
        ])

        # Testing the range transactions operation
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

    # Driver method that handles the logging of transactions and when to record execution times
    def __test_log(self, case: int) -> None:
        # Loop for the number of trials
        for _ in range(self.__n_trials):
            transactions = self.__gen_transactions_same_stock(case)
            platform = StockTradingPlatform()

            # Iterate through generated transactions with a particular randomly chosen stock name
            for i, transaction in enumerate(transactions):
                start = timeit.default_timer()
                platform.logTransaction(transaction)
                end = timeit.default_timer()

                # For desired multiples of step size
                if (i + 1) % self.__n_step == 0:
                    # Record log time
                    self.__times[case][i + 1].append(end - start)

                    # Examine performance of ordered API operations
                    if case == ExperimentalFramework.LOG_RANDOM:
                        self.__test_all_ordered_ops(i + 1, platform, transaction[0])

    # Calls the driver method __test_log() twice to perform all the required tests
    def run_tests(self) -> None:
        self.__test_log(ExperimentalFramework.LOG_RANDOM)
        self.__test_log(ExperimentalFramework.LOG_SORTED)

    # Displays the recorded execution times for each examined case
    def output_times(self) -> None:
        print("CASE #i = {num_trades_1: [trial_1, ..., trial_n], ..., num_trades_n: [trial_1, ..., trial_n]}\n")
        [print(f"CASE #{case} = {self.__times[case]}\n") for case in range(11)]

    # Returns a list of all multiples of step size less than or equal to the maximum number of transactions
    def get_n_transactions_list(self) -> list:
        return list(range(self.__n_step, self.__n_transactions + 1, self.__n_step))

    # Returns the execution times for a specified case
    def get_times(self, case: int) -> list:
        return [sum(time) / self.__n_trials for time in self.__times[case].values()]


if __name__ == '__main__':
    ef = ExperimentalFramework(10000, 100, 20)
    ef.run_tests()
    ef.output_times()

from src.stocks.platform import StockTradingPlatform
from src.exp.transaction_data_generator import TransactionDataGenerator
import matplotlib.pyplot as plt
import numpy as np
import timeit

stp = StockTradingPlatform()
tdg = TransactionDataGenerator()

insertions = []
times = []


# EXAMPLE : Test 1 for logTransactions: execution time when the transactions logged are in random order.
def log_transactions_test_1(num):

    startTime = timeit.default_timer()
    for i in range(num):
        stp.logTransaction(tdg.generateTransactionData(1))
    endTime = timeit.default_timer()

    time_taken = endTime - startTime
    # adding data for the graph
    insertions.append(num)
    times.append(time_taken)
    return time_taken

def test_graph():
    # y = np.array(times)
    # x = np.array(insertions)

    # example data
    y = np.array([1, 2])
    x = np.array([1, 2])
    # plt.xscale("log")

    plt.plot(x, y, '-', color='red')

    plt.ylabel('Average log time')
    plt.xlabel('Number of insertions')

    # setting y-axis range
    plt.ylim([0.5, 1.5])
    plt.show()


test_graph()

def plotLogTransactions(x, times):
    y = []
    numOfTransactions = len(x)
    for i in range(numOfTransactions):
        y.append(times[i][1])
    y = np.array(y)
    x = np.array(x)

    plt.plot(x, y, '-', color = "red")

    plt.ylabel('Average log time')
    plt.xlabel('Number of insertions')

    # setting y-axis range
    plt.ylim([0.5, 1.5])
    plt.show()

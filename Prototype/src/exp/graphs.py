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
    y1 = []
    y2 = []
    y3 = []
    y4 = []
    y5 = []
    y6 = []

    numOfTransactions = len(x)
    for i in range(numOfTransactions):
        y1.append(times[i][0])
        y2.append(times[i][1])
        y3.append(times[i][2])
        y4.append(times[i][3][0])
        y5.append(times[i][3][1])
        y6.append(times[i][3][2])

    plt.plot(x, y1, '-', color="red", label="random order transactions")
    plt.plot(x, y3, '-', color="blue", label="transactions in decreasing order")
    plt.plot(x, y2, '-', color="green", label="transactions in increasing order")

    plt.title("Average log time against number of insertions for logTransactions")
    plt.legend()
    plt.ylabel('Average log time')
    plt.xlabel('Number of insertions')

    # setting y-axis range
    plt.ylim([0, 1])
    plt.show()

    plt.plot(x, y3, '-', color="red", label="same transactions for stockName1")
    plt.plot(x, y4, '-', color="blue", label="same transactions for stockName2")
    plt.plot(x, y5, '-', color="green", label="same transactions for stockName3")
    plt.title("Average log time against number of equal transactions for 3 different stocks")
    plt.ylabel("Average log time")
    plt.xlabel("Number of insertions")
    plt.legend()
    plt.ylim([0, 1])
    plt.show()



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
    start_time = timeit.default_timer()
    for i in range(num):
        stp.logTransaction(tdg.generateTransactionData(1))
    end_time = timeit.default_timer()

    time_taken = end_time - start_time
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

    plt.plot(x, y, '-', color = 'red')

    plt.ylabel('Average log time')
    plt.xlabel('Number of insertions')

    # setting y-axis range
    plt.ylim([0.5, 1.5])
    plt.show()


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

    plt.plot(x, y1, '-', color = "red", label = "random order transactions")
    plt.plot(x, y3, '-', color = "blue", label = "transactions in decreasing order")
    plt.plot(x, y2, '-', color = "green", label = "transactions in increasing order")

    plt.title("Average log time against number of insertions for logTransactions")
    plt.legend()
    plt.ylabel('Average log time')
    plt.xlabel('Number of insertions')

    # setting y-axis range
    plt.ylim([0, 1])
    plt.show()

    plt.plot(x, y4, '-', color = "red", label = "same transactions for stockName1")
    plt.plot(x, y5, '-', color = "blue", label = "same transactions for stockName2")
    plt.plot(x, y6, '-', color = "green", label = "same transactions for stockName3")
    plt.title("Average log time against number of equal transactions for 3 different stocks")
    plt.ylabel("Average log time")
    plt.xlabel("Number of insertions")
    plt.legend()
    plt.ylim([0, 0.01])
    plt.show()


def plotSortedTransactions(x, times, stockName1, stockName2, stockName3):
    y1 = []
    y2 = []
    y3 = []

    numOfTransactions = len(x)
    for i in range(numOfTransactions):
        index = i * 3
        y1.append(times[index])
        y2.append(times[index + 1])
        y3.append(times[index + 2])

    plt.plot(x, y1, '-', color = "red", label = stockName1)
    plt.plot(x, y3, '-', color = "blue", label = stockName2)
    plt.plot(x, y2, '-', color = "green", label = stockName3)

    plt.title("Average time to sort the transactions")
    plt.legend()
    plt.ylabel('Average time')
    plt.xlabel('Number of transactions in the platform')

    # setting y-axis range
    plt.ylim([0, 0.0009])
    plt.show()

def plotMinTransactions(x, times, stockName1, stockName2, stockName3):
    y1 = []
    y2 = []
    y3 = []

    numOfTransactions = len(x)
    for i in range(numOfTransactions):
        index = i * 3
        y1.append(times[index])
        y2.append(times[index + 1])
        y3.append(times[index + 2])

    plt.plot(x, y1, '-', color = "red", label = stockName1)
    plt.plot(x, y3, '-', color = "blue", label = stockName2)
    plt.plot(x, y2, '-', color = "green", label = stockName3)

    plt.title("Average time to find the minimum transaction")
    plt.legend()
    plt.ylabel('Average time')
    plt.xlabel('Number of transactions in the platform')

    # setting y-axis range
    plt.ylim([0, 0.0009])
    plt.show()

def plotMaxTransactions(x, times, stockName1, stockName2, stockName3):
    y1 = []
    y2 = []
    y3 = []

    numOfTransactions = len(x)
    for i in range(numOfTransactions):
        index = i * 3
        y1.append(times[index])
        y2.append(times[index + 1])
        y3.append(times[index + 2])

    plt.plot(x, y1, '-', color = "red", label = stockName1)
    plt.plot(x, y3, '-', color = "blue", label = stockName2)
    plt.plot(x, y2, '-', color = "green", label = stockName3)

    plt.title("Average time to find the maximum transaction")
    plt.legend()
    plt.ylabel('Average time')
    plt.xlabel('Number of transactions in the platform')

    # setting y-axis range
    plt.ylim([0, 0.0009])
    plt.show()

def y_coords(x, times):
    y1 = []
    y2 = []
    y3 = []
    y4 = []
    y5 = []
    y6 = []
    y7 = []
    y8 = []
    y9 = []

    numOfTransactions = len(x)
    for i in range(numOfTransactions):
        index = i * 3
        y1.append(times[index][0])
        y2.append(times[index][1])
        y3.append(times[index][2])
        y4.append(times[index + 1][0])
        y5.append(times[index + 1][1])
        y6.append(times[index + 1][2])
        y7.append(times[index + 2][0])
        y8.append(times[index + 2][1])
        y9.append(times[index + 2][2])

    return y1, y2, y3, y4, y5, y6, y7, y8, y9


def plotFloorTransactions(x, times, stockName1, stockName2, stockName3):
    y1, y2, y3, y4, y5, y6, y7, y8, y9 = y_coords(x, times)

    plt.plot(x, y1, '-', color = "red", label = "returning largest values below minimum")
    plt.plot(x, y2, '-', color = "blue", label = "returning largest value below maximum")
    plt.plot(x, y3, '-', color = "green", label = "returning largest value below middle value")

    plt.title("Average log time against number of insertions for floorTransactions tests on " + stockName1)
    plt.legend()
    plt.ylabel('Average log time')
    plt.xlabel('Number of insertions')

    # setting y-axis range
    plt.ylim([0, 0.00001])
    plt.show()

    plt.plot(x, y4, '-', color = "red", label = "returning largest values below minimum")
    plt.plot(x, y5, '-', color = "blue", label = "returning largest value below maximum")
    plt.plot(x, y6, '-', color = "green", label = "returning largest value below middle value")

    plt.title("Average log time against number of insertions for floorTransactions tests on " + stockName2)
    plt.legend()
    plt.ylabel('Average log time')
    plt.xlabel('Number of insertions')

    # setting y-axis range
    plt.ylim([0, 0.00001])
    plt.show()

    plt.plot(x, y7, '-', color = "red", label = "returning largest values below minimum")
    plt.plot(x, y8, '-', color = "blue", label = "returning largest value below maximum")
    plt.plot(x, y9, '-', color = "green", label = "returning largest value below middle value")

    plt.title("Average log time against number of insertions for floorTransactions tests on " + stockName3)
    plt.legend()
    plt.ylabel('Average log time')
    plt.xlabel('Number of insertions')

    # setting y-axis range
    plt.ylim([0, 0.00001])
    plt.show()

    pass


def plotCeilingTransactions(x, times, stockName1, stockName2, stockName3):
    y1, y2, y3, y4, y5, y6, y7, y8, y9 = y_coords(x, times)

    plt.plot(x, y1, '-', color = "red", label = "returning smallest value below minimum")
    plt.plot(x, y2, '-', color = "blue", label = "returning smallest value below maximum")
    plt.plot(x, y3, '-', color = "green", label = "returning smallest value below middle value")

    plt.title("Average log time against number of insertions for ceilingTransactions tests on " + stockName1)
    plt.legend()
    plt.ylabel('Average log time')
    plt.xlabel('Number of insertions')

    # setting y-axis range
    plt.ylim([0, 0.00001])
    plt.show()

    plt.plot(x, y4, '-', color = "red", label = "returning smallest values below minimum")
    plt.plot(x, y5, '-', color = "blue", label = "returning smallest value below maximum")
    plt.plot(x, y6, '-', color = "green", label = "returning smallest value below middle value")

    plt.title("Average log time against number of insertions for ceilingTransactions tests on " + stockName2)
    plt.legend()
    plt.ylabel('Average log time')
    plt.xlabel('Number of insertions')

    # setting y-axis range
    plt.ylim([0, 0.00001])
    plt.show()

    plt.plot(x, y7, '-', color = "red", label = "returning smallest values below minimum")
    plt.plot(x, y8, '-', color = "blue", label = "returning smallest value below maximum")
    plt.plot(x, y9, '-', color = "green", label = "returning smallest value below middle value")

    plt.title("Average log time against number of insertions for ceilingTransactions tests on " + stockName3)
    plt.legend()
    plt.ylabel('Average log time')
    plt.xlabel('Number of insertions')

    # setting y-axis range
    plt.ylim([0, 0.00001])
    plt.show()


def plotRangeTransactions(x, times, stockName1, stockName2, stockName3):
    y1, y2, y3, y4, y5, y6, y7, y8, y9 = y_coords(x, times)

    plt.plot(x, y1, '-', color = "red", label = "return values between min and max value")
    plt.plot(x, y2, '-', color = "blue", label = "return values between min and middle value")
    plt.plot(x, y3, '-', color = "green", label = "return values between middle and max value")

    plt.title("Average log time against number of insertions for rangeTransactions tests on " + stockName1)
    plt.legend()
    plt.ylabel('Average log time')
    plt.xlabel('Number of insertions')

    # setting y-axis range
    plt.ylim([0, 0.001])
    plt.show()

    plt.plot(x, y4, '-', color = "red", label = "return values between min and max value")
    plt.plot(x, y5, '-', color = "blue", label = "return values between min and middle value")
    plt.plot(x, y6, '-', color = "green", label = "return values between middle and max value")

    plt.title("Average log time against number of insertions for rangeTransactions tests on " + stockName2)
    plt.legend()
    plt.ylabel('Average log time')
    plt.xlabel('Number of insertions')

    # setting y-axis range
    plt.ylim([0, 0.001])
    plt.show()

    plt.plot(x, y7, '-', color = "red", label = "return values between min and max value")
    plt.plot(x, y8, '-', color = "blue", label = "return values between min and middle value")
    plt.plot(x, y9, '-', color = "green", label = "return values between middle and max value")

    plt.title("Average log time against number of insertions for rangeTransactions tests on " + stockName3)
    plt.legend()
    plt.ylabel('Average log time')
    plt.xlabel('Number of insertions')

    # setting y-axis range
    plt.ylim([0, 0.001])
    plt.show()

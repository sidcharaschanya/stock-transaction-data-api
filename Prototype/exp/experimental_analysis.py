import timeit
import datetime
import random
from transaction_data_generator import TransactionDataGenerator
from stocks.platform import StockTradingPlatform

stockNames = ["Barclays", "HSBA", "Lloyds", "Banking Group", "Natwest Group", "Standard Chartered", "3i", "Abdrdn",
              "Hargreaves", "Lansdown", "London Stock Exchange Group", "Perching Square Holdings", "Schroders",
              "St. James' Place plc."]
currentTime = datetime.datetime.now()
currentTime = currentTime.strftime("%d/%m/%Y %H:%M:%S")

stp = StockTradingPlatform()


# generate 3 random stock names from start, middle and end of the list.
def generateStockNames():
    firstFour = stockNames[0:4]
    middleFour = stockNames[5:8]
    lastFour = stockNames[9:12]
    stockName1 = firstFour[random.randint(0, 3)]
    stockName2 = middleFour[random.randint(0, 3)]
    stockName3 = lastFour[random.randint(0, 3)]
    return stockName1, stockName2, stockName3


# generate random transactions of a given number for a specific stock.
def generateTransactions(stockName, num):
    for i in range(num):
        pricePerStock = round(random.uniform(50.00, 100.00), 2)
        quantity = random.randint(10, 1000)
        record = [stockName, pricePerStock, quantity, currentTime]
        stp.log_transaction(record)


# returns the trade value for a transaction.
def tradeValue(transaction):
    tradeValue = transaction[1] * transaction[2]
    return tradeValue


def sort():
    pass


# Test 1 for logTransactions: execution time when the transactions logged are in random order.
def logTransactionsTest1(num):
    timeTaken = timeit.repeat(stp.log_transaction(TransactionDataGenerator.generateTransactionData(1)), repeat = num,
                              number = 1000)
    return timeTaken


# Test for sortedTransactions: time taken for function to return the sorted list of transactions for a stock.
def sortedTransactionsTest(stockName):
    timeTaken = timeit.timeit(stp.sorted_transactions(stockName), number = 1000)
    return timeTaken


# Test for minTransaction: time taken for function to return the minimum transaction for a stock.
def minTransactionsTest(stockName):
    timeTaken = timeit.timeit(stp.min_transactions(stockName), number = 1000)
    return timeTaken


# Test for maxTransaction: time taken for function to return the maximum transaction for a stock.
def maxTransactionsTest(stockName):
    timeTaken = timeit.timeit(stp.max_transactions(stockName), number = 1000)
    return timeTaken


# Test 1 for floorTransactions: execution time when finding the largest trade value below the minimum for a stock.
def floorTransactionsTest1(stockName):
    num = getMin(stockName)
    timeTaken = timeit.timeit(stp.floor_transactions(stockName, num), number = 1000)
    return timeTaken


# Test 2 for floorTransactions: execution time when finding the largest trade value below the maximum for a stock.
def floorTransactionsTest2(stockName):
    num = getMax(stockName)
    timeTaken = timeit.timeit(stp.floor_transactions(stockName, num), number = 1000)
    return timeTaken


# Test 3 for floorTransactions: execution time when finding the largest trade value below all transactions for a stock.
def floorTransactionsTest3(stockName, num):
    timeTaken = timeit.timeit(stp.floor_transactions(stockName, num), number = 1000)
    return timeTaken


# Test 1 for ceilingTransactions: execution time when finding the smallest trade value below the minimum for a stock.
def ceilingTransactionsTest1(stockName):
    num = getMin(stockName)
    timeTaken = timeit.timeit(stp.ceiling_transactions(stockName, num), number = 1000)
    return timeTaken


# Test 2 for ceilingTransactions: execution time when finding the smallest trade value below the maximum for a stock.
def ceilingTransactionsTest2(stockName):
    num = getMax(stockName)
    timeTaken = timeit.timeit(stp.ceiling_transactions(stockName, num), number = 1000)
    return timeTaken


# Test 3 for ceilingTransactions: execution time when finding the smallest trade value below all transactions for a stock.
def ceilingTransactionsTest3(stockName, transactions):
    num = transactions.pop(0)
    timeTaken = timeit.timeit(stp.ceiling_transactions(stockName, num), number = 1000)
    print(timeTaken)
    ceilingTransactionsTest3(stockName, transactions)


# Testing all cases for floorTransactions
def floorTransactionsTests(stockName):
    times = []
    times3 = []

    floorTransactionsTest1(stockName)
    floorTransactionsTest2(stockName)

    transactions = stp.sorted_transactions(stockName)
    numOfTransactions = len(transactions)
    transactions.pop(0)
    transactions.pop(numOfTransactions - 1)
    for i in range(numOfTransactions - 3):
        num = transactions.pop(0)
        times3.append(floorTransactionsTest3(stockName, num))

    times.append(times3)

    return times


# Testing all cases for ceilingTransactions
def ceilingTransactionsTests(stockName):
    times = []
    times3 = []

    times.append(ceilingTransactionsTest1(stockName))
    times.append(ceilingTransactionsTest2(stockName))

    transactions = stp.sorted_transactions(stockName)
    numOfTransactions = len(transactions)
    transactions.pop(0)
    transactions.pop(numOfTransactions - 1)
    for i in range(numOfTransactions - 3):
        num = transactions.pop(0)
        times3.append(ceilingTransactionsTest3(stockName, num))
    times.append(times3)

    return times


# Test 1 for rangeTransactions: time taken for rangeTransactions to return all transactions in between the maximum and minimum.
def rangeTransactionsTest1(stockName):
    fromValue = getMin(stockName)
    toValue = getMax(stockName)
    timeTaken = timeit.timeit(stp.range_transactions(stockName, fromValue, toValue), number = 1000)
    return timeTaken


# Test 2 for range Transactions: times taken for rangeTransactions to return all transactions in between the minimum and
# every other transaction excluding the maximum.
def rangeTransactionsTest2(stockName, transactions):
    times = []
    transactions.pop(0)

    fromValue = getMin(stockName)
    numOfTransactions = len(transactions)
    for i in range(1, numOfTransactions - 2):
        toValue = transactions[i]
        times.append(timeit.timeit(stp.range_transactions(stockName, fromValue, toValue), number = 1000))

    return times


# Test 3 for range Transactions: time taken for rangeTransaction to return all transaction in between all other
# transactions excluding the minimum and the maximum
def rangeTransactionsTest3(stockName, transactions):
    times = []
    transactions.pop(0)

    toValue = getMax(stockName)
    numOfTransactions = len(transactions)
    for i in range(numOfTransactions - 2, 1):
        fromValue = transactions[i]
        times.append(timeit.timeit(stp.range_transactions(stockName, fromValue, toValue), number = 1000))

    # returns a list
    return times


# testing all cases for rangeTransactions.
def rangeTransactionsTests(stockName):
    times = []

    transactions = stp.sorted_transactions(stockName)
    times.append(rangeTransactionsTest1(stockName))
    times.append(rangeTransactionsTest2(stockName, transactions))
    times.append(rangeTransactionsTest3(stockName, transactions))

    return times


# return the minimum transaction for stock.
def getMin(stockName):
    min = stp.min_transactions(stockName)
    if len(min) > 1:
        return min[0]
    else:
        return min


# return the maximum transaction for a stock.
def getMax(stockName):
    max = stp.max_transactions(stockName)
    if len(max) > 1:
        return max[0]
    else:
        return max


def outputData(times):
    if type(times) == list:
        n = 0
        for time in times:
            print("Time taken for test ", n, ": ", time, "\n")
    else:
        print("Time taken : ", times, "\n")


def runTests(stockName):
    print("Tests for ", stockName)
    # log transactions
    print("Data for sortedTransactions tests: \n")
    outputData(sortedTransactionsTest(stockName))
    print("Data for minTransactions tests: \n")
    outputData(minTransactionsTest(stockName))
    print("Data for maxTransactions tests: \n")
    outputData(maxTransactionsTest(stockName))
    print("Data for floorTransactions tests: \n")
    outputData(floorTransactionsTests(stockName))
    print("Data for ceilingTransactions tests: \n")
    outputData(ceilingTransactionsTests(stockName))
    print("Data for rangeTransactions tests: \n")
    outputData(rangeTransactionsTests(stockName))


def testing():
    N = [10, 100, 1000]
    stockName1, stockName2, stockName3 = generateStockNames()

    for num in N:
        generateTransactions(stockName1, num)
        generateTransactions(stockName2, num)
        generateTransactions(stockName3, num)
        runTests(stockName1)
        runTests(stockName2)
        runTests(stockName3)

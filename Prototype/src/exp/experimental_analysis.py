import timeit
import datetime
import random
from src.exp.transaction_data_generator import TransactionDataGenerator
from src.stocks.platform import StockTradingPlatform

stockNames = ["Barclays", "HSBA", "Lloyds Banking Group", "NatWest Group",
              "Standard Chartered", "3i", "Abrdn", "Hargreaves Lansdown",
              "London Stock Exchange Group", "Pershing Square Holdings",
              "Schroders", "St. James's Place plc."]
currentTime = datetime.datetime.now()
currentTime = currentTime.strftime("%d/%m/%Y %H:%M:%S")

stp = StockTradingPlatform()
stp1 = StockTradingPlatform()
stp2 = StockTradingPlatform()
stp3 = StockTradingPlatform()
testData = TransactionDataGenerator()
numRuns = 10


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
    listTransactions = []
    for i in range(num):
        pricePerStock = round(random.uniform(50.00, 100.00), 2)
        quantity = random.randint(10, 1000)
        record = [stockName, pricePerStock, quantity, currentTime]
        listTransactions.append(record)
        stp.logTransaction(record)
    return listTransactions


# returns the trade value for a transaction.
def tradeValue(transaction):
    tradeValue = transaction[1] * transaction[2]
    return tradeValue


def sort():
    sortedListTransactions = []
    for stockName in stockNames:
        transactions = stp1.sortedTransactions(stockName)
        num = len(transactions)
        for i in range(0, num - 1):
            sortedListTransactions.append(transactions[i].to_list())

    return sortedListTransactions


def testingLogTransactions(num):
    times = []
    # Test 1 for logTransactions: execution time when the transactions logged are in random order.
    listTransactions = testData.generateTransactionData(num)
    times.append(logTransactionsTest(listTransactions, stp1))
    # Test 2 for logTransactions: execution time when the transactions logged are in increasing order.
    listTransactions = sort()
    times.append(logTransactionsTest(listTransactions, stp2))
    # Test 3 for logTransactions: execution time when the transactions logged are in decreasing order.
    listTransactions.reverse()
    times.append(logTransactionsTest(listTransactions, stp3))

    return times


def logTransactionsTest(listTransactions, system):
    timeTaken = 0
    for n in range(numRuns):
        for transaction in listTransactions:
            startTime = timeit.default_timer()
            system.logTransaction(transaction)
            endTime = timeit.default_timer()
            timeTaken += endTime - startTime
    timeTaken = round((timeTaken / numRuns), 8)

    return timeTaken


# Test for sortedTransactions: time taken for function to return the sorted list of transactions for a stock.
def sortedTransactionsTest(stockName):
    timeTaken = 0
    for n in range(numRuns):
        startTime = timeit.default_timer()
        stp.sortedTransactions(stockName)
        endTime = timeit.default_timer()
        timeTaken += endTime - startTime
    timeTaken = round((timeTaken / numRuns), 4)
    return timeTaken


# Test for minTransaction: time taken for function to return the minimum transaction for a stock.
def minTransactionsTest(stockName):
    timeTaken = 0
    for n in range(numRuns):
        startTime = timeit.default_timer()
        stp.minTransactions(stockName)
        endTime = timeit.default_timer()
        timeTaken += endTime - startTime
    timeTaken = round((timeTaken / numRuns), 8)
    return timeTaken


# Test for maxTransaction: time taken for function to return the maximum transaction for a stock.
def maxTransactionsTest(stockName):
    timeTaken = 0
    for n in range(numRuns):
        startTime = timeit.default_timer()
        stp.maxTransactions(stockName)
        endTime = timeit.default_timer()
        timeTaken += endTime - startTime
    timeTaken = round((timeTaken / numRuns), 8)
    return timeTaken


def floorTransactionsTest(stockName, num):
    timeTaken = 0
    for n in range(numRuns):
        startTime = timeit.default_timer()
        stp.floorTransactions(stockName, num)
        endTime = timeit.default_timer()
        timeTaken += endTime - startTime
    timeTaken = round((timeTaken / numRuns), 8)
    return timeTaken


def ceilingTransactionsTest(stockName, num):
    timeTaken = 0
    for n in range(numRuns):
        startTime = timeit.default_timer()
        stp.ceilingTransactions(stockName, num)
        endTime = timeit.default_timer()
        timeTaken += endTime - startTime
    timeTaken = round((timeTaken / numRuns), 8)
    return timeTaken


# Testing all cases for floorTransactions
def testingFloorTransactions(stockName):
    minTradeValue = tradeValue(getMin(stockName)[0])
    maxTradeValue = tradeValue(getMax(stockName)[0])
    midTradeValue = middleTradeValue(stockName)

    times = []

    # Test 1 for floorTransactions: execution time when finding the largest trade value below the minimum for a stock.
    times.append(floorTransactionsTest(stockName, minTradeValue))

    # Test 2 for floorTransactions: execution time when finding the largest trade value below the maximum for a stock.
    times.append(floorTransactionsTest(stockName, maxTradeValue))

    # Test 3 for floorTransactions: execution time when finding the largest trade value below the middle trade value
    # for a stock.
    times.append(floorTransactionsTest(stockName, midTradeValue))

    return times


# Testing all cases for ceilingTransactions
def testingCeilingTransactions(stockName):
    minTradeValue = tradeValue(getMin(stockName)[0])
    maxTradeValue = tradeValue(getMax(stockName)[0])
    midTradeValue = middleTradeValue(stockName)
    times = []
    times3 = []

    # Test 1 for ceilingTransactions: execution time when finding the smallest trade value below the minimum for a stock.
    times.append(ceilingTransactionsTest(stockName, minTradeValue))

    # Test 2 for ceilingTransactions: execution time when finding the smallest trade value below the maximum for a stock.
    times.append(ceilingTransactionsTest(stockName, maxTradeValue))

    # Test 3 for ceilingTransactions: execution time when finding the smallest trade value below the middle trade value.
    times.append(ceilingTransactionsTest(stockName, midTradeValue))

    return times


# Test 1 for rangeTransactions: time taken for rangeTransactions to return all transactions in between the maximum
# and minimum trade values for a stock.
def rangeTransactionsTest(stockName, fromValue, toValue):
    timeTaken = 0
    for n in range(numRuns):
        startTime = timeit.default_timer()
        stp.rangeTransactions(stockName, fromValue, toValue)
        endTime = timeit.default_timer()
        timeTaken += endTime - startTime
    timeTaken = round((timeTaken / numRuns), 8)
    return timeTaken


# Test 2 for range Transactions: times taken for rangeTransactions to return transactions between the minimum and
# middle trade values for a stock


# Test 3 for range Transactions: time taken for rangeTransactions to return all transactions in between middle and
# maximum trade values for a stock.


# testing all cases for rangeTransactions.
def rangeTransactionsTests(stockName):
    minTradeValue = tradeValue(getMin(stockName)[0])
    midTradeValue = middleTradeValue(stockName)
    maxTradeValue = tradeValue(getMax(stockName)[0])
    times = []

    # Test 1 for rangeTransactions: time taken for rangeTransactions to return all transactions in between the maximum
    # and minimum trade values for a stock.
    times.append(rangeTransactionsTest(stockName, minTradeValue, maxTradeValue))

    # Test 2 for range Transactions: times taken for rangeTransactions to return transactions between the minimum and
    # middle trade values for a stock
    times.append(rangeTransactionsTest(stockName, minTradeValue, midTradeValue))

    # Test 3 for range Transactions: time taken for rangeTransactions to return all transactions in between middle and
    # maximum trade values for a stock.
    times.append(rangeTransactionsTest(stockName, midTradeValue, maxTradeValue))

    return times


# return the minimum transaction for a stock.
def getMin(stockName):
    min = stp.minTransactions(stockName)
    try:
        min = [min[0].to_list()]
    except:
        min = 0
    else:
        if len(min) > 1:
            return min[0]
        else:
            return min


# return the maximum transaction for a stock.
def getMax(stockName):
    max = stp.maxTransactions(stockName)
    try:
        max = [max[0].to_list()]
    except:
        max = 0
    else:
        if len(max) > 1:
            return max[0]
        else:
            return max


def middleTradeValue(stockName):
    sortedListTransactions = []
    transactions = stp.sortedTransactions(stockName)
    num = len(transactions) - 1
    for i in range(0, num):
        sortedListTransactions.append(transactions[i].to_list())
    if len(sortedListTransactions) == 1:
        return tradeValue(sortedListTransactions[0])
    elif len(sortedListTransactions) == 0:
        return 0
    else:
        middle = num // 2
        middleTransaction = sortedListTransactions[middle]
        middleValue = tradeValue(middleTransaction)
        return middleValue


def outputData(times):
    if type(times) == list:
        n = 1
        for time in times:
            print("Time taken for test ", n, ": ", time)
            n += 1
    else:
        print("Time taken : ", times, "\n")


def testing(stockName):
    print("Tests for ", stockName, "\n")
    print("Data for sortedTransactions tests: \n")
    outputData(sortedTransactionsTest(stockName))
    print("Data for minTransactions tests: \n")
    outputData(minTransactionsTest(stockName))
    print("Data for maxTransactions tests: \n")
    outputData(maxTransactionsTest(stockName))
    print("Data for floorTransactions tests: \n")
    outputData(testingFloorTransactions(stockName))
    print("Data for ceilingTransactions tests: \n")
    outputData(testingCeilingTransactions(stockName))
    print("Data for rangeTransactions tests: \n")
    outputData(rangeTransactionsTests(stockName))


def runTests():
    N = 1000
    stockName1, stockName2, stockName3 = generateStockNames()

    print("Data for logTransactions test for N transactions: \n")
    outputData(testingLogTransactions(N))
    print("For N = ", N, "\n")
    generateTransactions(stockName1, N)
    generateTransactions(stockName2, N)
    generateTransactions(stockName3, N)
    testing(stockName1)
    testing(stockName2)
    testing(stockName3)


runTests()

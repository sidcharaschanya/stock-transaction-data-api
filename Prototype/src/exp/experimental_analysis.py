import timeit
import datetime
import random
from src.exp.transaction_data_generator import TransactionDataGenerator
from src.stocks.platform import StockTradingPlatform
import graphs

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
stp4 = StockTradingPlatform()

testData = TransactionDataGenerator()
numRuns = 10


logTransactionTimes = []


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


def generateEqualTransactions(stockName, num):
    listTransactions = []
    pricePerStock = round(random.uniform(50.00, 100.00), 2)
    quantity = random.randint(10, 1000)
    record = [stockName, pricePerStock, quantity, currentTime]
    for i in range(num):
        listTransactions.append(record)
    return listTransactions


# returns the trade value for a transaction.
def tradeValue(transaction):
    if transaction == 0:
        return 0
    else:
        transaction = transaction[0]
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


def testingLogTransactions(stockName1, stockName2, stockName3, num):
    times = []
    stockNames = [stockName1, stockName2, stockName3]

    # Test 1 for logTransactions: execution time when the transactions logged are in random order.
    listTransactions = testData.generateTransactionData(num)
    times.append(logTransactionsTest(listTransactions, stp1))

    # Test 2 for logTransactions: execution time when the transactions logged are in increasing order.
    listTransactions = sort()
    times.append(logTransactionsTest(listTransactions, stp2))

    # Test 3 for logTransactions: execution time when the transactions logged are in decreasing order.
    listTransactions.reverse()
    times.append(logTransactionsTest(listTransactions, stp3))

    # Test 4 for logTransactions: execution time when all the transactions logged are the same, for 3 different,
    # random stock.
    time = []
    for stockName in stockNames:
        listTransactions = generateEqualTransactions(stockName, num)
        time.append(logTransactionsTest(listTransactions, stp4))
    times.append(time)

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
def sortedTransactionsTest(stockName, system):
    timeTaken = 0
    for n in range(numRuns):
        startTime = timeit.default_timer()
        system.sortedTransactions(stockName)
        endTime = timeit.default_timer()
        timeTaken += endTime - startTime
    timeTaken = round((timeTaken / numRuns), 4)
    return timeTaken


# Test for minTransaction: time taken for function to return the minimum transaction for a stock.
def minTransactionsTest(stockName, system):
    timeTaken = 0
    for n in range(numRuns):
        startTime = timeit.default_timer()
        system.minTransactions(stockName)
        endTime = timeit.default_timer()
        timeTaken += endTime - startTime
    timeTaken = round((timeTaken / numRuns), 8)
    return timeTaken


# Test for maxTransaction: time taken for function to return the maximum transaction for a stock.
def maxTransactionsTest(stockName, system):
    timeTaken = 0
    for n in range(numRuns):
        startTime = timeit.default_timer()
        system.maxTransactions(stockName)
        endTime = timeit.default_timer()
        timeTaken += endTime - startTime
    timeTaken = round((timeTaken / numRuns), 8)
    return timeTaken


def floorTransactionsTest(stockName, num, system):
    timeTaken = 0
    for n in range(numRuns):
        startTime = timeit.default_timer()
        system.floorTransactions(stockName, num)
        endTime = timeit.default_timer()
        timeTaken += endTime - startTime
    timeTaken = round((timeTaken / numRuns), 8)
    return timeTaken


def ceilingTransactionsTest(stockName, num, system):
    timeTaken = 0
    for n in range(numRuns):
        startTime = timeit.default_timer()
        system.ceilingTransactions(stockName, num)
        endTime = timeit.default_timer()
        timeTaken += endTime - startTime
    timeTaken = round((timeTaken / numRuns), 8)
    return timeTaken


# Testing all cases for floorTransactions
def testingFloorTransactions(stockName, system):
    minTradeValue = tradeValue(getMin(stockName))
    maxTradeValue = tradeValue(getMax(stockName))
    midTradeValue = middleTradeValue(stockName)

    times = []

    # Test 1 for floorTransactions: execution time when finding the largest trade value below the minimum for a stock.
    times.append(floorTransactionsTest(stockName, minTradeValue, system))

    # Test 2 for floorTransactions: execution time when finding the largest trade value below the maximum for a stock.
    times.append(floorTransactionsTest(stockName, maxTradeValue, system))

    # Test 3 for floorTransactions: execution time when finding the largest trade value below the middle trade value
    # for a stock.
    times.append(floorTransactionsTest(stockName, midTradeValue, system))

    return times


# Testing all cases for ceilingTransactions
def testingCeilingTransactions(stockName, system):
    minTradeValue = tradeValue(getMin(stockName))
    maxTradeValue = tradeValue(getMax(stockName))
    midTradeValue = middleTradeValue(stockName)
    times = []
    times3 = []

    # Test 1 for ceilingTransactions: execution time when finding the smallest trade value below the minimum
    # for a stock.
    times.append(ceilingTransactionsTest(stockName, minTradeValue, system))

    # Test 2 for ceilingTransactions: execution time when finding the smallest trade value below the maximum
    # for a stock.
    times.append(ceilingTransactionsTest(stockName, maxTradeValue, system))

    # Test 3 for ceilingTransactions: execution time when finding the smallest trade value below the middle trade value.
    times.append(ceilingTransactionsTest(stockName, midTradeValue, system))

    return times


# Test 1 for rangeTransactions: time taken for rangeTransactions to return all transactions in between the maximum
# and minimum trade values for a stock.
def rangeTransactionsTest(stockName, fromValue, toValue, system):
    timeTaken = 0
    for n in range(numRuns):
        startTime = timeit.default_timer()
        system.rangeTransactions(stockName, fromValue, toValue)
        endTime = timeit.default_timer()
        timeTaken += endTime - startTime
    timeTaken = round((timeTaken / numRuns), 8)
    return timeTaken


# testing all cases for rangeTransactions.
def testingRangeTransactions(stockName, system):
    minTradeValue = tradeValue(getMin(stockName))
    midTradeValue = middleTradeValue(stockName)
    maxTradeValue = tradeValue(getMax(stockName))

    times = []

    # Test 1 for rangeTransactions: time taken for rangeTransactions to return all transactions in between the maximum
    # and minimum trade values for a stock.
    times.append(rangeTransactionsTest(stockName, minTradeValue, maxTradeValue, system))

    # Test 2 for rangeTransactions: times taken for rangeTransactions to return transactions between the minimum and
    # middle trade values for a stock
    times.append(rangeTransactionsTest(stockName, minTradeValue, midTradeValue, system))

    # Test 3 for rangeTransactions: time taken for rangeTransactions to return all transactions in between middle and
    # maximum trade values for a stock.
    times.append(rangeTransactionsTest(stockName, midTradeValue, maxTradeValue, system))

    return times


# Repeat all tests but with a system that has transactions which are all equal.
def testingEqualTransactions(stockName):
    times = []

    times.append(sortedTransactionsTest(stockName, stp4))
    times.append(minTransactionsTest(stockName, stp4))
    times.append(maxTransactionsTest(stockName, stp4))
    times.append(testingFloorTransactions(stockName, stp4))
    times.append(testingCeilingTransactions(stockName, stp4))
    times.append(testingRangeTransactions(stockName, stp4))

    return times


# return the minimum transaction for a stock.
def getMin(stockName):
    min = stp.minTransactions(stockName)
    try:
        min = [min[0].to_list()]
    except:
        return 0
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
        return 0
    else:
        if len(max) > 1:
            return max[0]
        else:
            return max


def middleTradeValue(stockName):
    sortedListTransactions = []
    transactions = stp.sortedTransactions(stockName)
    num = len(transactions)
    for i in range(0, num):
        sortedListTransactions.append(transactions[i].to_list())
    if len(sortedListTransactions) == 1:
        return tradeValue(sortedListTransactions)
    elif len(sortedListTransactions) == 0:
        return 0
    else:
        middle = num // 2
        middleTransaction = [sortedListTransactions[middle]]
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
    return times


def testing(stockName):
    print("Tests for ", stockName, "\n")
    print("Data for sortedTransactions tests: \n")
    outputData(sortedTransactionsTest(stockName, stp))
    print("Data for minTransactions tests: \n")
    outputData(minTransactionsTest(stockName, stp))
    print("Data for maxTransactions tests: \n")
    outputData(maxTransactionsTest(stockName, stp))
    print("Data for floorTransactions tests: \n")
    outputData(testingFloorTransactions(stockName, stp))
    print("Data for ceilingTransactions tests: \n")
    outputData(testingCeilingTransactions(stockName, stp))
    print("Data for rangeTransactions tests: \n")
    outputData(testingRangeTransactions(stockName, stp))
    print("Data for all tests repeated with equal transactions: \n")
    times = (testingEqualTransactions(stockName))
    for time in times:
        outputData(time)



def runTests():
    N = [0, 1, 10, 50, 100, 200, 300, 400, 500, 600, 700, 1000]
    stockName1, stockName2, stockName3 = generateStockNames()

    for num in N:
        print("Data for logTransactions test for N transactions: \n")
        times = outputData(testingLogTransactions(stockName1, stockName2, stockName3, num))
        logTransactionTimes.append(times)
        print(logTransactionTimes)
        print("For N = ", num, "\n")
        generateTransactions(stockName1, num)
        generateTransactions(stockName2, num)
        generateTransactions(stockName3, num)
        testing(stockName1)
        testing(stockName2)
        testing(stockName3)

    graphs.plotLogTransactions(N, logTransactionTimes)


runTests()

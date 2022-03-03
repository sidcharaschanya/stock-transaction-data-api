import timeit
import datetime
import random
from transaction_data_generator import TransactionDataGenerator
from src.stocks.platform import StockTradingPlatform

stockNames = ["Barclays", "HSBA", "Lloyds Banking Group", "NatWest Group",
                           "Standard Chartered", "3i", "Abrdn", "Hargreaves Lansdown",
                           "London Stock Exchange Group", "Pershing Square Holdings",
                           "Schroders", "St. James's Place plc."]
currentTime = datetime.datetime.now()
currentTime = currentTime.strftime("%d/%m/%Y %H:%M:%S")

stp = StockTradingPlatform()
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
        transactions = stp.sortedTransactions(stockName)
        num = len(transactions)
        for i in range(0, num - 1):
            sortedListTransactions.append(transactions[i].to_list())

    return sortedListTransactions


# Test 1 for logTransactions: execution time when the transactions logged are in random order.
def testingLogTransactions(num):
    times = []
    listTransactions = testData.generateTransactionData(num)
    times.append(logTransactionsTest(listTransactions, stp))
    listTransactions = sort()
    times.append(logTransactionsTest(listTransactions, stp2))
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
    timeTaken = round((timeTaken / numRuns), 4)

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


# Test 1 for floorTransactions: execution time when finding the largest trade value below the minimum for a stock.
def floorTransactionsTest1(stockName, num):
    timeTaken = 0
    for n in range(numRuns):
        startTime = timeit.default_timer()
        stp.floorTransactions(stockName, num)
        endTime = timeit.default_timer()
        timeTaken += endTime - startTime
    timeTaken = round((timeTaken / numRuns), 8)
    return timeTaken


# Test 2 for floorTransactions: execution time when finding the largest trade value below the maximum for a stock.
def floorTransactionsTest2(stockName, num):
    timeTaken = 0
    for n in range(numRuns):
        startTime = timeit.default_timer()
        stp.floorTransactions(stockName, num)
        endTime = timeit.default_timer()
        timeTaken += endTime - startTime
    timeTaken = round((timeTaken / numRuns), 8)
    return timeTaken


# Test 3 for floorTransactions: execution time when finding the largest trade value below all transactions
# excluding min and max for a stock.
def floorTransactionsTest3(stockName, num):
    timeTaken = 0
    for n in range(numRuns):
        startTime = timeit.default_timer()
        stp.floorTransactions(stockName, num)
        endTime = timeit.default_timer()
        timeTaken += endTime - startTime
    timeTaken = round((timeTaken / numRuns), 8)
    return timeTaken


# Test 1 for ceilingTransactions: execution time when finding the smallest trade value below the minimum for a stock.
def ceilingTransactionsTest1(stockName, num):
    timeTaken = 0
    for n in range(numRuns):
        startTime = timeit.default_timer()
        stp.ceilingTransactions(stockName, num)
        endTime = timeit.default_timer()
        timeTaken += endTime - startTime
    timeTaken = round((timeTaken / numRuns), 8)
    return timeTaken


# Test 2 for ceilingTransactions: execution time when finding the smallest trade value below the maximum for a stock.
def ceilingTransactionsTest2(stockName, num):
    startTime = timeit.default_timer()
    for n in range(numRuns):
        stp.ceilingTransactions(stockName, num)
    endTime = timeit.default_timer()
    timeTaken = round(((endTime - startTime) / numRuns), 8)
    return timeTaken


# Test 3 for ceilingTransactions: execution time when finding the smallest trade value below all transactions excluding
# min and max for a stock.
def ceilingTransactionsTest3(stockName, num):
    timeTaken = 0
    for n in range(numRuns):
        startTime = timeit.default_timer()
        stp.ceilingTransactions(stockName, num)
        endTime = timeit.default_timer()
        timeTaken += endTime - startTime
    timeTaken = round((timeTaken / numRuns), 8)
    return timeTaken


# Testing all cases for floorTransactions
def floorTransactionsTests(stockName):
    minTradeValue = tradeValue(getMin(stockName)[0])
    maxTradeValue = tradeValue(getMax(stockName)[0])
    times = []
    times3 = []

    times.append(floorTransactionsTest1(stockName, minTradeValue))
    times.append(floorTransactionsTest2(stockName, maxTradeValue))

    transactions = stp.sortedTransactions(stockName)
    numOfTransactions = len(transactions)
    transactions.pop(0)
    transactions.pop(numOfTransactions - 2)
    for i in range(numOfTransactions - 3):
        transaction = transactions.pop(0)
        transaction = transaction.to_list()
        num = tradeValue(transaction)
        times3.append(floorTransactionsTest3(stockName, num))

    times.append(times3)

    return times


# Testing all cases for ceilingTransactions
def ceilingTransactionsTests(stockName):
    minTradeValue = tradeValue(getMin(stockName)[0])
    maxTradeValue = tradeValue(getMax(stockName)[0])
    times = []
    times3 = []

    times.append(ceilingTransactionsTest1(stockName, minTradeValue))
    times.append(ceilingTransactionsTest2(stockName, maxTradeValue))

    transactions = stp.sortedTransactions(stockName)
    numOfTransactions = len(transactions)
    transactions.pop(0)
    transactions.pop(numOfTransactions - 2)
    for i in range(numOfTransactions - 3):
        transaction = transactions.pop(0)
        transaction = transaction.to_list()
        num = tradeValue(transaction)
        times3.append(ceilingTransactionsTest3(stockName, num))

    times.append(times3)

    return times


# Test 1 for rangeTransactions: time taken for rangeTransactions to return all transactions in between the maximum
# and minimum.
def rangeTransactionsTest1(stockName):
    fromValue = tradeValue(getMin(stockName)[0])
    toValue = tradeValue(getMax(stockName)[0])
    timeTaken = 0
    for n in range(numRuns):
        startTime = timeit.default_timer()
        stp.rangeTransactions(stockName, fromValue, toValue)
        endTime = timeit.default_timer()
        timeTaken += endTime - startTime
    timeTaken = round((timeTaken / numRuns), 8)
    return timeTaken


# Test 2 for range Transactions: times taken for rangeTransactions to return all transactions in between the minimum and
# every other transaction excluding the maximum.
def rangeTransactionsTest2(stockName, listTransactions):
    times = []
    listTransactions.pop(0)
    fromValue = tradeValue(getMin(stockName)[0])
    numOfTransactions = len(listTransactions)
    for i in range(1, numOfTransactions - 2):
        toValue = listTransactions[i]
        timeTaken = 0
        for n in range(numRuns):
            startTime = timeit.default_timer()
            stp.rangeTransactions(stockName, fromValue, toValue)
            endTime = timeit.default_timer()
            timeTaken += startTime - endTime
        timeTaken = round((timeTaken / numRuns), 8)
        times.append(timeTaken)
    return times


# Test 3 for range Transactions: time taken for rangeTransaction to return all transaction in between all other
# transactions excluding the minimum and the maximum
def rangeTransactionsTest3(stockName, listTransactions):
    times = []
    listTransactions.pop(0)
    toValue = tradeValue(getMax(stockName)[0])

    numOfTransactions = len(listTransactions)
    for i in range(numOfTransactions - 2, 1):
        fromValue = listTransactions[i]
        timeTaken = 0
        for n in range(numRuns):
            startTime = timeit.default_timer()
            stp.rangeTransactions(stockName, fromValue, toValue)
            endTime = timeit.default_timer()
            timeTaken += startTime - endTime
        timeTaken = round((timeTaken / numRuns), 8)
        times.append(timeTaken)
    return times


# testing all cases for rangeTransactions.
def rangeTransactionsTests(stockName):
    times = []

    transactions = stp.sortedTransactions(stockName)
    transactions = transactions[0].to_list()
    times.append(rangeTransactionsTest1(stockName))
    times.append(rangeTransactionsTest2(stockName, transactions))
    times.append(rangeTransactionsTest3(stockName, transactions))

    return times


# return the minimum transaction for stock.
def getMin(stockName):
    min = stp.minTransactions(stockName)
    min = [min[0].to_list()]
    if len(min) > 1:
        return min[0]
    else:
        return min


# return the maximum transaction for a stock.
def getMax(stockName):
    max = stp.maxTransactions(stockName)
    max = [max[0].to_list()]
    if len(max) > 1:
        return max[0]
    else:
        return max


def outputData(times):
    if type(times) == list:
        n = 1
        for time in times:
            print("Time taken for test ", n, ": ", time, "\n")
            n += 1
    else:
        print("Time taken : ", times, "\n")


def testing(stockName):
    print("Tests for ", stockName)
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


def runTests():
    N = 200
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
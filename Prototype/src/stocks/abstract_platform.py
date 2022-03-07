from abc import ABC, abstractmethod


# noinspection PyPep8Naming
# abstract class to represent a stock trading platform
class AbstractStockTradingPlatform(ABC):
    # constructor
    @abstractmethod
    def __init__(self):
        pass

    # adds transactionRecord to the set of completed transactions
    @abstractmethod
    def logTransaction(self, transactionRecord):
        pass

    # returns a list with all transactions of a given stockName,
    # sorted by increasing trade value.
    # stockName : str
    @abstractmethod
    def sortedTransactions(self, stockName):
        sortedList = []
        return sortedList

    # returns a list of transactions of a given stockName with minimum trade value
    # stockName : str
    @abstractmethod
    def minTransactions(self, stockName):
        minList = []
        return minList

    # returns a list of transactions of a given stockName with maximum trade value
    # stockName : str
    @abstractmethod
    def maxTransactions(self, stockName):
        maxList = []
        return maxList

    # returns a list of transactions of a given stockName,
    # with the largest trade value below a given thresholdValue.
    # stockName : str
    # thresholdValue : double
    @abstractmethod
    def floorTransactions(self, stockName, thresholdValue):
        floorList = []
        return floorList

    # returns a list of transactions of a given stockName,
    # with the smallest trade value above a given thresholdValue.
    # stockName : str
    # thresholdValue : double
    @abstractmethod
    def ceilingTransactions(self, stockName, thresholdValue):
        ceilingList = []
        return ceilingList

    # returns a list of transactions of a given stockName,
    # whose trade value is within the range [fromValue, toValue].
    # stockName : str
    # fromValue : double
    # toValue : double
    @abstractmethod
    def rangeTransactions(self, stockName, fromValue, toValue):
        rangeList = []
        return rangeList

import random
from datetime import timedelta
from datetime import datetime


# noinspection PyPep8Naming
class TransactionDataGenerator:
    def __init__(self):
        # noinspection SpellCheckingInspection
        self.stockNames = ["Barclays", "HSBA", "Lloyds Banking Group", "NatWest Group",
                           "Standard Chartered", "3i", "Abrdn", "Hargreaves Lansdown",
                           "London Stock Exchange Group", "Pershing Square Holdings",
                           "Schroders", "St. James's Place plc."]
        self.minTradeValue = 500.00
        self.maxTradeValue = 100000.00
        self.startDate = datetime.strptime('1/1/2022 1:00:00', '%d/%m/%Y %H:%M:%S')
        random.seed(20221603)

    # returns the name of a traded stock at random
    def getStockName(self):
        return random.choice(self.stockNames)

    # returns the trade value of a transaction at random
    def getTradeValue(self):
        return round(random.uniform(self.minTradeValue, self.maxTradeValue), 2)

    # returns a list of N randomly generated transactions,
    # where each transaction is represented as a list [stock name, price, quantity, timestamp]
    # N : int
    def generateTransactionData(self, N):
        listTransactions = [[]] * N
        listDates = [self.startDate + timedelta(seconds=3 * x) for x in range(0, N)]
        listDatesFormatted = [x.strftime('%d/%m/%Y %H:%M:%S') for x in listDates]
        for i in range(N):
            stockName = random.choice(self.stockNames)
            price = round(random.uniform(50.00, 100.00), 2)
            quantity = random.randint(10, 1000)
            listTransactions[i] = [stockName, price, quantity, listDatesFormatted[i]]
        return listTransactions

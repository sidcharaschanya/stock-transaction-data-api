import numpy as np
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt

insertions = []
times = []

# EXAMPLE : Test 1 for logTransactions: execution time when the transactions logged are in random order.
def logTransactionsTest1(num):
    timeTaken = timeit.repeat(logTransaction(TransactionDataGenerator.TransactionDataGenerator.generateTransactionData(1)), repeat=num, number=1000)
    
    #adding data for the graph
    insertions.append(num)
    times.append(timeTaken)
    return timeTaken



def testgraph():

    #y = np.array(times)
    #x = np.array(insertions) 

    #example data
    y = np.array([1,1, 1.1, 1.15, 1.17])
    x = np.array([1,10,100,1000,10000])        
    #plt.xscale("log")
    
    plt.plot(x, y, '-', color='red')
    
    plt.ylabel('Average log time')
    plt.xlabel('Number of insertions')
    
    #setting y-axis range
    plt.ylim([0.5, 1.5])
    plt.show()      

testgraph()
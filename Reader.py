'''
Reference - https://pythonspot.com/reading-csv-files-in-python/
Reads the dataset in .csv format and stores it in a list format

'''

import csv
import networkx as nx
import matplotlib.pyplot as plt

def readMyFile(filename):
    From = []
    To = []
    Miles = []
    G = nx.Graph()

    with open(filename) as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            if row[0] != 'Dead End' and row[1] != 'Dead End':
                if row[0] not in From and row[0] not in To:
                    G.add_node(row[0])
                if row[1] not in From and row[1] not in To:
                    G.add_node(row[1])
                From.append(row[0])
                To.append(row[1])
                Miles.append(row[2])
                G.add_edge(row[0], row[1], weight=row[2])
    return From, To, Miles, G



if __name__ == "__main__":

    From, To, Miles, G = readMyFile('St-Data-Original - Processed - Copy.csv')
    fig = plt.figure()
    ax = plt.axes()
    nx.draw(G, with_labels=True)
    plt.grid()
    plt.show()



    # for edge in range(len(From)):
    #     print('The distance from ' + str(From[edge]) + ' to ' + str(To[edge]) + ' is ' + str(Miles[edge]) + ' miles. \n')
    # print(From)
    # print(To)
    # print(Miles)
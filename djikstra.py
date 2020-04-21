import numpy as np
# also import our data processing .py file here
from Reader import *
import networkx as nx


def djikstra(G, start, end):
    # initialize priority queue to hold the closest path
    Priority = []
    # initialize dictionary of visited status
    visited = graphdict.fromkeys(graph, False) # make a dictionary with keys from graph and set all the values to be False
    # initialize dictionary of previous nodes
    prev = graphdict.fromkeys(graph, None)
    # initialize dictionary of accumulated distances
    dist = graphdict.fromkeys(graph, 1000) # arbitrary big number

    Priority.append(start)
    dist[start] = 0
    visited[start] = True

    while len(Priority) > 0:

        if len(Priority) == 1:
            curr = Priority.pop(0)
            visited[curr] = True
            Priority.append(G.neighbors(curr))
        else:
            for i in range(len(Priority)):
                if dist[curr] + edge(curr, i) < dist[i]:
                    # update distance
                else:
                    # keep the original distance
                Priority.pop(i) # get rid of the nodes that was analyzed

        # find all the neighbors of currently analyzing node/location
        curr_neighbors = G.neighbors(curr)

        # find the closest neighbor & add it to priority queue
        # update dictionary of visited status

        

    # if you reach dead end:
        # remove current node in priority queue and continue with next node in queue

    # if you reach the end node:
        # return the shortest path taken


if __name__ == "__main__":
    
    From, To, Miles, G = readMyFile('St-Data-Original - Processed.csv')
    djikstra(G, 'Neptune Rd', 'Boylston St')
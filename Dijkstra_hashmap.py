from data_processer import *
import numpy as np
import networkx as nx
import sys

def djikstra(G, start, end):
    '''
    Finds the optimal shortest path from a starting st. to the
    ending st. using Djikstra's Algorithm

    Input - Start: Starting St. Name
            End: Destination St. Name

    Output - Optimal Path to take

    '''
    nodelist = list(G.nodes())
    # A new dictionary to store the distances
    dist = dict()
    # A new dictionary to store the visited flag
    visited = dict()
    # A new dictionary to store the previous nodde name
    prev = dict()
    # A priority queue to hold the unprocessed nodes
    Priority = [start]

    # Initializing the dictionaries
    for street in nodelist:
        # None of the streets are visited
        visited[street] = False
        # None of the streets are mapped
        prev[street] = None
        # The initial distance to reach each
        # street is infinite miles
        dist[street] = 1000.0

    # The starting street is itself, hence it costs
    # no number of miles to reach it
    dist[start] = 0.0

    # We start on this street, so it is alreadt visited
    visited[start] = True

    while len(Priority) > 0:

        # Find the closest street to the street being
        # processed currently
        min_dist_street_i = 0
        for street in range(len(Priority)):
            if dist[Priority[street]] < dist[Priority[min_dist_street_i]]:
                min_dist_street_i = street
        
        # Remove the street being currently processed
        # from the queue 
        curr = Priority.pop(street)

        # Mark the current street as visited
        visited[curr] = True

        # Find out all the neighbors of the current street,
        # or the streets that connect to this street
        neighbors = list(G.neighbors(curr))
        temp_list = []
        for neighbor in neighbors:
            if visited[neighbor] != True:
                temp_list.append(neighbor)
        neighbors = temp_list

        # Compare the current interation distance for the street
        # with the previously stored min distance
        # Update it if it is more optimal / better
        # Add all its unvisited neighbors to the priority queue
        for unvisited_neighbor in neighbors:
            if dist[curr] + float(G.edges[curr,unvisited_neighbor]['weight']) < dist[unvisited_neighbor]:
                dist[unvisited_neighbor] = dist[curr] + float(G.edges[curr,unvisited_neighbor]['weight'])
                prev[unvisited_neighbor] = curr
            Priority.append(unvisited_neighbor)
    
    # Store the path to the end street from the start street
    end_copy = end
    directions = []
    while end_copy:
        directions.append(end_copy)
        end_copy = prev[end_copy]

    # Return the processed path
    return [ele for ele in reversed(directions)] 

if __name__ == "__main__":
  G, street_hashmap = data_to_graph()
  directions = djikstra(G, street_hashmap['Neptune Rd'], street_hashmap['Boylston St'])
  print('Directions using Djikstra Algorithm: ' + str(directions))
  print('Directions using Networkx Algorithm: ' + str(nx.shortest_path(G, street_hashmap['Neptune Rd'], street_hashmap['Boylston St'])))
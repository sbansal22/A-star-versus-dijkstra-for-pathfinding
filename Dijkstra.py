from Reader import *
import numpy as np
import networkx as nx
import sys
from datetime import datetime as dt
from datetime import timedelta as td
import timeit

'''
Thoughts on the space complexity of this program:

This program uses 3 dictionaries, and 5 lists of
variable lengths.

'''

def dijkstra(start, end):
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

    while len(Priority) > 0 and visited[end] == False:

        # Find the closest street to the street being
        # processed currently
        min_dist_street_i = 0
        for street in range(len(Priority)):
            if dist[Priority[street]] < dist[Priority[min_dist_street_i]]:
                min_dist_street_i = street
        
        # Remove the street being currently processed
        # from the queue 
        curr = Priority.pop(min_dist_street_i)

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
                if unvisited_neighbor not in Priority:
                    Priority.append(unvisited_neighbor)
    
    # Store the path to the end street from the start street
    end_copy = end
    directions = []
    while end_copy:
        directions.append(end_copy)
        end_copy = prev[end_copy]

    output_directions = [ele for ele in reversed(directions)] 
    output_distance = 0.0
    for i in range(len(output_directions)-1):
        output_distance += float(G.edges[output_directions[i],output_directions[i+1]]['weight'])

    avg_speed = 25 #mph
    current_time = dt.now()
    time = current_time + td(hours=output_distance*10/avg_speed)
    time = time.strftime("%H:%M:%S")
    current_time = current_time.strftime("%H:%M:%S")

    # Return the processed path
    return output_directions, output_distance*10, current_time, time 

if __name__ == "__main__":
  From, To, Miles, G = readMyFile('St-Data-Original - Processed.csv')
  directions, distance, current_time, time = dijkstra('Saratoga St', 'Perkins St')
  if len(directions) < 2:
    print('Directions using Dijkstra Algorithm: ' + 'Cannot find a suitable path!')
  else: 
    print('Directions using Dijkstra Algorithm: ' + str(directions))
  nx_output_directions = list(nx.shortest_path(G, 'Saratoga St', 'Perkins St'))
  print('Directions using Networkx Algorithm: ' + str(nx_output_directions))
  output_distance = 0.0
  for i in range(len(nx_output_directions)-1):
      output_distance += float(G.edges[nx_output_directions[i],nx_output_directions[i+1]]['weight'])
  print('Total distance to your destination according to Dijkstra will be about: ' + str(distance) + ' miles')
  print('Total distance to your destination according to NetworkX will be about: ' + str(output_distance*10) + ' miles')
  print('If you leave now at ' + str(current_time) + ', you will reach your destination at about: ' + str(time))
  print('Average runtime is: ' + str(timeit.timeit("dijkstra('Washington St', 'Charlotte St')", setup="from __main__ import dijkstra", number=10)/10))

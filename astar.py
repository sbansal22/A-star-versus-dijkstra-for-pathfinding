from data_processer import *
from Reader import *
import numpy as np
import networkx as nx
import sys
from datetime import datetime as dt
from datetime import timedelta as td
import timeit
from math import radians, cos, sin, asin, sqrt

# -----------------------------------------------------------------------------

def Euclidean(x, y, heuristic, traffic_level):
    '''
    Calculates the Euclidean distance between the cities x and
    y in miles, based on the input heuristic and traffic level

    Input - cities x and y
            heuristic type - euclidiean or manhatan
            traffic type - low, high
    Output - Euclidean or Manhatan Distance, adjusted with traffic

    '''

    # Geographical center of Boston, MA
    x_loc = (42.3601, -71.0589)
    y_loc = (42.3601, -71.0589)
    # Obtaining the geographical location of the streets
    for i in street_hashmap:
        if x == street_hashmap[i]:
            if i in street_locations:
                x_loc = street_locations[i]
        if y == street_hashmap[i]:
            if i in street_locations:
                y_loc = street_locations[i]
  
    # Computing the manhatan distance based on the raw latitude and longitude
    # from the geographical locations for the streets
    if heuristic == 'Manhatan':
        return abs(x_loc[0]-y_loc[0]) + abs(x_loc[1]-y_loc[1])
    
    # Computing the euclidean distance between the street nodes after 
    # converting the geographical location to coordinates on the map
    else:
        a = sin((radians(y_loc[0]-x_loc[0]))/2)**2 + cos(x_loc[0]) * cos(y_loc[0]) * sin((radians(y_loc[1]-x_loc[1]))/2)**2
        dist_eu = 3956*(2*asin(sqrt(a)))

        # Returning the heuristic, which is a combination of the actual
        # geographical distance between the nodes as well as the traffic
        # based on the traffic function returned index
        return dist_eu * traffic(x, traffic_level)

# -----------------------------------------------------------------------------
def traffic(street, traffic_level):
    '''
    Creates a traffic adjustment index based on the input traffic
    level

    low - fair traffic conditions in the Boston City area
    high - bad traffic conditions in the Boston City area
    auto - time determined traffic conditions in the Boston City area

    Input - street in consideration
            given traffic_level
    Output - traffic adjustment index

    '''
    
    # Geographical center of Boston, MA
    boston_city = (42.3601, -71.0589)
    x_loc = boston_city
    for i in street_hashmap:
        if street == street_hashmap[i]:
            if i in street_locations:
                x_loc = street_locations[i]

    # Computing the distance of the current node from the Boston City center
    a = sin((radians(boston_city[0]-x_loc[0]))/2)**2 + cos(x_loc[0]) * cos(boston_city[0]) * sin((radians(boston_city[1]-x_loc[1]))/2)**2
    dist_eu = 3956*(2*asin(sqrt(a)))

    # If the node is with one mile of the city center, impose the traffic conditions
    if dist_eu < 1:
        if traffic_level == 'low':
            return 1.5
        if traffic_level == 'high':
            return 2.5
        if traffic_level == 'auto':
            # Computes the traffic conditions based on the current time
            current_time = dt.now()
            current_time = current_time.strftime("%H:%M:%S")
            if '8:00:00' < current_time < '9:00:00' or '17:00:00' < current_time < '18:00:00':
                return 2.5
            if '7:00:00' < current_time < '8:00:00' or '9:00:00' < current_time < '10:00:00' or '16:00:00' < current_time < '17:00:00' or '18:00:00' < current_time < '19:00:00':
                return 1.5
            else:
                return 1
    else:
        return 1

def astar(start, end, heuristic, traffic_level):
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
            if dist[Priority[street]] + Euclidean(Priority[street], end, heuristic, traffic_level) < dist[Priority[min_dist_street_i]] + Euclidean(Priority[min_dist_street_i],end, heuristic, traffic_level):
                min_dist_street_i = street 
        
        # Remove the street being currently processed
        # from the queue 
        curr = Priority.pop(min_dist_street_i)

        # Mark the current street as visited
        visited[curr] = True

        if curr == end:
            # Store the path to the end street from the start street
            end_copy = end
            directions = []
            while end_copy:
                directions.append(end_copy)
                end_copy = prev[end_copy]

            # Arrange the streets to make the tour suggestions
            output_directions = [ele for ele in reversed(directions)] 

            # Intializing variables
            output_distance = 0.0
            time = 0
            avg_speed = 25 #mph

            # Computing the total distance traveled and the total time taken, based
            # on the traffic conditions
            for i in range(len(output_directions)-1):
                output_distance += float(G.edges[output_directions[i],output_directions[i+1]]['weight'])
                time += output_distance*10*traffic(output_directions[i], traffic_level)/avg_speed

            # Computes the ETA
            current_time = dt.now()
            dest_time = current_time + td(hours=time)
            dest_time = dest_time.strftime("%H:%M:%S")
            current_time = current_time.strftime("%H:%M:%S")

            # Return the processed path if we have iterated over the destination
            return output_directions, output_distance*10, time*60, dest_time, current_time

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
    
if __name__ == "__main__":
    # dist = Euclidean('Newbury Street, Boston', 'Boylston Street, Boston')
    From, To, Miles, G = readMyFile('St-Data-Original - Processed.csv')

    # read location_hashmap from pickle file
    pkl_file_geopy = open('location_hashmap.pkl', 'rb')
    street_locations = pickle.load(pkl_file_geopy)
    pkl_file_geopy.close()

    # read graph_hashmap from pickle file
    pkl_file_graph = open('graph_hashmap.pkl', 'rb')
    street_hashmap = pickle.load(pkl_file_graph)
    pkl_file_graph.close()

    # -- Euclidean
    directions, distance, time, dest_time, current_time = astar('Jeffries St', 'South St', 'Euclidean','high')
    if len(directions) < 2:
        print('Directions using A-star Algorithm: ' + 'Cannot find a suitable path!')
    else: 
        print('Directions using A-star Algorithm, Euclidean Distance: ' + str(directions))
    print('Total distance to your destination according to A-star using Euclidean Distance will be about: ' + str(distance) + ' miles')

    print('If you leave now at ' + str(current_time) + ', you will reach your destination in about ' + str(time) + ' minutes, at about: ' + str(dest_time))
    # print(timeit.timeit("astar('Washington St', 'Charlotte St', 'Euclidean')", setup="from __main__ import astar, Euclidean", number=10)/10)
    # -- Manhatan
    # directions, distance, time = astar('Washington St', 'Canterbury St', 'Manhatan')
    # if len(directions) < 2:
    #     print('Directions using A-star Algorithm: ' + 'Cannot find a suitable path!')
    # else: 
    #     print('Directions using A-star Algorithm, Manhatan Distance: ' + str(directions))
    # print('Total distance to your destination according to A-star using Manhatan Distance will be about: ' + str(distance) + ' miles')
    # print(timeit.timeit("astar('Washington St', 'Charlotte St', 'Manhatan')", setup="from __main__ import astar, Euclidean", number=10)/10)
    # print('Directions using Networkx Algorithm: ' + str(nx.astar_path(G, 'Florence St', 'Walnut Ave')))
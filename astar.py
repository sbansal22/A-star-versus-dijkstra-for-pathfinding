from data_processer import *
from Reader import *
from geopy.geocoders import Nominatim

def Euclidean(x, y):
    geolocator = Nominatim()
    x_com = x + ', Boston, Massachusetts'
    y_com = y + ', Boston, Massachusetts'
    x_loc = geolocator.geocode(x_com)
    y_loc = geolocator.geocode(y_com)
    if x_loc is None:
        return print(x_com)
    if y_loc is None:
        return print(y_com)
    return (((x_loc.latitude-y_loc.latitude)**2 + ((x_loc.longitude-y_loc.longitude)**2)))


def astar(G, start, end):
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
        if visited[end] == True:
            return [ele for ele in reversed(directions)]


        # Find the closest street to the street being
        # processed currently
        min_dist_street_i = 0
        for street in range(len(Priority)):
            if dist[Priority[street]] + Euclidean(Priority[street], end) < dist[Priority[min_dist_street_i]] + Euclidean(Priority[min_dist_street_i],end):
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
    # dist = Euclidean('Newbury Street, Boston', 'Boylston Street, Boston')
    From, To, Miles, G = readMyFile('St-Data-Original - Processed.csv')
    for i in range(len(From)):
        dist = Euclidean(From[i], To[i])

    # print(From)
    # directions = astar(G, 'Neptune Rd', 'Boylston St')
    # print('Directions using Djikstra Algorithm: ' + str(directions))
    # print('Directions using Networkx Algorithm: ' + str(nx.astar_path(G, 'Neptune Rd', 'Boylston St')))
  
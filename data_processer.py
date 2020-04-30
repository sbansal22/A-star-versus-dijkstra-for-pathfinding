import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim

# def Euclidean(x, y):
#     geolocator = Nominatim()
#     x_com = x + ', Boston, Massachusetts'
#     y_com = y + ', Boston, Massachusetts'
#     x_loc = geolocator.geocode(x_com)
#     y_loc = geolocator.geocode(y_com)
#     if x_loc is None or y_loc is None:
#         return print(x_com, y_com)
#     return (((x_loc.latitude-y_loc.latitude)**2 + ((x_loc.longitude-y_loc.longitude)**2)))

def geo(G, street_hashmap):
    long_lat = dict()
    geolocator = Nominatim(user_agent="google maps")
    # List of encoded nodes
    node_list = list(G.nodes())
    print(node_list)
    node_list_word = []
    for i in node_list:
        node_list_word.append(street_hashmap[i])
    for street in node_list:
        street_com = street_hashmap[street_hashmap((node_list[street]))] + ', Boston, Massachusetts'
        street_loc = geolocator.geocode(street_com)
        if street_com is None:
            continue
        else:
            long_lat[street] = (street_loc.latitude, street_loc.long_longitude)
    
    return long_lat

def data_to_graph():
    data = pd.read_excel(r'St-Data-Original.xlsx')
    # print(data)

    df = pd.DataFrame(data)
    st_name = df['St_name']
    from_st = df['from']
    to_st = df['to']
    miles = df['miles']


    location_map = dict()
    G = nx.Graph()


    for i in range(len(df.index)):

        # if the dictionary is empty
        if len(location_map) == 0:
            if to_st[i] == "Dead End":
                location_map[st_name[i]] = i
                G.add_node(location_map[st_name[i]])
                location_map[from_st[i]] = i+1
                G.add_node(location_map[from_st[i]])
                # print("A")
                G.add_edge(location_map[st_name[i]], location_map[from_st[i]], weight=miles[i])
            
            else:
                location_map[from_st[i]] = i
                G.add_node(location_map[from_st[i]])
                location_map[to_st[i]] = i+1
                G.add_node(location_map[to_st[i]])
                # print("B")
                G.add_edge(location_map[from_st[i]], location_map[to_st[i]], weight=miles[i])

        # if the dictionary is not empty 
        else:
            # if the to_st has a dead end, just make an edge between the st name and from
            if to_st[i] == "Dead End":
                if st_name[i] not in location_map:
                    location_map[st_name[i]] = max(location_map.values()) + 1
                    G.add_node(location_map[st_name[i]])

                if from_st[i] not in location_map:
                    location_map[from_st[i]] = max(location_map.values()) + 1
                    G.add_node(location_map[from_st[i]])

                # print("C")
                G.add_edge(location_map[st_name[i]], location_map[from_st[i]], weight=miles[i])

            # if no dead end, make edge between from_st and to_st
            else:
                if from_st[i] not in location_map:
                    location_map[from_st[i]] = max(location_map.values()) + 1
                    G.add_node(location_map[from_st[i]])

                if to_st[i] not in location_map:
                    location_map[to_st[i]] = max(location_map.values()) + 1
                    G.add_node(location_map[to_st[i]])

                # print(location_map[from_st[i]])
                # print("D")
                G.add_edge(location_map[from_st[i]], location_map[to_st[i]], weight=miles[i])
    
    return G, location_map


if __name__ == "__main__":
    G, street_hashmap = data_to_graph()
    print(street_hashmap)
    # nx.draw(G, with_labels=True, font_weight='bold')
    # plt.show()
    long_lat = geo(G, street_hashmap)
    # print(long_lat['Washington St.'])
    print(long_lat)

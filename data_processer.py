import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
import csv

# # def Euclidean(x, y):
# #     geolocator = Nominatim()
# #     x_com = x + ', Boston, Massachusetts'
# #     y_com = y + ', Boston, Massachusetts'
# #     x_loc = geolocator.geocode(x_com)
# #     y_loc = geolocator.geocode(y_com)
# #     if x_loc is None or y_loc is None:
# #         return print(x_com, y_com)
# #     return (((x_loc.latitude-y_loc.latitude)**2 + ((x_loc.longitude-y_loc.longitude)**2)))

# def geo(G, street_hashmap):
#     long_lat = dict()
#     geolocator = Nominatim(user_agent="google maps")
#     # List of encoded nodes
#     node_list = list(G.nodes())
#     node_list_word = []
#     for i in node_list:
#         node_list_word.append(street_hashmap[i])
#     for street in node_list:
#         if type(street_hashmap[street]) != type(', Boston, Massachusetts'):
#             continue
#         else: 
#             street_com = street_hashmap[street] + ', Boston, Massachusetts'
#             street_loc = geolocator.geocode(street_com)
#             if street_loc is None:
#                 continue
#             else:
#                 long_lat[street] = (street_loc.latitude, street_loc.longitude)
    
#     return long_lat


def drop_dead_ends(df):
    df.drop(df.loc[df['to']=='Dead End'].index, inplace=True)
    # df.reset_index(drop=True)


def data_to_graph():
    data = pd.read_excel(r'St-Data-Original.xlsx')
    df = pd.DataFrame(data)

    # find rows that contain 'Dead End' and delete them from df
    drop_dead_ends(df)
    from_st = df['from'].values.tolist()
    to_st = df['to'].values.tolist()
    miles = df['miles'].values.tolist()

    street_hashmap = dict()
    G = nx.Graph()

    for i in range(len(df.index)):
        # if the dictionary is empty
        if len(street_hashmap) == 0:
            street_hashmap[i] = from_st[i]
            G.add_node(i)
            street_hashmap[i+1] = to_st[i]
            G.add_node(i+1)
            G.add_edge(i, i+1, weight=miles[i])
        
        # if the dictionary is not empty 
        else:
            if from_st[i] not in street_hashmap.values():
                street_hashmap[max(street_hashmap.keys()) + 1] = from_st[i]
                node = list(street_hashmap.keys())[list(street_hashmap.values()).index(from_st[i])]
                G.add_node(node)

            if to_st[i] not in street_hashmap.values():
                street_hashmap[max(street_hashmap.keys()) + 1] = to_st[i]
                node = list(street_hashmap.keys())[list(street_hashmap.values()).index(to_st[i])]
                G.add_node(node)

            from_st_node = list(street_hashmap.keys())[list(street_hashmap.values()).index(from_st[i])]
            to_st_node = list(street_hashmap.keys())[list(street_hashmap.values()).index(to_st[i])]
            G.add_edge(from_st_node, to_st_node, weight=miles[i])
    
    return G, street_hashmap

        
if __name__ == "__main__":
    ### TEST data_to_graph() ###
    G, street_hashmap = data_to_graph()
    print(street_hashmap)
    # print(street_hashmap)
    # nx.draw(G, with_labels=True, font_weight='bold')
    # plt.show()

    # ### TEST geo() ###
    # long_lat = geo(G, street_hashmap)
    # # # print(long_lat['Washington St.'])
    # print(long_lat)
    # csv_columns = ['No','Name','Country']
    # csv_file = "Names.csv"
    # try:
    #     with open(csv_file, 'w') as csvfile:
    #         writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    #         writer.writeheader()
    #         for data in long_lat:
    #             writer.writerow(data)
    # except IOError:
    #     print("I/O error")

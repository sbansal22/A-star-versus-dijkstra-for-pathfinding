import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
import pickle


def geo(G, street_hashmap):
    long_lat = dict()
    geolocator = Nominatim(user_agent="google maps")

    # List of encoded nodes
    node_list = list(G.nodes())
    node_list_word = []

    # convert the nodes in numbers to nodes in street names
    for i in node_list:
        node_list_word.append(street_hashmap[i])
    
    # find the lat/long of all the streets
    for street in node_list:
        if type(street_hashmap[street]) != type(', Boston, Massachusetts'):
            continue
        else: 
            street_com = street_hashmap[street] + ', Boston, Massachusetts'
            street_loc = geolocator.geocode(street_com)
            if street_loc is None:
                continue
            else:
                long_lat[street] = (street_loc.latitude, street_loc.longitude)
    
    return long_lat


def drop_dead_ends(df):
    df.drop(df.loc[df['from']=='Dead End'].index, inplace=True)
    df.drop(df.loc[df['to']=='Dead End'].index, inplace=True)
    df.drop(df.loc[df['to']=='Dead end'].index, inplace=True)
    df.drop(df.loc[df['to']=='End of Street'].index, inplace=True)


def drop_empty_streets(df):
    df.drop(df.loc[df['from']=='NaN'].index, inplace=True)
    df.drop(df.loc[df['to']=='NaN'].index, inplace=True)


def drop_insignificant_miles(df):
    df.drop(df.loc[df['miles']==0].index, inplace=True)
    # print(type(df['miles'][1]))
    # pd.set_option("display.max_rows", None, "display.max_columns", None)
    # print(df)


def data_to_graph():
    data = pd.read_excel(r'St-Data-Original-Processed.xlsx')
    df = pd.DataFrame(data)

    # delete rows that contain a Dead End, NaN or miles=0
    drop_dead_ends(df)
    drop_insignificant_miles(df)
    drop_empty_streets(df)

    # convert the df columns to lists to go around the missing index numbers from deleting rows
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
    ############################
    ### TEST data_to_graph() ###
    ############################
    G, street_hashmap = data_to_graph()
    # print(street_hashmap)
    # nx.draw(G, with_labels=True, font_weight='bold')
    # plt.show()

    ##################
    ### TEST geo() ###
    ##################
    ### only run geo(G, street_hashmap) once to obtain the latitudes and longitudes of all nodes ###
    '''
    long_lat = geo(G, street_hashmap)
    '''
    
    # write street_hashmap to pickle file
    output1 = open('graph_hashmap.pkl', 'wb')
    pickle.dump(street_hashmap, output1)
    output1.close()

    # write long_lat to pickle file
    output2 = open('location_hashmap.pkl', 'wb')
    pickle.dump(long_lat, output2)
    output2.close()

    # read street_hashmap from pickle file
    pkl_file1 = open('graph_hashmap.pkl', 'rb')
    graph_hashmap = pickle.load(pkl_file1)
    pkl_file1.close()

    # read long_lat from pickle file
    pkl_file2 = open('location_hashmap.pkl', 'rb')
    lat_long = pickle.load(pkl_file2)
    pkl_file2.close()

    # print(graph_hashmap)
    # print(lat_long)
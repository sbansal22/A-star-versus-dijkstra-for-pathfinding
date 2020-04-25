import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

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
    nx.draw(G, with_labels=True, font_weight='bold')
    plt.show()
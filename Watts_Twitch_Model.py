import networkx as nx
from collections import deque
import random

"""
    This program reads from data file sample.txt, 
    using the networkx package to build the largest component graph
    builds the Watt Strogatz model
    lastly, prints the average path length and the clustering coefficient for 
    the original data, and the implemented model """

#use the sample.txt for graph data, if recalculation needed, run Watts_Twitch_Sample
file_path = "sample.txt"

#build the graph
sample_graph = nx.read_edgelist(file_path, nodetype=int)



print(f"\n Watts_Twitch_ Gamer Graph\n size: {sample_graph.number_of_nodes()}")

#Display the original graph attributes

if nx.is_connected(sample_graph):
    average_path_length = nx.average_shortest_path_length(sample_graph)
    print(f"\nAverage Path Length (Before): {average_path_length}")
else:
    print("The graph is not connected, so the average path length cannot be computed over the entire graph.")
average_clustering_coefficient = nx.average_clustering(sample_graph)
print(f"Average Clustering Coefficient (Before): {average_clustering_coefficient}")



# Define n, k, p for building the model
n = sample_graph.number_of_nodes()  
k = int(sum(dict(sample_graph.degree()).values()) / n) 

k = k * 2
if k < 4:
    k = 4
# Use a probability of 0.1
p = 0.1 



# Build the model
def custom_watts_strogatz_model(n, k, p):

    #Create the ring lattice
    G = nx.Graph()
    nodes = list(range(n))
    G.add_nodes_from(nodes)
    for i in nodes:
        for j in range(1, k // 2 + 1): #Adding neighbors to nodes
            G.add_edge(i, (i + j) % n)
            G.add_edge(i, (i - j) % n)
    
    tempEdges = list(G.edges())

    #rewire the nodes, prevants self loop and disconnction
    for i in nodes:
        neighbors = list(G.neighbors(i))
        for neighbor in neighbors:
            if i < neighbor:
                if random.random() < p:
                    while True:
                        vk = random.choice(nodes)
                        if vk != i and not G.has_edge(i, vk):
                            G.remove_edge(i, neighbor)
                            G.add_edge(i, vk)
                            
                            if nx.is_connected(G):
                                break  
                            else:
                                G.remove_edge(i, vk)
                                G.add_edge(i, neighbor)
    
    
    return G

#Calculate the Avg Path Length and the Clustering Coefficient
ws_graph_2= custom_watts_strogatz_model(n, k, p)
ws_graph_1 = ws_graph_2.to_undirected()
if nx.is_connected(ws_graph_1):
    avg_path_length = nx.average_shortest_path_length(ws_graph_1)
    print(f"\nAverage Path Length (After): {avg_path_length}")
else:
    print("The graph is not connected, so average path length cannot be calculated.")


avg_clustering_coefficient = nx.average_clustering(ws_graph_1)
print(f"Clustering Coefficient (After): {avg_clustering_coefficient}")


#Testing code
"""
ws_graph = nx.watts_strogatz_graph(n, k, p)


if nx.is_connected(ws_graph):
    average_path_length = nx.average_shortest_path_length(ws_graph)
    print(f"\nAverage Path Length (nx Watts-Strogatz): {average_path_length}")
else:
    print("The Watts-Strogatz graph is not fully connected, so the average path length cannot be calculated over the entire graph.")


average_clustering_coefficient = nx.average_clustering(ws_graph)
print(f"Clustering Coefficient (nx Watts-Strogatz): {average_clustering_coefficient}") """

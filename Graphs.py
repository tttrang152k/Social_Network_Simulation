import pandas as pd
import networkx as nx
import random
import numpy as np


# TWITCH NETWORK -------------------------------------------------------------------------------------------

'''
# Load the data - TWITCH
edges_path = 'large_twitch_edges.csv'
edges_df = pd.read_csv(edges_path)

# Initialized an undirected graph
G = nx.Graph()

# Add edges to the graph
edges = edges_df[['numeric_id_1', 'numeric_id_2']].values
G.add_edges_from(edges)

# Extract the largest connected component
largest_cc = max(nx.connected_components(G), key=len)
G_lcc = G.subgraph(largest_cc).copy()

# Write edges of the largest connected component to a text file
with open("largest_cc_edges.txt", "w") as file:
    for edge in G_lcc.edges():
        file.write(f"{edge[0]} {edge[1]}\n")
  
'''


# initialize the largest connected component graph
G_lcc = nx.Graph()

# Read edges from the text file and add them to the graph
with open("twitch_largest_component.txt", "r") as file:
    for line in file:
        # Split each line by whitespace to get the node pair
        node1, node2 = map(int, line.split())
        G_lcc.add_edge(node1, node2)

# Select 5% of nodes randomly
num_nodes = int(0.1* G_lcc.number_of_nodes())
selected_nodes = random.sample(list(G_lcc.nodes()), num_nodes)

# Subgraph with selected nodes
selected_subgraph = G_lcc.subgraph(selected_nodes).copy()
# Extract the largest connected component from this 5% subgraph
largest_cc = max(nx.connected_components(selected_subgraph), key=len)
G_lcc_10 = selected_subgraph.subgraph(largest_cc).copy()

# Network properties
print("Twitch Network Original Graph Properties: ")
# Graph's size
size = G_lcc_10.number_of_nodes()
print("Twitch's Original Graph Size:", size)
print("Twitch's Original Graph Edges:", G_lcc_10.number_of_edges())
# Average degree
avg_degree = sum(dict(G_lcc_10.degree()).values()) / size
print("Twitch's Original Graph Average Degree:", avg_degree)
# Average path length
average_path_length = nx.average_shortest_path_length(G_lcc_10)
print("Twitch's Original Graph Average Path Length:", average_path_length)
# Clustering Coefficient
clustering_coef = nx.average_clustering(G_lcc_10)
print("Twitch's Original Graph Clustering Coefficient:", clustering_coef)

# Write edges of the largest connected component to a text file
with open("twitch_extracted_lcc.txt", "w") as file:
    for edge in G_lcc_10.edges():
        file.write(f"{edge[0]} {edge[1]}\n")

'''
# AMAZON NETWORK ---------------------------------------------------------------------

# Load the data - AMAZON
edges_path_2 = 'com-amazon.ungraph.txt'

# Initialized an undirected graph
G_2 = nx.Graph()

# Read file and add edges to the graph
with open(edges_path_2, "r") as file:
    for line in file:
        # Skip header lines starting with '#'
        if line.startswith("#"):
            continue
        
        # Split the line into two node IDs
        from_node, to_node = map(int, line.split())
        
        # Add the edge to the graph
        G_2.add_edge(from_node, to_node)

print("Amazon's Original Graph Size before extracting:", G_2.number_of_nodes())

# Extract the largest connected component
largest_cc_A = max(nx.connected_components(G_2), key=len)
G_lcc_A = G_2.subgraph(largest_cc_A).copy()

# Select 30% of nodes randomly
num_nodes = int(0.2* G_lcc_A.number_of_nodes())
selected_nodes = random.sample(list(G_lcc_A.nodes()), num_nodes)

# Subgraph with selected nodes
selected_subgraph = G_lcc_A.subgraph(selected_nodes).copy()
# Extract the largest connected component from this 10% subgraph
largest_cc = max(nx.connected_components(selected_subgraph), key=len)
G_lcc_10_A = selected_subgraph.subgraph(largest_cc).copy()

# Network properties
print("Amazon Network Original Graph Properties: ")
# Graph's size
size = G_lcc_10_A.number_of_nodes()
print("Amazon's Original Graph Size:", size)
print("Amazon's Original Graph Edges:", G_lcc_10_A.number_of_edges())
# Average degree
avg_degree = sum(dict(G_lcc_10_A.degree()).values()) / size
print("Amazon's Original Graph Average Degree:", avg_degree)
# Average path length
average_path_length = nx.average_shortest_path_length(G_lcc_10_A)
print("Amazon's Original Graph Average Path Length:", average_path_length)
# Clustering Coefficient
clustering_coef = nx.average_clustering(G_lcc_10_A)
print("Amazon's Original Graph Clustering Coefficient:", clustering_coef)

# Write edges of the largest connected component to a text file
with open("amazon_10_largest_cc_edges.txt", "w") as file:
    for edge in G_lcc_10_A.edges():
        file.write(f"{edge[0]} {edge[1]}\n")

'''








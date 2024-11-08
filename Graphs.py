import pandas as pd
import networkx as nx
import random
import numpy as np

'''
# Load the data
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

# Select 10% of nodes randomly
num_nodes = int(0.1* G_lcc.number_of_nodes())
selected_nodes = random.sample(list(G_lcc.nodes()), num_nodes)

# Subgraph with selected nodes
selected_subgraph = G_lcc.subgraph(selected_nodes).copy()
# Extract the largest connected component from this 10% subgraph
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


'''
# Calculate the closeness centrality
close_centrality = nx.closeness_centrality(G_lcc_10)

# Sort nodes by closeness centrality in descending order and get the top 10
top_10_nodes = sorted(close_centrality.items(), key=lambda x: x[1], reverse=True)[:10]

# Print the top 10 nodes and their closeness centrality
print("Top 10 nodes by closeness centrality:")
for node, centrality in top_10_nodes:
    print(f"Node {node}: Closeness Centrality = {centrality:.4f}")
'''


import pandas as pd
import networkx as nx

# Initialize graph
G = nx.Graph()

# Load the edge list in chunks to manage memory usage
chunk_size = 200000  #
for chunk in pd.read_csv('/home/achoo/Desktop/Social_Network_Simulation/large_twitch_edges.csv', chunksize=chunk_size):
    # Add edges from the chunk #
    G.add_edges_from(zip(chunk['numeric_id_1'], chunk['numeric_id_2'])) #

# Extract the largest connected component (LCC)
largest_cc = max(nx.connected_components(G), key=len)
G_largest = G.subgraph(largest_cc)

num_nodes = len(G_largest)
num_edges = G_largest.number_of_edges()

# Calculate Average Degree (2 * number of edges / number of nodes)
avg_degree = 2 * num_edges / num_nodes if num_nodes > 0 else 0

# Calculate Average Path Length
avg_path_length = nx.average_shortest_path_length(G_largest) if nx.is_connected(G_largest) else float('inf')

# Calculate Clustering Coefficient
clustering_coeff = nx.average_clustering(G_largest)

# Display results
print("Largest Connected Component Size:", num_nodes)
print("Number of Edges in LCC:", num_edges)
print("Average Degree:", avg_degree)
print("Average Path Length:", avg_path_length)
print("Clustering Coefficient:", clustering_coeff)
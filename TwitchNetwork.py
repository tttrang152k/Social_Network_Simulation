import pandas as pd
import networkx as nx

# Initialize graph
G = nx.Graph()

# Load the edge list in chunks to manage memory usage
chunk_size = 250000 
for chunk in pd.read_csv('/home/achoo/Desktop/Social_Network_Simulation/large_twitch_edges.csv', chunksize=chunk_size):
    # Add edges from the chunk
    G.add_edges_from(zip(chunk['numeric_id_1'], chunk['numeric_id_2']))

# Get the total size of the network
total_nodes = len(G.nodes)
total_edges = G.number_of_edges()

# Print the size of the network
print(f"Total Number of Nodes in the Network: {total_nodes}") 
print(f"Total Number of Edges in the Network: {total_edges}")

# Extract the largest connected component (LCC)
largest_cc = max(nx.connected_components(G), key=len)
G_largest = G.subgraph(largest_cc)

# Get the number of nodes and edges in the largest connected component
num_nodes = len(G_largest)
print("Largest Connected Component Size:", num_nodes)
num_edges = G_largest.number_of_edges()
print("Number of Edges in LCC:", num_edges)

# Calculate 
avg_degree = 2 * num_edges / num_nodes if num_nodes > 0 else 0
print("Average Degree:", avg_degree)
avg_path_length = nx.average_shortest_path_length(G_largest) if nx.is_connected(G_largest) else float('inf')
print("Average Path Length:", avg_path_length)
clustering_coeff = nx.average_clustering(G_largest)
print("Clustering Coefficient:", clustering_coeff)

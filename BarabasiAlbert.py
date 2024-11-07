import random
import pandas as pd
import networkx as nx

# Initialize
BA_graph = nx.Graph()

# Read the edge list in chunks
chunk_size = 200000  
edges_df = pd.read_csv('/home/achoo/Desktop/Social_Network_Simulation/large_twitch_edges.csv', chunksize=chunk_size)

# Process the file in chunks
for chunk in edges_df:
    # Add edges from the chunk
    BA_graph.add_edges_from(zip(chunk['numeric_id_1'], chunk['numeric_id_2']))  # # Add edges in chunks

# Get nodes and edges number 
num_nodes = len(BA_graph.nodes)  
num_edges = BA_graph.number_of_edges() 

# Initialize parameters for Barabási-Albert model
m = 3  # number of edges to attach
BA_nodes = list(range(m))
BA_edges = [(i, j) for i in range(m) for j in range(i + 1, m)]

# Create list to track node connections for preferential attachment
node_connections = BA_nodes * (m - 1)

# Add new nodes one by one
for new_node in range(m, num_nodes):
    # Select m nodes based on preferential attachment
    targets = set()
    while len(targets) < m:
        chosen = random.choice(node_connections)
        targets.add(chosen)
    
    # Add edges between the new and chosen nodes
    for target in targets:
        BA_edges.append((new_node, target))
        node_connections.extend([new_node, target])

    # Include new node in the connections list
    node_connections.extend([new_node] * m)

# Create the BA graph using NetworkX
BA_graph.add_edges_from(BA_edges)

# Calculate 
avg_path_length = nx.average_shortest_path_length(BA_graph) if nx.is_connected(BA_graph) else float('inf')
clustering_coeff = nx.average_clustering(BA_graph)

print(f"Number of Nodes: {num_nodes}")
print(f"Number of Edges: {num_edges}")
print(f"Average Path Length: {avg_path_length}")
print(f"Clustering Coefficient: {clustering_coeff}")

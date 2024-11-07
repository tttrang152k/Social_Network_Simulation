import random
import pandas as pd
import networkx as nx

# Initialize
BA_graph = nx.Graph()

# Read edge list in chunks
chunk_size = 200000  
edges_df = pd.read_csv('/home/achoo/Desktop/Social_Network_Simulation/large_twitch_edges.csv', chunksize=chunk_size)

# Add edges from chunks
for chunk in edges_df:
    BA_graph.add_edges_from(zip(chunk['numeric_id_1'], chunk['numeric_id_2']))

# Get nodes and edges
num_nodes = len(BA_graph.nodes)  
num_edges = BA_graph.number_of_edges() 
print(f"Nodes: {num_nodes}")
print(f"Edges: {num_edges}")

# Initialize Barabási-Albert model
m = 3  # edges to attach

# Start with complete graph of m nodes
BA_graph = nx.complete_graph(m)
BA_edges = list(BA_graph.edges)

# Track node connections
node_connections = [node for node in range(m)] * (m - 1)

# Add new nodes
for new_node in range(m, num_nodes):
    targets = set()
    while len(targets) < m:
        chosen = random.choice(node_connections)
        targets.add(chosen)
    
    # Add edges
    for target in targets:
        BA_edges.append((new_node, target))
        node_connections.extend([new_node, target])

    node_connections.extend([new_node] * m)

# Add BA edges to graph
BA_graph.add_edges_from(BA_edges)

# Calculate average path length and clustering coefficient
avg_path_length = nx.average_shortest_path_length(BA_graph) if nx.is_connected(BA_graph) else float('inf')
print(f"Avg Path Length: {avg_path_length}")
clustering_coeff = nx.average_clustering(BA_graph)
print(f"Clustering Coefficient: {clustering_coeff}")

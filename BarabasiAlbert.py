import random
import pandas as pd
import networkx as nx

# Initialize
n0 = 3  # Initial number of nodes
t = 100  # Number of new nodes to add
BA_graph = nx.Graph()

# Start with a small complete graph with n0 nodes
BA_graph = nx.complete_graph(n0)

# Create the degree list
node_connections = [node for node in range(n0)] * (n0 - 1)

chunk_size = 200000  
edges_df = pd.read_csv('/home/achoo/Desktop/Social_Network_Simulation/large_twitch_edges.csv', chunksize=chunk_size)

# Add edges from chunks
for chunk in edges_df:
    BA_graph.add_edges_from(zip(chunk['numeric_id_1'], chunk['numeric_id_2']))

# Get the networkSize
num_nodes = len(BA_graph.nodes)  
num_edges = BA_graph.number_of_edges() 
print(f"Nodes: {num_nodes}")
print(f"Edges: {num_edges}")

# Add new nodes based on the Barabási-Albert model
for new_node in range(n0, t + n0):
    targets = set()
    while len(targets) < 1: 
        # Select a node with probability proportional to degree
        total_degree = sum(dict(BA_graph.degree()).values())
        probabilities = [BA_graph.degree(node) / total_degree for node in BA_graph.nodes]
        chosen = random.choices(list(BA_graph.nodes), weights=probabilities, k=1)[0]
        targets.add(chosen)
    
    # Add edges from the new node to selected targets
    for target in targets:
        BA_graph.add_edge(new_node, target)

# Calculate
avg_path_length = nx.average_shortest_path_length(BA_graph) if nx.is_connected(BA_graph) else float('inf')
print(f"Avg Path Length: {avg_path_length}")
clustering_coeff = nx.average_clustering(BA_graph)
print(f"Clustering Coefficient: {clustering_coeff}")

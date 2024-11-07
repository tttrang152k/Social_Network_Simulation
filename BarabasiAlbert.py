import random
import pandas as pd
import networkx as nx
from tqdm import tqdm
from multiprocessing import Pool, Manager

# Parameters
n0 = 3  # Initial nodes
t = 100  # New nodes to add
BA_graph = nx.complete_graph(n0)

# Read and add edges in chunks
chunk_size = 200000  
edges_df = pd.read_csv('/home/achoo/Desktop/Social_Network_Simulation/large_twitch_edges.csv', chunksize=chunk_size)

# Function to add edges from chunk
def add_edges(chunk):
    BA_graph.add_edges_from(zip(chunk['numeric_id_1'], chunk['numeric_id_2']))

# Add edges in parallel
with Pool() as pool:
    pool.map(add_edges, edges_df)

# Debug: Nodes and edges after adding edges
print(f"After edge addition -> Nodes: {len(BA_graph.nodes)}, Edges: {BA_graph.number_of_edges()}")

# Function to add new nodes and collect edges
def add_new_node(new_node):
    targets = set()
    while len(targets) < 1:  # Select node by degree probability
        total_degree = sum(dict(BA_graph.degree()).values())
        probabilities = [BA_graph.degree(node) / total_degree for node in BA_graph.nodes]
        chosen = random.choices(list(BA_graph.nodes), weights=probabilities, k=1)[0]
        targets.add(chosen)
    
    # Return new edges
    return [(new_node, target) for target in targets]

# Manager for shared edges list
manager = Manager()
shared_edges_list = manager.list()

# Add new nodes in parallel
with Pool() as pool:
    new_edges_list = list(tqdm(pool.imap(add_new_node, range(n0, t + n0)), total=t, desc="Adding new nodes"))

# Add new edges to graph
for new_edges in new_edges_list:
    BA_graph.add_edges_from(new_edges)

# Debug: Nodes and edges after adding nodes
print(f"After node addition -> Nodes: {len(BA_graph.nodes)}, Edges: {BA_graph.number_of_edges()}")

# Calculate metrics
with tqdm(total=2, desc="Calculating metrics", unit="metric") as pbar:
    avg_path_length = nx.average_shortest_path_length(BA_graph) if nx.is_connected(BA_graph) else float('inf')
    print(f"Avg Path Length: {avg_path_length}")
    pbar.update(1)

    clustering_coeff = nx.average_clustering(BA_graph)
    print(f"Clustering Coefficient: {clustering_coeff}")
    pbar.update(1)

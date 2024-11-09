import random
import networkx as nx
import pandas as pd

# Add a node with preferential attachment
def add_node_with_edges(G, node_id, expectedConnections):
    targets = set()
    total_degree = sum(G.degree(node) for node in G.nodes)
    
    while len(targets) < expectedConnections:
        probabilities = [G.degree(node) / total_degree for node in G.nodes]
        chosen = random.choices(list(G.nodes), weights=probabilities, k=1)[0]
        targets.add(chosen)

    for target in targets:
        G.add_edge(node_id, target)

# Add multiple nodes with preferential attachment
def barabasiAlbertSimple(G, expectedConnections, numNewNodes):
    currentNodeID = max(G.nodes()) + 1
    for i in range(numNewNodes):
        add_node_with_edges(G, currentNodeID + i, expectedConnections)
    return G

# Load graph (updated file path)
file_path = '/home/achoo/Desktop/Social_Network_Simulation/large_twitch_edges.csv'

# Assuming the CSV has columns 'numeric_id_1' and 'numeric_id_2' for edges
edges_df = pd.read_csv(file_path)  # Read the CSV file
G = nx.from_pandas_edgelist(edges_df, source='numeric_id_1', target='numeric_id_2')

print("Twitch_BarabassiAlbert:")
print("Original Graph - Nodes:", G.number_of_nodes(), "Edges:", G.number_of_edges())

# Extract the largest connected component (LCC) of the original graph
lcc_original = max(nx.connected_components(G), key=len)
G_lcc_original = G.subgraph(lcc_original).copy()
print("Largest Connected Component of Original Graph - Nodes:", G_lcc_original.number_of_nodes(), "Edges:", G_lcc_original.number_of_edges())

# Sample 5% of nodes from the LCC (updated percentage)
sample_fraction = 0.05  # Changed from 20% to 5%
selected_nodes = set(random.sample(list(G_lcc_original.nodes()), int(len(G_lcc_original) * sample_fraction)))
subgraph = G_lcc_original.subgraph(selected_nodes)
print("Subgraph (5% of LCC) - Nodes:", subgraph.number_of_nodes(), "Edges:", subgraph.number_of_edges())

# Extract largest connected component of the sampled subgraph
lcc = max(nx.connected_components(subgraph), key=len)
G_lcc = subgraph.subgraph(lcc).copy()

# Calculate initial metrics
avg_path_length_before = nx.average_shortest_path_length(G_lcc) if nx.is_connected(G_lcc) else float('inf')
avg_degree = sum(dict(G_lcc.degree()).values()) / G_lcc.number_of_nodes()
avg_degree_rounded = round(sum(dict(G_lcc.degree()).values()) / G_lcc.number_of_nodes())  # Rounded to the nearest whole number
clustering_coeff_before = nx.average_clustering(G_lcc)

print("\nLargest Connected Component (20% of LCC) - Nodes:", G_lcc.number_of_nodes(), "Edges:", G_lcc.number_of_edges())
print("Average Degree (Before):", avg_degree)
print("Average Path Length (Before):", avg_path_length_before)
print("Clustering Coefficient (Before):", clustering_coeff_before)

# Use initial average degree as expected connections for new nodes
expected_connections = int(avg_degree_rounded)
new_nodes = 1000  # Updated new nodes to 1000

# Add new nodes with preferential attachment
G_lcc = barabasiAlbertSimple(G_lcc, expected_connections, new_nodes)

# Calculate updated metrics
avg_path_length_after = nx.average_shortest_path_length(G_lcc) if nx.is_connected(G_lcc) else float('inf')
clustering_coeff_after = nx.average_clustering(G_lcc)

print("\nUpdated Graph - Nodes:", G_lcc.number_of_nodes(), "Edges:", G_lcc.number_of_edges())
print("Average Path Length (After):", avg_path_length_after)
print("Clustering Coefficient (After):", clustering_coeff_after)
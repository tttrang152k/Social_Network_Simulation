import random
import networkx as nx
import pandas as pd

# Add a node with preferential attachment
def add_node_with_edges(G, node_id, expectedConnections):
    targets = set()
    totalDegree = sum(G.degree(node) for node in G.nodes)
    
    while len(targets) < expectedConnections:
        probabilities = [G.degree(node) / totalDegree for node in G.nodes]
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

# Load graph
file_path = '/home/achoo/Desktop/Social_Network_Simulation/com-amazon.ungraph.txt'
G = nx.read_edgelist(file_path, nodetype=int)
print("Amazon_BarabassiAlbert:")
print("Original Graph - Nodes:", G.number_of_nodes(), "Edges:", G.number_of_edges())

# Extract the largest connected component (LCC) of the original graph
lcc_original = max(nx.connected_components(G), key=len)
G_lcc_original = G.subgraph(lcc_original).copy()
print("Largest Connected Component of Original Graph - Nodes:", G_lcc_original.number_of_nodes(), "Edges:", G_lcc_original.number_of_edges())

# Sample 20% of nodes from the LCC
sampleFraction = 0.20
selectedNodes = set(random.sample(list(G_lcc_original.nodes()), int(len(G_lcc_original) * sampleFraction)))
subgraph = G_lcc_original.subgraph(selectedNodes)
print("Subgraph (20% of LCC) - Nodes:", subgraph.number_of_nodes(), "Edges:", subgraph.number_of_edges())

# Extract largest connected component of the sampled subgraph
lcc = max(nx.connected_components(subgraph), key=len)
G_lcc = subgraph.subgraph(lcc).copy()

# Calculate initial metrics
avg_path_length_before = nx.average_shortest_path_length(G_lcc) if nx.is_connected(G_lcc) else float('inf')
avgDegree = sum(dict(G_lcc.degree()).values()) / G_lcc.number_of_nodes()
avgDegree_rounded = round(sum(dict(G_lcc.degree()).values()) / G_lcc.number_of_nodes())  # Rounded to the nearest whole number
clustering_coeff_before = nx.average_clustering(G_lcc)

print("\nLargest Connected Component (20% of LCC) - Nodes:", G_lcc.number_of_nodes(), "Edges:", G_lcc.number_of_edges())
print("Average Degree (Before):", avgDegree)
print("Average Path Length (Before):", avg_path_length_before)
print("Clustering Coefficient (Before):", clustering_coeff_before)

# Use initial average degree as expected connections for new nodes
expectedConnections = int(avgDegree_rounded)
expectedConnections = 5000

# Add new nodes with preferential attachment
G_lcc = barabasiAlbertSimple(G_lcc, expectedConnections, expectedConnections)

# Calculate updated metrics
avg_path_length_after = nx.average_shortest_path_length(G_lcc) if nx.is_connected(G_lcc) else float('inf')
clustering_coeff_after = nx.average_clustering(G_lcc)

print("\nUpdated Graph - Nodes:", G_lcc.number_of_nodes(), "Edges:", G_lcc.number_of_edges())
print("Average Path Length (After):", avg_path_length_after)
print("Clustering Coefficient (After):", clustering_coeff_after)

import networkx as nx
import random
import matplotlib.pyplot as plt
import scipy as sp

def barabasi_albert_model(G_0, num_new_nodes, expected_connections):

    G = G_0.copy()

    current_node_id = max(G.nodes()) + 1    #   Advoid duplicates with the nodes in orginial graph
    total_degree = sum(G.degree(node) for node in G.nodes())

    for new_node in range (current_node_id, current_node_id + num_new_nodes):
        #   Get the degree's probabilities for each existing node
        probabilities = [G.degree(node) / total_degree for node in G.nodes()]

        #   Choose unique expected edges based on preferential attachment probability
        targets = set()
        while len(targets) < expected_connections:
            chosen_nodes = random.choices(list(G.nodes()), weights=probabilities, k=1)[0]
            targets.add(chosen_nodes)

        #   Add new node with expected connections to chosen nodes
        for node in targets:
            G.add_edge(new_node, node)

    return G

'''
# AMAZON -----------------------------------------------------------------------
# Define the parameters for the BA model
G = nx.Graph()

# Read edges from the text file and add them to the graph
with open("amazon_10_largest_cc_edges.txt", "r") as file:
    for line in file:
        # Split each line by whitespace to get the node pair
        node1, node2 = map(int, line.split())
        G.add_edge(node1, node2)

num_new_nodes = 1000
expected_edges = 5

expanded_G = barabasi_albert_model(G, num_new_nodes, expected_edges)


# Graph's size
size = expanded_G.number_of_nodes()
print("Amazon's Barabasi Graph Size:", size)
print("Amazon's Barabasi Graph Edges:", expanded_G.number_of_edges())
# Average degree
avg_degree = sum(dict(expanded_G.degree()).values()) / size
print("Amazon's Barabasi Graph Average Degree:", avg_degree)
# Average path length
average_path_length = nx.average_shortest_path_length(expanded_G)
print("Amazon's Barabasi Graph Average Path Length:", average_path_length)
# Clustering Coefficient
clustering_coef = nx.average_clustering(expanded_G)
print("Amazon's Barabasi Graph Clustering Coefficient:", clustering_coef)


# Plot the final network
plt.figure(figsize=(10, 10))
nx.draw(expanded_G, with_labels=True, node_color='lightgreen', edge_color='gray', node_size=500)
plt.title("Barabási-Albert Scale-Free Network")
plt.show()
'''

# TWITCH ----------------------------------------------------------------------------------------
# Define the parameters for the BA model
G = nx.Graph()

# Read edges from the text file and add them to the graph
with open("twitch_extracted_lcc.txt", "r") as file:
    for line in file:
        # Split each line by whitespace to get the node pair
        node1, node2 = map(int, line.split())
        G.add_edge(node1, node2)

num_new_nodes = 1000
expected_edges = 5

expanded_G = barabasi_albert_model(G, num_new_nodes, expected_edges)


# Graph's size
size = expanded_G.number_of_nodes()
print("Twitch's Barabasi Graph Size:", size)
print("Twitch's Barabasi Graph Edges:", expanded_G.number_of_edges())
# Average degree
avg_degree = sum(dict(expanded_G.degree()).values()) / size
print("Twitch's Barabasi Graph Average Degree:", avg_degree)
# Average path length
average_path_length = nx.average_shortest_path_length(expanded_G)
print("Twitch's Barabasi Graph Average Path Length:", average_path_length)
# Clustering Coefficient
clustering_coef = nx.average_clustering(expanded_G)
print("Twitch's Barabasi Graph Clustering Coefficient:", clustering_coef)

'''
# Plot the final network
plt.figure(figsize=(10, 10))
nx.draw(expanded_G, with_labels=True, node_color='lightgreen', edge_color='gray', node_size=500)
plt.title("Barabási-Albert Scale-Free Network")
plt.show()

'''
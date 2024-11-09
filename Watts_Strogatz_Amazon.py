import networkx as nx 
import gzip 
import random 
import matplotlib.pyplot as plt

#Some file manipuilation stuff 
# Open and read the file as a single string
# with gzip.open("com-amazon.ungraph.txt.gz", "rt", encoding="utf-8") as f:
#     data = f.read()

# # Write the data to a new .txt file
# with open("output.txt", "w", encoding="utf-8") as output_file:
#     output_file.write(data)



# Draw the graph (optional, if you want to visualize it)
# nx.draw(T, with_labels=True)
# plt.show()


G = nx.Graph() 
G = nx.read_edgelist("com-amazon.ungraph.txt", create_using=nx. DiGraph(), nodetype=int)
G_ud = G.to_undirected()
N_ori, K_ori = G_ud.order(), G_ud.size() 
print("Original Graph - Nodes: ", N_ori, " Edges: ", K_ori)


#Extract largest component 
connected_components = list(nx.connected_components(G_ud))
largest_comp = max(connected_components, key=len)
G_largest_comp= G_ud.subgraph(largest_comp)

#Extract 10% from largest component 
sorted_nodes = sorted(G_largest_comp.degree, key=lambda x: x[1], reverse=True)
top_10_percent_count = int(len(sorted_nodes) * 0.025)
top_10_percent_nodes = [node for node, degree in sorted_nodes[:top_10_percent_count]]
G_10_subgraph_largest_comp = G_largest_comp.subgraph(top_10_percent_nodes)
G_10_subgraph_largest_comp_ud = G_10_subgraph_largest_comp.to_undirected()

#Extract largest component from 10%
connected_components = list(nx.connected_components(G_10_subgraph_largest_comp_ud))
largest_comp_10 = max(connected_components, key=len)
G_largest_comp_10 = G_10_subgraph_largest_comp_ud.subgraph(largest_comp_10)


##Calculation for the original network of the 10% most connected nodes from the largest component
N, K = G_largest_comp_10.order(), G_largest_comp_10.size() 
avg_deg = 2*float(K) / N
avg_path_lenghts = []


#Cluster Coefficient of all nodes 
clust_coefficients = nx.clustering(G_largest_comp_10)
avg_clust = sum(clust_coefficients.values()) / len(clust_coefficients)
avg_path_length = nx.average_shortest_path_length(G_largest_comp_10) if nx.is_connected(G_largest_comp_10) else float('inf')


print("\n\n10 percent of Largest Component- Nodes: ", N, " Edges: ", K)
print("Average degree: ", avg_deg)
print("Average Path Length: ", avg_path_length)
print("Average Clustering Coefficient: ", avg_clust)


#Watts-Strogatz model
beta = 0.05

#regular ring lattice 
G_Watts = nx.Graph()
# Add nodes to the graph
G_Watts.add_nodes_from(range(N))

k = int(avg_deg) // 2 

# Connect each node to half_k neighbors on each side
for node in range(N):
    for j in range(1, k + 1):
        neighbor1 = (node + j) % N
        neighbor2 = (node - j) % N
        G_Watts.add_edge(node, neighbor1)
        G_Watts.add_edge(node, neighbor2)


edges = list(G_Watts.edges())
nodes = list(range(N))

#Rewirring
for i in G_Watts.nodes():
        neighbors = list(G_Watts.neighbors(i))
        for neighbor in neighbors:
            if i < neighbor:
                if random.random() < beta:
                    while True:
                        vk = random.choice(nodes)
                        if vk != i and not G_Watts.has_edge(i, vk):
                            G_Watts.remove_edge(i, neighbor)
                            G_Watts.add_edge(i, vk)
                            
                            # Check connectivity
                            if nx.is_connected(G_Watts):
                                break 
                            else:
                                # If disconnected, revert the change
                                G_Watts.remove_edge(i, vk)
                                G_Watts.add_edge(i, neighbor)



#Calculation for Watts Network
N_Watts, K_Watts = G_Watts.order(), G_Watts.number_of_edges() 
avg_deg_Watts = sum(dict(G_Watts.degree()).values()) / G_Watts.number_of_nodes()
avg_path_lenghts_Watts = []


G_ud_Watts = G_Watts.to_undirected()
avg_clust_Watts = nx.average_clustering(G_Watts)
for C in (G_ud_Watts.subgraph(c).copy() for c in nx.connected_components(G_ud_Watts)):
    avg_path_lenghts_Watts.append(nx.average_shortest_path_length(C))

print("\n\nWatts-Strogatz Network - Nodes: ", N_Watts, " Edges: ", K_Watts)
print("Average degree: ", avg_deg_Watts)
print("Average path length: ", sum(avg_path_lenghts_Watts)/nx.number_connected_components(G_ud_Watts))
print("AVG Clustering Coefficient: ", avg_clust_Watts)


# print("\n\nNetworkx")
# T = nx.watts_strogatz_graph(N, int(avg_deg), beta)
# print("Average degree: ", 2*float(T.size())/T.order())
# print("AVG CLUSTER: ", nx.average_clustering(T))
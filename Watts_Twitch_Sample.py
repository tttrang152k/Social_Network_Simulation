import csv
import networkx as nx
import random

# Create an empty graph
originalData = nx.Graph()

#Read from the Twitch dataset source file and build the graph
with open("large_twitch_edges.csv", "r") as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  

    for row in csv_reader:        
        from_node = int(row[0]) 
        to_node = int(row[1])
        originalData.add_edge(from_node, to_node)

#Print Attributes
undirectedData = originalData.to_undirected() 
print(f"Original Graph - Nodes: {undirectedData.number_of_nodes()} Edges: {undirectedData.number_of_edges()}")
#connectedComp = nx.connected_components(undirectedData)
#largestCC = max(connectedComp, key=len)  
#largestComp = undirectedData.subgraph(largestCC).copy()

# Randomly xtract 10% of nodes
lcNodes = undirectedData.number_of_nodes()
sampleSize = int(0.1*lcNodes)

sampleNodes = random.sample(list(undirectedData.nodes()),sampleSize)

sampleGraph = undirectedData.subgraph(sampleNodes).copy()
#Find the max connected component
tempSample = max(nx.connected_components(sampleGraph), key = len)
realSample = sampleGraph.subgraph(tempSample).copy()
print(f"Largest Component (for 10% Subgraph) - Nodes: {realSample.number_of_nodes()} Edges: {realSample.number_of_edges()}")

# Define the output file path
output_file_path = "sample.txt"

# Open the file and write the edges
with open(output_file_path, "w") as file:
    for edge in realSample.edges():
        # Write each edge as a pair of nodes, separated by a tab (adjust if necessary)
        file.write(f"{edge[0]}\t{edge[1]}\n")

print(f"Sampled graph saved to {output_file_path}")





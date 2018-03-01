import networkx as nx # To use graph features
import numpy as np # To input the adjacency matrix as a 2-D array
import matplotlib.pyplot as plt # To display a graphical view of the graph
import datetime as dt # To keep the run-time of each algorithm

G = nx.Graph() # Create graph G
# Inputting the adjacency matrix
#----------------------control input: nXn & symmetric & connected/ make animation of coloring/ keep time/ change colors
adjacency_matrix = np.array([[0,1,1,1],
                             [1,0,1,0],
                             [1,1,0,0],
                             [1,0,0,0]])
#or also:
#adjacency_matrix = np.array(input(" Please enter the adjacency matrix as a 2-D array: "))

G = nx.from_numpy_array(adjacency_matrix) # Creating the graph given the adjacency matrix

# Displaying the graph
pos = nx.circular_layout(G) # Set position layout
nx.draw(G, pos, edge_color = 'red')
#print([n for n in G[0]]) #adjacency list
# nx.draw_networkx_nodes(G, pos, nodelist=G.nodes(), node_color='b')
# nx.draw_networkx_edges(G, pos, edgelist = G.edges(), edge_color = 'r')
plt.axis('off') # To prevent showing X-Y axes
plt.show()

# BackTracking Graph Coloring algorithm

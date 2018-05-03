import networkx as nx # To use graph features
import numpy as np # To input the adjacency matrix as a 2-D array
import matplotlib.pyplot as plt # To display a graphical view of the graph
import datetime as dt # To keep the run-time of each algorithm

G = nx.Graph() # Create graph G ------------------------ Do we need this line?
# Inputting the adjacency matrix
#----------------------control input: nXn & symmetric & connected/ make animation of coloring/ keep time/ change colors
g1_adj = [[0,1,1,1,0],
         [1,0,1,0,1],
         [1,1,0,1,1],
         [1,0,1,0,0],
         [0,1,1,0,0]]

g2_adj = [[0,1,1,1],
          [1,0,1,0],
          [1,1,0,0],
          [1,0,0,0]]

g3_adj = [[0,1,1,1,1],
          [1,0,1,1,1],
          [1,1,0,1,1],
          [1,1,1,0,1],
          [1,1,1,1,0]]
adjacency_matrix = np.array(g3_adj)
#or also:
#adjacency_matrix = np.array(input(" Please enter the adjacency matrix as a 2-D array: "))

G = nx.from_numpy_array(adjacency_matrix) # Creating the graph given the adjacency matrix
G.add_nodes_from(G.nodes(), color='red') # Initializing graph with red-colored nodes

# BackTracking Graph Coloring algorithm
# The default color is red
color_list = ['blue', 'pink', 'green', 'purple', 'khaki', 'orange', 'yellow']

# Coloring Function
def assignColor(node_):

    safe_color_list = color_list.copy()

    for nd in G.adj[node_].keys():
       if G.node[nd]['color'] != 'red':
            safe_color_list.remove(G.node[nd]['color'])
    G.node[node_]['color'] = safe_color_list[0]
    for nd_ in G.adj[node_].keys():
        if G.node[nd_]['color'] == 'red':
            assignColor(nd_)

# main call
node_colors = []
for nd in G.nodes():
    if G.node[nd]['color'] == 'red':
        assignColor(nd)
    node_colors.append(G.node[nd]['color'])

pos = nx.circular_layout(G) # Set position layout
nx.draw(G, pos, node_color=node_colors)
plt.axis('off') # To prevent showing X-Y axes
plt.show() # Displays the graph
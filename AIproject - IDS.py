import networkx as nx # To use graph features
import numpy as np # To input the adjacency matrix as a 2-D array
import matplotlib.pyplot as plt # To display a graphical view of the graph
import datetime as dt # To keep the run-time of each algorithm
import random
import copy

G = nx.Graph() # Create graph G ------------------------ Do we need this line?
# Inputting the adjacency matrix

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

g4_adj = [[0,1,1,1],
          [1,0,1,1],
          [1,1,0,1],
          [1,1,1,0]]
adjacency_matrix = np.array(g3_adj)
G = nx.from_numpy_array(adjacency_matrix) # Creating the graph given the adjacency matrix

#---------------- function maximumDegree ----------------
# This function receives a graph as input, and returns the maximum degree of a node in the graph (Known
# as Big-Delta).
def maximum_degree(graph_):
    degrees = [deg for name,deg in graph_.degree]
    return max(degrees)

#---------------- function generate_random_color ----------------
# This function receives an integer, and generates that much random colors.
def generate_random_color(number_of_colors):
    list_of_colors = []
    for i in range(number_of_colors):
        r = lambda: random.randint(0,255)
        color = '#%02X%02X%02X' % (r(),r(),r())
        while color == '#FF0000':
            color = '#%02X%02X%02X' % (r(), r(), r())
        list_of_colors.append(color)
    return list_of_colors

# -------------------- function assign_color --------------------
def assign_color(graph__, node):
    colors_copy = copy.deepcopy(color_list)
    for neig in graph__.adj[node].keys():
        color_ = graph__.nodes[neig]['color']
        if (color_ != "#FF0000") and (color_ in colors_copy):
            colors_copy.remove(color_)
    return colors_copy[0]

# -------------------- function is_colored --------------------
# This function receives a graph as input, and returns True if every node in the graph is colored,
# and False otherwise.
def is_colored(graph_):
    answer = True
    for node in graph_.nodes:
        if graph_.nodes[node]['color'] == "#FF0000":
            answer = False
    return answer

#---------------- function countColoring ----------------
def countColoring(graph_):
    color_of_nodes = []
    for node in graph_.nodes:
        if graph_.nodes[node]['color'] not in color_of_nodes:
            color_of_nodes.append(graph_.nodes[node]['color'])
    return len(color_of_nodes)

# -------------------- dls --------------------
def dls(graph_, limit):
    if limit >= 0:
        for node in graph_.nodes:
            if graph_.nodes[node]['color'] == "#FF0000":
                graph_.nodes[node]['color'] = assign_color(graph_, node)
                limit -= 1
            for neig in graph_.adj[node].keys():
                if graph_.nodes[neig]['color'] == '#FF0000':
                    dls(graph_, limit)
    return graph_

# -------------------- function ids --------------------
# This function receives a graph as input, and performs Iterative Deepening Depth-First Search on it.
def ids(graph):
    d = nx.number_of_nodes(graph)
    # for node in graph.nodes:
    #     print(graph.nodes[node]['color'])
    for depth in range(d):
        # dls(graph, 0, depth)
        if is_colored(graph):
            print(countColoring(graph))
            break
        else:
            dls(graph, depth)
        # if is_colored(result):
        #     print(countColoring(graph))

# ==================== main call ====================
color_list = generate_random_color(maximum_degree(G)+1)
G.add_nodes_from(G.nodes(), color="#FF0000")
ids(G)

node_colors = []
for node in G.nodes():
    node_colors.append(G.nodes[node]['color'])

pos = nx.circular_layout(G) # Set position layout
nx.draw(G, pos, node_color=node_colors)
plt.axis('off') # To prevent showing X-Y axes
plt.show() # Displays the graph

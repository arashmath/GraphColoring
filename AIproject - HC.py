#---------------- Importing necessary modules ----------------
import networkx as nx # To use graph features
import numpy as np # To input the adjacency matrix as a 2-D array
import matplotlib.pyplot as plt # To display a graphical view of the graph
import datetime as dt # To keep the run-time of each algorithm
import random
import copy

### CHECK ALL COMMENTS, ADD MORE COMMENTS OF NEEDED

#---------------- Initialization ----------------
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

adjacency_matrix = np.array(g1_adj)
G = nx.from_numpy_array(adjacency_matrix) # Creating the graph given the adjacency matrix

#---------------- function maximum_degree ----------------
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
        while (color == '#FF0000') or (color in list_of_colors):
            color = '#%02X%02X%02X' % (r(), r(), r())
        list_of_colors.append(color)
    return list_of_colors

#---------------- function assign_color ----------------
# This function receives a graph and a list of colors as input, and assigns a valid color in the list to the
# nodes of the graph and returns the result graph.
def assign_color(graph_, colors):

    for node in graph_.nodes:
        graph_.nodes[node]['color'] = '#FF0000'
    for node in graph_.nodes:
        adjacent_colors = []
        for adj_node in graph_.adj[node].keys():
            adjacent_colors.append(graph_.nodes[adj_node]['color'])
        while (graph_.nodes[node]['color'] == '#FF0000') or (graph_.nodes[node]['color'] in adjacent_colors):
            graph_.nodes[node]['color'] = random.choice(colors)
    return graph_

#---------------- function initial_state_generator ----------------
# This function receives a graph as input, and returns a graph in a random-color state, so that
# we can run Simulated Annealing algorithm on that graph. It also returns the list of colors to be used in HC.
def initial_state_generator(graph):

    max_deg = maximum_degree(graph)
    color_list = generate_random_color(max_deg+1)
    graph = assign_color(graph, color_list)
    return graph, color_list

#---------------- function loss_function ----------------
def print_graph(graph_):
    for node in graph_.nodes:
        print(str(node) +" , "+ graph_.nodes[node]['color'])
    print("\n")

#---------------- function loss_function ----------------
# This function calculates the loss-function for each state
# Loss value is defined to be the number of colors used for coloring a graph
def loss_function(graph_):

    used_colors = []
    for node in graph_.nodes():
        if graph_.nodes[node]['color'] not in used_colors:
            used_colors.append(graph_.nodes[node]['color'])
    return len(used_colors)


#---------------- function choose_next_state ----------------
# This function receives a dictionary of nodes (zzz) and chooses one node randomly among them all.
def choose_next_state(graph_, nodes_dict):

    (node, color) = random.choice(list(nodes_dict.keys()))

    graph_.nodes[node]['color'] = color
    graph_ = hill_climbing(graph_, color_list)
    return graph_

#---------------- function hill_climbing ----------------
# This function receives a graph and a list of colors as input and performs the Hill Climbing
# search algorithm on that graph for the purpose of coloring its nodes
def hill_climbing(graph, colors):

    candidate_colored_nodes = {}
    current_loss = copy.deepcopy(loss_function(graph))

    for node in graph.nodes():
        node_initial_color = copy.deepcopy(graph.nodes[node]['color'])
        adjacent_colors = []
        for adj_node in graph.adj[node]:
            adjacent_colors.append(graph.nodes[adj_node]['color'])

        for color in colors: # check all the colors and compare with each other
            if color not in set(adjacent_colors):
                graph.nodes[node]['color'] = color
                if (loss_function(graph) <= current_loss):
                    candidate_colored_nodes[(node, color)] = loss_function(graph)
        graph.nodes[node]['color'] = node_initial_color

    if bool(candidate_colored_nodes):
        return graph
    else:
        graph = choose_next_state(graph, candidate_colored_nodes)
        return graph

#================ main call ================
G, color_list = initial_state_generator(G)
restart_times = 5
best_found = copy.deepcopy(G)

for i in range(restart_times):
    current_graph = copy.deepcopy(G)
    current_graph = hill_climbing(current_graph, color_list)
    current_loss = copy.deepcopy(loss_function(current_graph))
    print('\033[1;36m' + "Iteration: " + str(i) + "    loss: " + str(current_loss) + '\033[0m')
    print_graph(current_graph)
    if (loss_function(current_graph) < loss_function(best_found)):
        best_found = copy.deepcopy(current_graph)

#---------------- printing results ----------------
node_colors = []
for node in best_found.nodes():
    node_colors.append(best_found.nodes[node]['color'])
print('\033[1;32m' + "Chromatic number is: " + str(len(set(node_colors))) + '\033[1;32m')

pos = nx.circular_layout(best_found) # Set position layout
nx.draw(best_found, pos, node_color=node_colors)
plt.axis('off') # To prevent showing X-Y axes
plt.show() # Displays the graph
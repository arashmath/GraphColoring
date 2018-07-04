#---------------- Importing necessary modules ----------------
import networkx as nx # To use graph features
import numpy as np # To input the adjacency matrix as a 2-D array
import matplotlib.pyplot as plt # To display a graphical view of the graph
from math import e
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
# This function calculates the loss-function for each state
# Loss value is defined to be the number of colors used for coloring a graph
def loss_function(graph_):
    used_colors = []
    for node in graph_.nodes():
        if graph_.nodes[node]['color'] not in used_colors:
            used_colors.append(graph_.nodes[node]['color'])
    return len(used_colors)

#---------------- function assign_probability ----------------
# This function receives a graph, a node of that graph, a color and current temperature
# and returns the probability of accepting the next state.
# Next state is the input graph with colored input node with input color
def assign_probability(graph_, node_, color_, t):
    current_value = (-1) * loss_function(graph_)
    graph_.nodes[node_]['color'] = color_
    next_value = (-1) * loss_function(graph_)
    changed_energy_level = next_value - current_value
    if (changed_energy_level >= 0):
        return 1
    else:
        return e**(changed_energy_level/t)

#---------------- function choose_next_state ----------------
# This function receives a dictionary of nodes (zzz) and chooses one node randomly among them all.
def choose_next_state(graph_, nodes_dict):
    (node, color) = random.choice(list(nodes_dict.keys()))
    if nodes_dict[(node, color)] == 1:
        graph_.nodes[node]['color'] = color
        return graph_
        ### change graph to new state
    else:
        ### generate random number an choose an interval, therefore next state
        rand = random.random()
        if (rand<=nodes_dict[(node, color)]):
            graph_.nodes[node]['color'] = color
            return graph_
        else:
            return graph_

#---------------- function simulated_annealing ----------------
def simulated_annealing(graph, colors, t):
    if t == 0:
        return graph

    candidate_colored_nodes = {}

    for node in graph.nodes():
        node_initial_color = copy.deepcopy(graph.nodes[node]['color'])
        adjacent_colors = []
        for adj_node in graph.adj[node]:
            adjacent_colors.append(graph.nodes[adj_node]['color'])

        for color in colors: # check all the colors and compare with each other
            if color not in set(adjacent_colors):
                candidate_colored_nodes[(node, color)] = assign_probability(graph, node, color, t)

        graph.nodes[node]['color'] = node_initial_color
    graph = choose_next_state(graph, candidate_colored_nodes)
    t -= 1
    graph = simulated_annealing(graph, color_list, t)
    return graph
#================ main call ================
#######################################################   !! TEST EACH FUNCTION SEPARATELY FIRST !!

G, color_list = initial_state_generator(G)
temperature = 50
G = simulated_annealing(G, color_list, temperature)

node_colors = []
for node in G.nodes():
    node_colors.append(G.nodes[node]['color'])
print(len(set(node_colors)))

pos = nx.circular_layout(G) # Set position layout
nx.draw(G, pos, node_color=node_colors)
plt.axis('off') # To prevent showing X-Y axes
plt.show() # Displays the graph
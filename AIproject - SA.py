#---------------- Importing needed modules ----------------
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

adjacency_matrix = np.array(g4_adj)
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
# This function receives a graph and a list of colors as input, and assigns the colors in the list to the
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
# we can run hill-climbing algorithm on that graph. It also returns the list of colors to be used in HC.
def initial_state_generator(graph):
    max_deg = maximum_degree(graph)
    color_list = generate_random_color(max_deg+1)
    graph = assign_color(graph, color_list)
    return graph, color_list

#---------------- function count_coloring ----------------
def count_coloring(graph_):
    color_of_nodes = []
    for node in graph_.nodes:
        if graph_.nodes[node]['color'] not in color_of_nodes:
            color_of_nodes.append(graph_.nodes[node]['color'])
    return len(color_of_nodes)

#---------------- function loss_function ----------------
# This function calculates the loss-function for each state
def loss_function(graph_):
    used_colors = []
    for node in graph_.nodes():
        if graph_.nodes[node]['color'] not in used_colors:
            used_colors.append(graph_.nodes[node]['color'])
    return len(used_colors)

#---------------- function print_graph ----------------
def print_graph(graph_):
    for node in graph_.nodes:
        print(str(node) +" , "+ graph_.nodes[node]['color'])
    print("\n")

#---------------- function assign_probability ----------------
def assign_probability(graph_, node_, color_, t):
    current_value = (-1) * count_coloring(graph_)
    graph_.nodes[node_]['color'] = color_
    next_value = (-1) * count_coloring(graph_)
    changed_energy_level = next_value - current_value
    if (changed_energy_level >= 0):
        return 1
    else:
        return e**(changed_energy_level/t)

#---------------- function choose_next_state ----------------
def choose_next_state(nodes_dict):
    acceptance_dict = {}
    (node, color) = random.choice(list(nodes_dict.keys()))
    if nodes_dict[(node, color)] == 1:
        return (node, color)
        ### change graph to new state
    else:
        ### generate random number an choose an interval, therefore next state
        acceptance_dict[(node, color)] = nodes_dict[(node, color)]
        sum_of_probabilities = sum(acceptance_dict.values())
        for val in acceptance_dict.values():
            val /= sum_of_probabilities
        temp_sum = 0
        for nd_cl in acceptance_dict.keys():
            acceptance_dict[nd_cl] = (temp_sum, acceptance_dict[nd_cl]+temp_sum) ### might have an error
            temp_sum = copy.deepcopy(acceptance_dict[nd_cl])

        while(True):
            for key, val in acceptance_dict.items():
                rand = random.random()
                if ((rand >= val[0]) and (rand <= val[1])):
                    return key

#---------------- function Simulated_annealing ----------------
def simulated_annealing(graph, colors, t):
    if t == 0:
        return graph

    # print_graph(graph)
    candidate_colored_nodes = {}

    for node in graph.nodes():
        node_initial_color = copy.deepcopy(graph.nodes[node]['color'])
        adjacent_colors = []
        for adj_node in graph.adj[node]:
            if graph.nodes[adj_node]['color'] not in adjacent_colors:
                adjacent_colors.append(graph.nodes[adj_node]['color'])

        for color in colors: # check all the colors and compare with each other
            if color not in adjacent_colors:
                candidate_colored_nodes[(node, color)] = assign_probability(graph, node, color, t)

        graph.nodes[node]['color'] = node_initial_color
    nd, cl = choose_next_state(candidate_colored_nodes)
    graph.nodes[nd]['color'] = cl
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
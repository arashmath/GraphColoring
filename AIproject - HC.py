#---------------- Importing needed modules ----------------
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
        while color == '#FF0000':
            color = '#%02X%02X%02X' % (r(), r(), r())
        list_of_colors.append(color)
    return list_of_colors

#---------------- function assignColor ----------------
# This function receives a graph and a list of colors as input, and assigns the colors in the list to the
# nodes of the graph and returns the result graph.
def assignColor(graph_, colors):

    for node in graph_.nodes:
        graph_.nodes[node]['color'] = '#FF0000'
    for node in graph_.nodes:
        adjacent_colors = []
        for adj_node in graph_.adj[node]:
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
    graph = assignColor(graph, color_list)
    return graph, color_list

#---------------- function countColoring ----------------
def countColoring(graph_):
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

#---------------- function select_appropriate_node ----------------
# This function
def select_appropriate_node(candidate_dict):
    loss_values = []
    for node, val in candidate_dict.items():
        loss_values.append(val[1])
    for node, val in candidate_dict.items():
        if val[1] == min(loss_values): # Line to change, if we wanted to choose "random-choice" approach
            return node, val[0]

#---------------- function print_graph ----------------
def print_graph(graph_):
    for node in graph_.nodes:
        print(str(node) +" , "+ graph_.nodes[node]['color'])
    print("\n")
#---------------- function hillClimbing ----------------
def hill_climbing(graph, colors):

    candidate_colored_nodes = {}
    control_variable = False

    for node in graph.nodes():
        node_initial_color = copy.deepcopy(graph.nodes[node]['color'])
        min_loss = copy.deepcopy(loss_function(graph))
        candidate_colored_nodes[node] = (node_initial_color, loss_function(graph))
        adjacent_colors = []
        for adj_node in graph.adj[node]:
            if graph.nodes[adj_node]['color'] not in adjacent_colors:
                adjacent_colors.append(graph.nodes[adj_node]['color'])

        for color in colors: # check all the colors and compare with each other
            if color not in adjacent_colors:
                graph.nodes[node]['color'] = color
                loss = loss_function(graph)
                print(loss)
                if loss < min_loss:
                    control_variable = True
                    candidate_colored_nodes[node] = (color, loss)
                    min_loss = copy.deepcopy(loss)
                #if loss == min_loss:
                    #for i in range(10):
                    # control_variable = True
                    #     hill climbing ??
        graph.nodes[node]['color'] = node_initial_color
        print("next node \n")
    print(candidate_colored_nodes)
    if control_variable == False:
        print("Algorithm Termination")
        print("Coloring number found is: " + str(countColoring(graph)))

        node_colors = []
        for node in graph.nodes():
            node_colors.append(graph.nodes[node]['color'])
        pos = nx.circular_layout(G)  # Set position layout
        nx.draw(G, pos, node_color = node_colors)
        plt.axis('off')  # To prevent showing X-Y axes
        plt.show()  # Displays the graph
        return
    # select the first node with minimum loss
    # imply the changes to the graph  --> change the selected node's color
    else:
        nd, col = select_appropriate_node(candidate_colored_nodes)
        print(select_appropriate_node(candidate_colored_nodes))
        graph.nodes[nd]['color'] = col
        hill_climbing(graph, colors)

#================ main call ================
#######################################################   !! TEST EACH FUNCTION SEPARATELY FIRST !!

G, color_list = initial_state_generator(G)
hill_climbing(G, color_list)

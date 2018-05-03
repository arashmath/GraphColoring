#---------------- Importing needed modules ----------------
import networkx as nx # To use graph features
import numpy as np # To input the adjacency matrix as a 2-D array
import matplotlib.pyplot as plt # To display a graphical view of the graph
import datetime as dt # To keep the run-time of each algorithm
import random

###############  CORRECT GRAPH SYNTAX MESS-UPS! ###################

#---------------- Initialization ----------------
G = nx.Graph() # Create graph G

g3_adj = [[0,1,1,1,1],
          [1,0,1,1,1],
          [1,1,0,1,1],
          [1,1,1,0,1],
          [1,1,1,1,0]]

adjacency_matrix = np.array(g3_adj)
G = nx.from_numpy_array(adjacency_matrix) # Creating the graph given the adjacency matrix

#---------------- function initialStateGenerator ----------------
# def initialStateGenerator(graph, max_deg):
#     for node in graph.nodes:
#         graph.nodes(node)['color'] = random.random() * max_deg

#---------------- function generateRandomColor ----------------
def generateRandomColor(number_of_colors):
    list_of_colors = []
    for i in range(number_of_colors):
        r = lambda: random.randint(0,255)
        color = '#%02X%02X%02X' % (r(),r(),r())
        list_of_colors.append(color)
    return list_of_colors

#---------------- function assignColor ----------------
# def assignColor(graph, colors):
#     #color_list = generateRandomColor(max_deg)
#     for node in graph.nodes:
#         graph.nodes[node]['color'] = colors[graph.nodes[node]['color']]

#---------------- function traverseGraph ----------------
#def traverseGraph():

#---------------- function countConflictingPairs ----------------
def countConflictingPairs(graph):
    n = graph.number_of_nodes()
    list_of_conflicts = np.zeros((n,n))
    for node in graph.nodes:
        for neighbour in graph.adj[node].keys():
            if graph.nodes[node]['color'] == graph.nodes[neighbour]['color']:
                list_of_conflicts[node][neighbour] = list_of_conflicts[node][neighbour] + 1 # combine half matrix
    return list_of_conflicts

#---------------- function aggregateConflicts ----------------
def aggregateConflicts(conflict_list):
    length = len(conflict_list)
    aggregate_conflict_list = np.zeros(length)
    for i in range(length):
        aggregate_conflict_list[i] = sum(conflict_list[i])
    return aggregate_conflict_list
#---------------- function makeConflictsMatrix ----------------
# def makeConflictsMatrix(graph_):
#     m = len(graph_.nodes)
#     conflicts_matrix = np.zeros((m, m))
#     for node in graph_.nodes:
#         for neighbour in graph_.adj[node]:
#             conflicts_matrix[node][neighbour] = countConflicts(graph_, )

#---------------- function checkConflicts ----------------
def countConflicts(graph__, node_):
    number_of_conflicts = 0
    for neighbour in graph__.adj(node_):
        if graph__.nodes[node_]['color'] == graph__.nodes[neighbour]['color']:
            number_of_conflicts = number_of_conflicts + 1
    return number_of_conflicts

#----------------function countColoring ----------------
def countColoring(graph_):
    color_of_nodes = []
    for node in graph_.nodes:
        if graph_.node[node]['color'] not in color_of_nodes:
            color_of_nodes.append(graph_.nodes[node]['color'])
    return len(color_of_nodes)

#---------------- function hillClimbing ----------------
def hillClimbing(graph, colors):
    for node in graph.nodes:
        print(graph.nodes[node]['color'])

    conflicts = countConflictingPairs(graph)
    aggregate_conflicts = aggregateConflicts(conflicts)
    minimum_conflicts = np.min(aggregate_conflicts)       #####index problems might occur
    minimum_conflicts_index = np.argmin(aggregate_conflicts)

    for node in graph.nodes(minimum_conflicts_index):
        node_initial_color = graph.nodes[node]['color']
        for color in colors:
            # check all the colors and compare with each other
            graph.nodes[node]['color'] = color
            new_conflicts = countConflicts(graph, node)
            if new_conflicts < minimum_conflicts:# got any better # update conflicts
                # aggregate_conflicts[node] = new_conflicts
                hillClimbing(graph, colors) # make efficient to update only the latest edited conflict
            else:                               # maybe add another argument to the function?
                graph.nodes[node]['color'] = node_initial_color
        print(" Change on node:", node,"\n total conflicts:", sum(aggregate_conflicts), "\n Coloring number:", countColoring(graph), "\n\n")

#---------------- function maximumDegree ----------------
def maximumDegree(graph):
    degrees = [deg for name,deg in graph.degree]
    return max(degrees)

#================ main call ================
max_deg = maximumDegree(G)
# initialStateGenerator(G, maxDeg)
color_list = generateRandomColor(max_deg+1)
#print(color_list)
# assignColor(G, color_list)
G.add_nodes_from(G.nodes(), node_color = color_list) # Initializing graph with red-colored nodes

hillClimbing(G, color_list)
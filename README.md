### [To be updated]
This is the code for my **Graph Coloring Exploration Project**, which was my Artificial Intelligence course project at *Amirkabir University of Technology* (aka *AUT* or *Tehran Polytechnic*). My implementations not only return the adjacancy matrix of the graph, but also visualize the colored result graph.
### Goal
The goal of this project was to implement and compare some of the famous Heuristic algorithms and AI approaches to the Graph Coloring problem. 
### [NEW!]
I wrote a Python script to extract the adjacency matrix of graphs in _.col_ and _.col.b_ format from [here](https://mat.tepper.cmu.edu/COLOR/instances/instances.tar).

### A brief description of the files:
* AIproject - Back Tracking-DFS.py: An exact approach to solve the graph coloring problem using a back tracking algorithm
* AIproject - HC.py: An approximation of the coloring using Hill Climbing algorithm
* AIproject - IDS.py: An implementation using the Iterative-deepening search algorithm
* AIproject - Learning Model (2).ipynb: A naive approach to predict the chromatic number using linear regression
* AIproject - SA.py: An approximation of the coloring using Simulated Annealing algorithm
* data.csv: Contains the adjacancy matrix of some famous graphs from [here](https://mat.tepper.cmu.edu/COLOR/instances/instances.tar)
* extract_adj_matrix.py: The code that extracted the adjacancy matrix of graphs from _.col_ and _.col.b_ format into a _.csv_ file

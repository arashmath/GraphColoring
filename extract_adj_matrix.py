import numpy as np
import pandas as pd
import os

all_adj_matrices = []

def make_adj_matrix(file):
    raw = open(file, 'r')
    temp_list = []
    max_dim = 0
    for line in raw:
        if line.startswith('e'):
            (_, node1, node2) = line.split(' ')
            node1, node2 = int(node1), int(node2)
            temp_list.append((node1, node2))
            max_dim = max(max_dim, max(node1, node2))

    adj_mtrx = np.zeros((max_dim, max_dim))
    for i in temp_list:
        adj_mtrx[i[0]-1, i[1]-1] = 1
    return adj_mtrx


for file in os.listdir():
    if file.endswith('.col'):
        name = file.strip('.col')
        all_adj_matrices.append((name, make_adj_matrix(file)))

# make a dataframe out of it
data = pd.DataFrame(all_adj_matrices)
data.to_csv('data.csv')



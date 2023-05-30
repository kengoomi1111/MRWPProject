import networkx as nx
import random
from itertools import groupby
import matplotlib.pyplot as plt

X = 50
Y = 0.5
G = nx.Graph()
death = []

threshold = 20

G.add_node(0)
G.add_node(1)
G.add_edge(0, 1)
List = [0, 1]

for n in range(1, X-1):
    G.add_node(n+1)
    for m in List:
        if m in death:
            continue
        if len(G[m]) < threshold:
            prob = G.degree(m)/(2 * len(G.edges()))
            if random.random() < prob:
                G.add_edge(n+1, m)
        else:
            death.append(m)
    List.append(n+1)

print('For ' + str(X) + ' nodes, ' + str(threshold) + ' as threshold')

print('number of death = ' + str(len(death)))

# nx.write_gexf(G, 'scale_free_node'+str(X)+'threshold'+str(threshold)+'.gexf')

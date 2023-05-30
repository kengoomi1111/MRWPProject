import networkx as nx
import random
from itertools import groupby
import matplotlib.pyplot as plt

X = 100
Y = 0.5
G = nx.DiGraph()
death = []

threshold = 3

G.add_node(0)
G.add_node(1)
G.add_edge(0, 1)
List = [0, 1]

for n in range(1, X-1):
    G.add_node(n+1)
    for m in List:
        if m in death:
            continue
        if len(G[m]) - len(list(G.predecessors(m))) < threshold:
            if random.random() < Y:
                G.add_edge(n+1, m)
            if random.random() < Y:
                G.add_edge(m, n+1)
        else:
            # print('node ' + str(m) + 'dies.')
            death.append(m)
    List.append(n+1)

print('For ' + str(X) + ' nodes, ' + str(threshold) + ' as threshold')

print('number of death = ' + str(len(death)))

# nx.write_gexf(G, 'binomial_node'+str(X)+'threshold'+str(threshold)+'.gexf')

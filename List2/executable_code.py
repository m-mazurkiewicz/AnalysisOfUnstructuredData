from bs4 import BeautifulSoup
from urllib.request import urlopen
import networkx as nx
import itertools
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
import re

url = "http://prac.im.pwr.wroc.pl/~hugo/HSC/Publications/Publications"
html = urlopen(url)
soup = BeautifulSoup(html.read(), 'lxml')

groups = soup.find_all('group')
for i in range(len(groups)):
    if groups[i].find_all('name')[0].get_text() == 'Research papers':
        authors = groups[i].find_all('authors')

for i in range(len(authors)):
    new_list = []
    for j in range(len(authors[i])):
        if authors[i].find_all('author')[j].get('hsc')=='yes':
            author = authors[i].find_all('author')[j].get_text()
            author = re.sub(' ', '', author)
            author = re.sub('Wylomanska', 'Wyłomańska', author)
            author = re.sub('Loch-Olszewska', 'Loch', author)
            author = re.sub('Zak', 'Żak', author)
            new_list.append(author)
    authors[i] = new_list

edges = []
for i in range(len(authors)):
    for pair in itertools.combinations(authors[i],2):
        edges.append(tuple(sorted(pair)))
edges_dict = Counter(edges)

nodes_dict = dict()
for i in range(len(authors)):
    nodes_dict = Counter(authors[i]) + Counter(nodes_dict)

G = nx.Graph()
G.add_nodes_from(list(nodes_dict.keys()))
list_of_edges = list(edges_dict.items())
for i in range(len(edges_dict)):
    edge = list_of_edges[i]
    G.add_edge(edge[0][0], edge[0][1], weight = edge[1])
weights = [G[u][v]['weight'] for u,v in G.edges]

plt.figure(figsize=(50,50))
node_pos=nx.get_node_attributes(G,'pos')
edge_labels = nx.get_edge_attributes(G,'weight')
pos = nx.kamada_kawai_layout(G)
#pos = nx.random_layout(G)
nx.draw_networkx_edges(G, pos, width = weights)
nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels)
nx.draw_networkx_nodes(G, pos, node_size = np.multiply(list(nodes_dict.values()),100))
nx.draw_networkx_labels(G, pos)
plt.savefig('network_of_authors.png')

plt.show()
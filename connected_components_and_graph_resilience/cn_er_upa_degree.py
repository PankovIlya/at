import connected_components as cc
import sys
sys.path.append('../degree_distributions_for_graphs')
import ddg
import upa as mupa
import math, random
import matplotlib.pyplot as plt

nr_graph = cc.load_graph(cc.net_url)
nr_degre_distr = ddg.degree_distribution(nr_graph)
graph = nr_degre_distr

cnt = len(nr_graph)
mx = round(sum([x*1.0*graph[x] for x in graph])/sum(graph.values()))
p = round(mx*1.0/cnt, 3)
print mx, sum(graph.values())

er_ugraph = ddg.make_complete_ugraph_p(cnt, mx*1.0/cnt)
er_degre_distr = ddg.degree_distribution(er_ugraph)

upa_graph = mupa.upa(int(mx), cnt) 
upa_degre_distr = ddg.degree_distribution(upa_graph)

graph2 = er_degre_distr
graph3 = upa_degre_distr

plt.loglog(graph.keys(), graph.values(), "og",  label='Computer Network')
plt.loglog(graph2.keys(), graph2.values(), "ob",  label='ER')
plt.loglog(graph3.keys(), graph3.values(), "or",  label='UPA')

title = 'loglog degree distribution, n = {0} , p = {1}, m = {2}'.format(cnt, p, int(mx))
plt.title(title)
plt.xlabel('degree, quantity')
plt.ylabel('distribution')

plt.legend(loc='upper right')
plt.show()

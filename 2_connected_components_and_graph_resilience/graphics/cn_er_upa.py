import sys
sys.path.append('../../_degree_distributions_for_graphs')
sys.path.append('../../2_connected_components_and_graph_resilience')

import ddg
import connected_components as cc
import data.load_data_cc as ldc
import upa as gupa
import random
import matplotlib.pyplot as plt


cn_graph = ldc.load_graph(ldc.GRAPH)
cn_degre_distr = ddg.degree_distribution(cn_graph)
norm_degre_distr = ddg.norm_degree_distribution(cn_degre_distr)
graph = norm_degre_distr

cnt = len(cn_graph)
mx = sum(x*graph[x] for x in graph)
p = round(mx*1.0/cnt, 3)
print mx, p, sum(graph.values())


cn_graph = cc.renum_keys(cn_graph)
atack = cn_graph.keys()
random.shuffle(atack)

# computer network
cn_cr =cc.compute_resilience(cn_graph, atack)

# ER 
er_ugraph = ddg.make_complete_ugraph_p(cnt, p)
er_cr =cc.compute_resilience(er_ugraph, atack)

#upa 
upa_graph = gupa.upa(int(mx), cnt) #
upa_cr =cc.compute_resilience(upa_graph, atack)

count = [x for x in xrange(len(atack))]

plt.plot(count, cn_cr[1:], "r", label='Computer Network')
plt.plot(count, er_cr[1:], "b",  label='ER')
plt.plot(count, upa_cr[1:], "g", label='UPA')

title = 'Resilience of the graph, with random choice, n = {0} , p = {1}, m = {2}'.format(cnt, p, int(mx))
plt.title(title)

plt.xlabel('number of removed nodes')
plt.ylabel('the size of the largest connected component')

plt.legend(loc='upper right')
plt.grid(True)
plt.show()



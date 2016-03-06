import sys
sys.path.append('../../_degree_distributions_for_graphs')
sys.path.append('../../2_connected_components_and_graph_resilience')

import ddg
import data.load_data_cc as ldc
import upa as gupa
import matplotlib.pyplot as plt



cn_graph = ldc.load_graph(ldc.GRAPH)
cn_degre_distr = ddg.degree_distribution(cn_graph)
norm_degre_distr = ddg.norm_degree_distribution(cn_degre_distr)
graph = norm_degre_distr

cnt = len(cn_graph)
mx = sum([x*graph[x] for x in graph])
p = round(mx*1.0/cnt, 3)
print mx, p, sum(graph.values())

er_ugraph = ddg.make_complete_ugraph_p(cnt, mx*1.0/cnt)
er_degre_distr = ddg.degree_distribution(er_ugraph)

upa_graph = gupa.upa(int(mx), cnt)
upa_degre_distr = ddg.degree_distribution(upa_graph)

graph = cn_degre_distr
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

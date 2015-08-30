import sys
sys.path.append("../../degree_distributions_for_graphs")
import load_data as ld
import math, ddg, dpa
import matplotlib.pyplot as plt

graph = dpa.dpa(13,28000)
dpa_in_degre_distrib = ddg.in_degree_distribution(graph)
dpa_norm_degree_distr = ddg.norm_degree_distribution(dpa_in_degre_distrib)

citation_graph = ld.load_graph(ld.CITATION)
in_degre_distrib = ddg.in_degree_distribution(citation_graph)
norm_degree_distr = ddg.norm_degree_distribution(in_degre_distrib)

_, dpa =  plt.subplots()
cit = dpa.twinx()

dpa.loglog(dpa_norm_degree_distr.keys(), dpa_norm_degree_distr.values(), 'bo')
cit.loglog(norm_degree_distr.keys(), norm_degree_distr.values(), 'ro')

plt.title('loglog plot of DPA & Citation normalized in-degree distribution, n = 28000, m = 13')
dpa.set_xlabel('in-degree', color = 'k')
dpa.set_ylabel('dpa normalized distribution', color = 'b')
cit.set_ylabel('citation normalized distribution', color='r')
plt.show()



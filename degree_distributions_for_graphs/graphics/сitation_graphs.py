import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import sys
sys.path.append("../../degree_distributions_for_graphs")
import load_data as ld
import math, ddg


citation_graph = ld.load_graph(ld.CITATION)

in_degre_distrib = ddg.in_degree_distribution(citation_graph)
norm_degree_distr = ddg.norm_degree_distribution(in_degre_distrib)

graph = norm_degree_distr

mx = sum([x*graph[x] for x in graph])
sigma = (sum([((x - mx)**2)*graph[x] for x in graph]))**0.5
print mx, sigma

plt.loglog(norm_degree_distr.keys(), norm_degree_distr.values(), 'o')

plt.title('loglog plot of Citation normalized in-degree distribution')
plt.xlabel('in-degree')
plt.ylabel('normalized distribution')
plt.show()



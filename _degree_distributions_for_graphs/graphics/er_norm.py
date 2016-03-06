"""
generating random graphs ER and in the in-degree distribution
"""

import math
import matplotlib.pyplot as plt
import sys
sys.path.append("../../_degree_distributions_for_graphs")
import ddg

p = 0.2 #probability directed edge from i to j
n = 5000 # count nodes


er_graph = ddg.make_complete_graph_p(n, p)

in_degre_distrib = ddg.in_degree_distribution(er_graph)

norm_in_degre_distr = ddg.norm_degree_distribution(in_degre_distrib)

graph = norm_in_degre_distr

mx = sum(x*graph[x] for x in graph)
sigma = sum(((x - mx)**2)*graph[x] for x in graph)**0.5
print mx, sigma


plt.plot([math.log10(x) for x in norm_in_degre_distr],
         [math.log10(norm_in_degre_distr[x]) for x in norm_in_degre_distr], 'o')
plt.title('loglog plot of ER normalized in-degree distribution, n = {}, p = {}'.format(n , p))
plt.xlabel('in-degree')
plt.ylabel('normalized distribution')

plt.show()



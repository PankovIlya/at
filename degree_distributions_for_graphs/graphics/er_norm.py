import math
import matplotlib.pyplot as plt
import sys
sys.path.append("../../degree_distributions_for_graphs")
import ddg

print "begin ..."
er_graph = ddg.make_complete_graph_p(10000, 0.2)
sys.stdout.flush()
print "make graph complete"
in_degre_distrib = ddg.in_degree_distribution(er_graph)
print "in degre distribution complete"
norm_in_degre_distr = ddg.norm_degree_distribution(in_degre_distrib)
print "normalized distribution complete"

graph = norm_in_degre_distr

mx = sum([x*graph[x] for x in graph])
sigma = (sum([((x - mx)**2)*graph[x] for x in graph]))**0.5
print mx, sigma


plt.plot([math.log10(x) for x in norm_in_degre_distr],
         [math.log10(norm_in_degre_distr[x]) for x in norm_in_degre_distr], 'o')
plt.title('loglog plot of ER normalized in-degree distribution, n = 10000, p = 0.2')
plt.xlabel('in-degree')
plt.ylabel('normalized distribution')

plt.show()



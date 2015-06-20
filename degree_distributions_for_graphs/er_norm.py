import ddg, math
import matplotlib.pyplot as plt

er_graph = ddg.make_complete_graph_p(500, 1)
in_degre_distrib = ddg.in_degree_distribution(er_graph)
norm_in_degre_distr = ddg.norm_degree_distribution(in_degre_distrib)
graph = in_degre_distrib
mx = sum([x*1.0*graph[x] for x in graph])/sum(graph.values())
sigma = (sum([(x - mx)**2 for x in graph])/len(graph.values()))**0.5
print mx, sigma, len(er_graph)

#plt.plot(norm_in_degre_distr.keys(), norm_in_degre_distr.values(), "o")
plt.plot([math.log10(x) for x in norm_in_degre_distr],
         [math.log10(norm_in_degre_distr[x]) for x in norm_in_degre_distr], 'o')
plt.title('loglog plot of ER normalized in-degree distribution, n = 10000, p = 0.2')
plt.xlabel('in-degree')
plt.ylabel('normalized distribution')

plt.show()



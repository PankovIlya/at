import connected_components as cc
import sys
sys.path.append('/home/ilya/Documents/at/degree_distributions_for_graphs')
import ddg
import upa as mupa
import math, random
import matplotlib.pyplot as plt

def renum_keys(ugraph):
    ord_graph = {}
    idx = 0 
    res_graph = {}    
    for node in ugraph:
        ord_graph[node] = idx
        idx += 1

    for hnode in ugraph:
        idx = ord_graph[hnode]
        res_graph.setdefault(idx, set([]))
        for cnode in ugraph[hnode]:
            res_graph[idx].add(ord_graph[cnode])

    return res_graph

#tg = {20:set([30,40]), 30:set([20,40]), 40:set([20,30,50]), 50:set([40])}
#print renum_keys(tg)


nr_graph = cc.load_graph(cc.net_url)
nr_graph = renum_keys(nr_graph)

cnt = len(nr_graph)
atack = nr_graph.keys()
random.shuffle(atack)
nr_cr =cc.compute_resilience(nr_graph, atack)

er_ugraph = ddg.make_complete_ugraph_p(cnt, 0.005)
er_cr =cc.compute_resilience(er_ugraph, atack)

upa_graph = mupa.upa(5, cnt)
upa_cr =cc.compute_resilience(upa_graph, atack)

upa_degre_distr = ddg.degree_distribution(upa_graph)
er_degre_distr = ddg.degree_distribution(er_ugraph)
nr_degre_distr = ddg.degree_distribution(nr_graph)

print nr_degre_distr
print upa_degre_distr
print er_degre_distr



graph = nr_degre_distr
graph2 = er_degre_distr
graph3 = upa_degre_distr

mx = sum([x*1.0*graph[x] for x in graph])/sum(graph.values())
sigma = (sum([(x - mx)**2 for x in graph])/len(graph))**0.5
print mx, sigma, len(graph)

count = [x for x in xrange(len(atack))]

##plt.loglog(graph3.keys(), graph3.values(), "or",  label='upa')
##plt.loglog(graph2.keys(), graph2.values(), "ob",  label='er')
##plt.loglog(graph.keys(), graph.values(), "og",  label='cn')
##plt.title('loglog degree distribution, n = 1000, p = 0.006, m = 5')
##plt.xlabel('degree')
##plt.ylabel('distribution')

plt.plot(count, er_cr[1:], "b",  label='ER')
plt.plot(count, nr_cr[1:], "g", label='computer network')
plt.plot(count, upa_cr[1:], "r", label='UPA')

plt.xlabel('number of removed nodes')
plt.ylabel('the size of the largest connected component')

plt.legend(loc='upper right')
plt.show()

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

nr_graph = cc.load_graph(cc.net_url)
nr_degre_distr = ddg.degree_distribution(nr_graph)
graph = nr_degre_distr

cnt = len(nr_graph)
mx = round(sum([x*1.0*graph[x] for x in graph])/sum(graph.values()))
p = round(mx*1.0/cnt, 3)
print mx, p, sum(graph.values())


nr_graph = renum_keys(nr_graph)

atack = nr_graph.keys()

random.shuffle(atack)

nr_cr =cc.compute_resilience(nr_graph, atack)

er_ugraph = ddg.make_complete_ugraph_p(cnt, p)
er_cr =cc.compute_resilience(er_ugraph, atack)

upa_graph = mupa.upa(int(mx), cnt)
upa_cr =cc.compute_resilience(upa_graph, atack)

count = [x for x in xrange(len(atack))]

plt.plot(count, nr_cr[1:], "g", label='Computer Network')
plt.plot(count, er_cr[1:], "b",  label='ER')
plt.plot(count, upa_cr[1:], "r", label='UPA')

title = 'Resilience of the computer network, er, upa, n = {0} , p = {1}, m = {2}'.format(cnt, p, int(mx))
plt.title(title)

plt.xlabel('number of removed nodes')
plt.ylabel('the size of the largest connected component')

plt.legend(loc='upper right')
plt.show()

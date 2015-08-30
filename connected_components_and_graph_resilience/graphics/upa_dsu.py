import math, random, time
import matplotlib.pyplot as plt
import sys
sys.path.append('../../degree_distributions_for_graphs')
import ddg
sys.path.append('../../connected_components_and_graph_resilience')
import connected_components as cc
import load_data_cc as ldc
import upa as mupa


def time_run(ugraf, foo, lst):
    ts = time.time()
    foo(ugraf, lst)
    return time.time() - ts
    
cntx = []
cry = []
crsy = []

n, m, k = 1000, 5001, 750

for cnt in xrange(n, m, k):
    sys.stdout.flush()
    print "\r processing {0}%".format(cnt*100/m),
    cntx += [cnt]
    upa_graph = mupa.upa(5, cnt)
    atack = [x for x in upa_graph]
    cry += [time_run(upa_graph, cc.compute_resilience, atack)]
    crsy += [time_run(upa_graph, cc.compute_resilience_simple, atack)]

plt.plot(cntx, cry, "g", label='with dsu, O(n+m)')
plt.plot(cntx, crsy, "r", label='simple, O(n(n+m))')

title = 'Compute Resilience (number of removed nodes = n)'
plt.title(title)

plt.xlabel('number of nodes')
plt.ylabel('running time, sec')

plt.legend(loc='upper right')
plt.show()






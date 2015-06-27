import connected_components as cc
import sys
sys.path.append('/home/ilya/Documents/at/degree_distributions_for_graphs')
import ddg
import upa as mupa
import math, random, time
import matplotlib.pyplot as plt

def time_run(ugraf, foo, lst):
    ts = time.time()
    foo(ugraf, lst)
    return time.time() - ts
    
cntx = []
cry = []
crsy = []

for cnt in xrange(1000,8000,1500):
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






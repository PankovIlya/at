"""
  compare two method compute resilience, simple vs with dsu
"""
import sys
sys.path.append('../../_degree_distributions_for_graphs')
sys.path.append('../../2_connected_components_and_graph_resilience')

import time
import connected_components as cc
import upa as mupa
import matplotlib.pyplot as plt


def tcomlete(cnt, all):
    sys.stdout.flush()
    print "\r processing {0}%".format(round(cnt*100.0/all)),


def time_run(ugraf, foo, lst):
    ts = time.time()
    foo(ugraf, lst)
    return time.time() - ts


def test():
    cntx, cry, crsy = [], [],  []
    n, m, k = 1000, 3001, 500 # count min, max nodes, step

    for cnt in xrange(n, m, k):
        cntx.append(cnt)
        upa_graph = mupa.upa(5, cnt)
        atack = [x for x in upa_graph]
        cry.append(time_run(upa_graph, cc.compute_resilience, atack))
        crsy.append(time_run(upa_graph, cc.compute_resilience_simple, atack))
        tcomlete(cnt, m)

    return cntx, cry, crsy


cnt, dsu_ra, ra = test()



plt.plot(cnt, dsu_ra, "g", label='with dsu, O(n+m)')
plt.plot(cnt, ra, "r", label='simple, O(n(n+m))')

title = 'Compute Resilience (number of removed nodes = n)'
plt.title(title)

plt.xlabel('number of nodes')
plt.ylabel('running time, sec')

plt.legend(loc='upper right')
plt.show()






import connected_components as cc
import sys
sys.path.append('/home/ilya/Documents/at/degree_distributions_for_graphs')
import ddg
import upa as mupa
import math, random
import matplotlib.pyplot as plt

upa_graph = mupa.upa(1000, 5)
print 'upa_graph', upa_graph
atack = nr_graph.keys()
random.shuffle(atack)
print 'atack'

upa_cr =cc.compute_resilience(upa_graph, atack)
print 'resilience'
count = [x for x in xrange(len(atack))]

plt.plot(count, upa_cr[1:], "r", label='UPA')


plt.xlabel('number of removed nodes')
plt.ylabel('the size of the largest connected component')

plt.legend(loc='upper right')
plt.show()

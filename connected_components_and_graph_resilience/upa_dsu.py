import connected_components as cc
import sys
sys.path.append('/home/ilya/Documents/at/degree_distributions_for_graphs')
import ddg
import upa as mupa
import math, random


upa_graph = mupa.upa(5, 500000)
print 'upa_graph'
atack = [random.randint(0,500000-1) for _ in xrange(50000)]
#random.shuffle(atack)
print 'atack'
print 'resilience'
upa_cr =cc.compute_resilience(upa_graph, atack)
print 'complete'




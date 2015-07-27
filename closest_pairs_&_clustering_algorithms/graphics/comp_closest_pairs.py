import sys
sys.path.append('../../closest_pairs_&_clustering_algorithms')
import clustering as cl
import old_clustering as old
import math, random, time
import matplotlib.pyplot as plt


def time_run(foo, clasters):
    ts = time.time()
    foo(clasters)
    return time.time() - ts

def n_time_run(foo, xclasters, yclasters):
    ts = time.time()
    foo(xclasters, yclasters)
    return time.time() - ts

old_fast_closest_pair = []
slow_closest_pair = []
py_fast_closest_pair = []

for nn in xrange(2, 201):
    _clusters = cl.gen_random_clusters(nn)
        
    xclusters = sorted(_clusters, key = lambda cluster: cluster.horiz_center())
    yclusters = sorted(_clusters, key = lambda cluster: cluster.vert_center())

    slow_closest_pair.append(time_run(cl.slow_closest_pair, xclusters))
    old_fast_closest_pair.append(time_run(old.fast_closest_pair, xclusters))
    py_fast_closest_pair.append(n_time_run(cl.fast_closest_pair, xclusters, yclusters))


count = xrange(2,201)
plt.plot(count, slow_closest_pair, "r",  label='slow closest pair')
plt.plot(count, old_fast_closest_pair, "b", label='fast closest pair')
plt.plot(count, py_fast_closest_pair, "g", label="py's style fast closest pair with 'Y'")

#title = 'Resilience of the graph, with random choice, n = {0} , p = {1}, m = {2}'.format(cnt, p, int(mx))
#plt.title(title)

plt.xlabel('number of clusters')
plt.ylabel('running time, sec')

plt.legend(loc='upper left')
plt.grid(True)
plt.show()

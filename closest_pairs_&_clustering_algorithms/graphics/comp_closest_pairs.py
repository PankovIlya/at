import sys
sys.path.append('../../closest_pairs_&_clustering_algorithms')
import clustering as cl
import old_clustering as old
import math, random, time
import matplotlib.pyplot as plt
#import gc
#gc.disable()


def time_run(foo, args):
    ts = time.time()
    foo(*args)
    return time.time() - ts

old_fast_closest_pair = []
slow_closest_pair = []
py_fast_closest_pair = []


def trials (n):
    slow_c, old_fc, py_fc = [], [], []

    for nn in xrange(2, n):
        _clusters = cl.gen_random_clusters(nn)
        
        xclusters = sorted(_clusters, key = lambda cluster: cluster.horiz_center())
        yclusters = sorted(_clusters, key = lambda cluster: cluster.vert_center())

        slow_c.append(time_run(cl.slow_closest_pair, [xclusters]))
        old_fc.append(time_run(old.fast_closest_pair, [xclusters]))
        py_fc.append(time_run(cl.fast_closest_pair,
                                           [xclusters, yclusters]))

    return slow_c, old_fc, py_fc, range(2,n)

old_fast_closest_pair, slow_closest_pair, py_fast_closest_pair, count = trials(200)


plt.plot(count, slow_closest_pair, "r",  label='slow closest pair')
plt.plot(count, old_fast_closest_pair, "b", label='fast closest pair')
plt.plot(count, py_fast_closest_pair, "g", label="py's style fast closest pair with 'Y'")

plt.xlabel('number of clusters')
plt.ylabel('running time, sec')

plt.legend(loc='upper left')
plt.grid(True)
plt.show()

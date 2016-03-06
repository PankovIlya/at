import sys
sys.path.append('../../3_closest_pairs_&_clustering_algorithms')
import clustering as clr
import old_clustering as old
import matplotlib.pyplot as plt
import time


newtimes = []
oldtimes = []
count = []
m = 299
n = 100
c = 7

def run_time(foo, data, cnt):
    ts = time.time()
    foo(data, cnt)
    return time.time() - ts

def trials(n, m):
    new_l, old_l, cnt = [], [], []
    for cc in xrange(n, m, 5):
        clr.complete(cc, m)
        _clusters = clr.gen_random_clusters(cc)
        new_l.append(run_time(clr.hierarchical_clustering,_clusters, c))
        old_l.append(run_time(old.hierarchical_clustering,_clusters, c))
        cnt.append(cc)

    return new_l, old_l, cnt

newtimes, oldtimes, count = trials(n, m)
            
plt.plot(count, oldtimes, "r", label='old style')
plt.plot(count, newtimes, "g", label="py's style")
plt.legend(loc='upper left')
plt.show()    


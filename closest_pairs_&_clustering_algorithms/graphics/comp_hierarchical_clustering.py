import sys
sys.path.append('../../closest_pairs_&_clustering_algorithms')
import load_clusters as lc
import clustering as clr
import old_clustering as old
import matplotlib.pyplot as plt
import time

def n_time_run(foo, data, cnt):
    ts = time.time()
    foo(data, cnt)
    return time.time() - ts


newtimes = []
oldtimes = []
count = []
m = 301

def trials(n, m):
    print "start"
    new_l, old_l, cnt = [], [], []
    for nn in xrange(n, m, 2):
        sys.stdout.flush()
        print "\r create {0}% ".format(nn*100/m),
        _clusters = clr.gen_random_clusters(nn)
        new_l.append(n_time_run(clr.hierarchical_clustering,_clusters, 15))
        old_l.append(n_time_run(old.hierarchical_clustering,_clusters, 15))
        cnt.append(nn)

    return new_l, old_l, cnt

newtimes, oldtimes, count = trials(100, 301)
            
plt.plot(count, oldtimes, "r", label='old style')
plt.plot(count, newtimes, "g", label="py's style")
plt.legend(loc='upper left')
plt.show()    


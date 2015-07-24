"""
implement five functions:

slow_closest_pair(cluster_list)
fast_closest_pair(cluster_list)
closest_pair_strip(cluster_list, horiz_center, half_width)
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)

"""

import math, random
import cluster as cl
from itertools import combinations




######################################################
# Code for closest pairs of clusters

def pair_distance(clusters, idx1, idx2):
    """
    Helper function that computes Euclidean distance between two clusters in a list
    """
    return (clusters[idx1].distance(clusters[idx2]), min(idx1, idx2), max(idx1, idx2))


def slow_closest_pair(clusters):
    """
    Compute the distance between the closest pair of clusters in a list (slow)
    """
    min_d = (float('inf'), -1, -1)
    cnt = len(clusters)
    for idx1 in xrange(cnt-1):
        for idx2 in xrange(idx1+1, cnt):
            min_d = min(min_d, pair_distance(clusters, idx1, idx2))
            
    return min_d



def fast_closest_pair(clusters):
    """
    Compute the distance between the closest pair of clusters in a list (fast)
    """
    cnt = len(clusters)

    if cnt <= 3:
        return slow_closest_pair(clusters)
    else:
        mid = cnt//2
        #print m
        minl = fast_closest_pair(clusters[:mid])
        minr = fast_closest_pair(clusters[mid:])
        #print minl, minr
        minr =  (minr[0], minr[1]+mid, minr[2]+mid)
        #print minl, minr 
        expect = min(minl, minr)
        mid = (clusters[mid].horiz_center() + clusters[mid-1].horiz_center())/2.0
        #print mid           
        return min(expect, closest_pair_strip(clusters, mid, expect[0]))


def closest_pair_strip(clusters, horiz_center, half_width):
    """
    Helper function to compute the closest pair of clusters in a vertical strip
    """

    def find(obj):
        """
        thank's for index
        """
        for idx in xrange(len(clusters)):
            if clusters[idx] == obj:
                return idx
        return -1
                
    sub_clusters = [cls for cls in clusters if abs(cls.horiz_center() - horiz_center) < half_width]
    sub_clusters.sort(key = lambda cluster: cluster.vert_center())
    
    cnt = len(sub_clusters)
    min_d = (float('inf'), -1, -1)
    idx1, idx2 = -1, -1 

    for idx1 in xrange(cnt-1):
        for idx2 in xrange(idx1+1, min(idx1+4, cnt)):
            dist = pair_distance(sub_clusters, idx1, idx2)
            min_d = min(min_d, dist)

    if min_d[0] != float('inf'):    
        idx1, idx2 = find(sub_clusters[min_d[1]]), find(sub_clusters[min_d[2]])
        idx1, idx2 = min(idx1, idx2), max(idx1, idx2)
        
    return (min_d[0], idx1, idx2)     

def slow_closest_pair_new(clusters):
    """
    Compute the distance between the closest pair of clusters in a list (slow)
    """
    return min(map(lambda cls: (cls[0].distance(cls[1]), cls[0], cls[1]), combinations(clusters, 2)))


get_mid = lambda cls1, cls2 : (cls1.horiz_center() + cls2.horiz_center())/2.0

def fast_closest_pair_new(xclusters, yclusters):
    """
    Compute the distance between the closest pair of clusters in a list (fast)
    """
    cnt = len(xclusters)

    if cnt <= 3:
        return slow_closest_pair_new(xclusters)
    else:

        mid = cnt/2
        ys = [cls for cls in yclusters if cls.horiz_center() < xclusters[mid].horiz_center()]
        xs = [cls for cls in yclusters if cls.horiz_center() >= xclusters[mid].horiz_center()]

        minl = fast_closest_pair_new(xclusters[:mid], ys)
        minr = fast_closest_pair_new(xclusters[mid:], xs)

        expect = min(minl, minr)
       
        return min(expect, closest_pair_strip_new(xclusters, yclusters, get_mid(xclusters[mid-1], xclusters[mid]), expect[0]))

def closest_pair_strip_new(xclusters, yclusters, horiz_center, half_width):
    """
    Helper function to compute the closest pair of clusters in a vertical strip
    """
                
    def get_list(clusters):
        """
        helper foo
        """
        if not clusters:
            return []
        else:
            return [(clusters[0].distance(cls), clusters[0], cls) for cls in clusters[1:4]] + get_list(clusters[1:])

    def expect_list(clusters):
        """
        4 consecutive comparison. py is not haskell, but if you want...
        """
        cnt = len(clusters)
        
        if cnt <= 8:
            return get_list(clusters)
        else:
            return expect_list(clusters[:cnt//2+4]) + expect_list(clusters[cnt//2:])


    
    clusters = [cls for cls in yclusters if abs(cls.horiz_center() - horiz_center) < half_width]
    clusters = expect_list(clusters) 
    clusters.append((float('inf'), None, None))
        
    return min(clusters)


######################################################################
# Code for hierarchical clustering

compx = lambda cls1, cls2: 1 if cls1.horiz_center() > cls2.horiz_center() else ( -1 if cls1.horiz_center() < cls2.horiz_center() else 0)
compy = lambda cls1, cls2: 1 if cls1.vert_center() > cls2.vert_center() else ( -1 if cls1.vert_center() < cls2.vert_center() else 0)

def insert_claster(clasters, foo, val):
    """
    helper foo, insert into sorted list
    """
    if not clasters:
        return [val]
    else:
        mid = len(clasters)//2
        res = foo(clasters[mid], val)
        if res == 1:
            return insert_claster(clasters[:mid], foo, val) + clasters[mid:]
        elif res == -1:
            return clasters[:mid+1] + insert_claster(clasters[mid+1:], foo, val)
        else:
            return clasters[:mid] + [val] + clasters[mid:]
        
    
def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    """
    clusters = [cls.copy() for cls in cluster_list]
    clusters.sort(key = lambda cls: cls.horiz_center())

    while len(clusters) > num_clusters:
        min_cc = fast_closest_pair(clusters)
        cls = clusters[min_cc[1]].merge_clusters(clusters[min_cc[2]])
        del clusters[min_cc[2]]
        del clusters[min_cc[1]]
        clusters = insert_claster(clusters, compx, cls)
        #clusters.sort(key = lambda cls: cls.horiz_center())

    return clusters

def hierarchical_clustering_new(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    """
    xclusters = [cls.copy() for cls in cluster_list]
    xclusters.sort(key = lambda cls: cls.horiz_center())
    yclusters = sorted(xclusters, key = lambda cls: cls.vert_center())

    while len(xclusters) > num_clusters:
        min_cc = fast_closest_pair_new(xclusters, yclusters)
        cls1, cls2 = min_cc[1], min_cc[2] 
        new_cls = cls1.merge_clusters(cls2)

        xclusters.remove(cls1)
        xclusters.remove(cls2)
        yclusters.remove(cls1)
        yclusters.remove(cls2)
        
        xclusters = insert_claster(xclusters, compx, new_cls)
        yclusters = insert_claster(yclusters, compy, new_cls)
        
    return xclusters

######################################################################
# Code for k-means clustering

class KCluster(cl.Cluster):
    """
    Child Class, main Cluster 
    """
    def __init__(self, cluster):
        """
        Create a cluster 
        """
        cl.Cluster.__init__(self,
                             set(cluster.fips_codes()),
                                 cluster.horiz_center(),
                                 cluster.vert_center(),
                                 cluster.total_population(),
                                 cluster.averaged_risk())
        self._center = (0, 0)
        self.init()
        self.update()
                                      
    def update(self):
        """ update data center """
        self._center = (self._horiz_center, self._vert_center)

    def center(self):
        """ center coord """
        return self._center
                                     
    def init(self):
        """
        init cluster
        """

        self._fips_codes = set([])
        self._total_population = 0
        self._averaged_risk = 0

    def kdistance(self, cluster):
        """
        Compute the Euclidean distance between two clusters
        """
        vert_dist = self._center[1] - cluster.vert_center()
        horiz_dist = self._center[0] - cluster.horiz_center()

        return math.sqrt(vert_dist ** 2 + horiz_dist ** 2)       
    
def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    """

    clusters = []
    points = sorted(cluster_list, key = lambda cluster: cluster.total_population(), reverse=True)

    for idx in xrange(num_clusters):
            clusters.append(KCluster(points[idx]))

    for _ in xrange(num_iterations):

        for cluster in clusters:
            cluster.init()

        for point in points:
            min_c = (float('inf'), None)

            for cluster in clusters:
                min_c = min(min_c, (cluster.kdistance(point), cluster))

            min_c[1].merge_clusters(point)
        
        for cluster in clusters:
            cluster.update()

    return clusters

def gen_random_clusters(num_clusters):
    """
    gen random clusters
    """
    
    clusters = []
    
    for num in xrange(num_clusters):
        clusters.append(cl.Cluster(set([num]), random.uniform(-1,1), random.uniform(-1,1), 1, 0))

    return clusters

for nn in xrange(50):

    _clusters = gen_random_clusters(500)
    
    ogxclusters = sorted(_clusters, key = lambda cluster: cluster.horiz_center())

    gxclusters = sorted(_clusters, key = lambda cluster: cluster.horiz_center())
    gyclusters = sorted(_clusters, key = lambda cluster: cluster.vert_center())

    print 'go' + str(nn)
    a = fast_closest_pair_new(gxclusters, gyclusters)
    b = fast_closest_pair(ogxclusters)

    #print a, b
    assert a[0] == b[0]

    c = hierarchical_clustering_new(_clusters, 50)
    d = hierarchical_clustering(_clusters, 50)

    for idx in xrange(len(c)):
        assert c[idx].fips_codes()^d[idx].fips_codes() == set([])   

    



 



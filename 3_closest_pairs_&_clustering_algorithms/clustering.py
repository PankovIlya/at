"""
two methods of clustering data
https://drive.google.com/file/d/0B08tXgxczBp6dkZ3TEFtVzdvbms/view?usp=sharing

Hierarchical clustering algorithm O(n^3)
https://en.wikipedia.org/wiki/Hierarchical_clustering

K means_clustering algorithm O(q k n) n - number of points, k - number of clusters, q - number of iterations
https://en.wikipedia.org/wiki/K-means_clustering
"""


import math
import random
from itertools import combinations
import data.cluster as cl

### Hierarchical clustering ###

def slow_closest_pair(clusters):
    """
    Compute the distance between the closest pair of clusters in a list (slow)
    """
    return min(map(lambda cls: (cls[0].distance(cls[1]), cls[0], cls[1]), \
               combinations(clusters, 2)))


get_mid = lambda cls1, cls2 : (cls1.horiz_center() + cls2.horiz_center())/2.0

def fast_closest_pair(xclusters, yclusters):
    """
    Compute the distance between the closest pair of clusters in a list (fast)
    """
    cnt = len(xclusters)

    if cnt <= 3:
        return slow_closest_pair(xclusters)
    else:

        mid = cnt/2
        ys = [cls for cls in yclusters if cls.horiz_center() < xclusters[mid].horiz_center()]
        xs = [cls for cls in yclusters if cls.horiz_center() >= xclusters[mid].horiz_center()]

        minl = fast_closest_pair(xclusters[:mid], ys)
        minr = fast_closest_pair(xclusters[mid:], xs)

        expect = min(minl, minr)
       
        return min(expect, closest_pair_strip(xclusters, yclusters, \
                                              get_mid(xclusters[mid-1], \
                                              xclusters[mid]), expect[0]))

def closest_pair_strip(xclusters, yclusters, horiz_center, half_width):
    """
    Helper function to compute the closest pair of clusters in a vertical strip
    """

    cmp = 4 #4 consecutive comparison
    min_cl = 8 #

                
    def get_list(clusters):
        """
        helper foo
        """
        if not clusters:
            return []
        else:
            return [(clusters[0].distance(cls), clusters[0], cls) for cls in clusters[1:cmp]] + get_list(clusters[1:])

    def expect_list(clusters):
        cnt = len(clusters)
        
        if cnt <= min_cl:
            return get_list(clusters)
        else:
            return expect_list(clusters[:cnt//2+cmp]) + expect_list(clusters[cnt//2:])


    
    clusters = [cls for cls in yclusters if abs(cls.horiz_center() - horiz_center) < half_width]
    clusters = expect_list(clusters) 
    clusters.append((float('inf'), None, None))
        
    return min(clusters)



compx = lambda cls1, cls2: 1 if cls1.horiz_center() > cls2.horiz_center() \
                             else ( -1 if cls1.horiz_center() < cls2.horiz_center() else 0)

compy = lambda cls1, cls2: 1 if cls1.vert_center() > cls2.vert_center() \
                             else ( -1 if cls1.vert_center() < cls2.vert_center() else 0)



def insert_cluster(clusters, foo, val):
    """
    helper foo, insert into sorted list
    """
    if not clusters:
        return [val]

    mid = len(clusters)//2
    res = foo(clusters[mid], val)

    if res == 1:
        return insert_cluster(clusters[:mid], foo, val) + clusters[mid:]
    elif res == -1:
        return clusters[:mid+1] + insert_cluster(clusters[mid+1:], foo, val)

    return clusters[:mid] + [val] + clusters[mid:]
        

def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    """
    xclusters = [cls.copy() for cls in cluster_list]
    xclusters.sort(key = lambda cls: cls.horiz_center())
    yclusters = sorted(xclusters, key = lambda cls: cls.vert_center())

    while len(xclusters) > num_clusters:
        min_cc = fast_closest_pair(xclusters, yclusters)
        cls1, cls2 = min_cc[1], min_cc[2] 
        new_cls = cls1.merge_clusters(cls2)

        #Yes, but del a cluster of Y-clusters by index still does not work and del from list it's O(n)
        xclusters.remove(cls1)
        xclusters.remove(cls2)
   
        yclusters.remove(cls1)
        yclusters.remove(cls2)

        xclusters = insert_cluster(xclusters, compx, new_cls)
        yclusters = insert_cluster(yclusters, compy, new_cls)
        
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

class Clusters( object ):
    def __init__(self, points, num_cls):
        self.points = points 
        self.clusters = [KCluster(points[idx]) for idx in xrange(num_cls)]

    def init(self):
        for cluster in self.clusters:
            cluster.init()
    
    def update(self):
        for cluster in self.clusters:
            cluster.update()
        
    def calc(self):
        self.init()
        
        for point in self.points:
            min_c = (float('inf'), None)

            for cluster in self.clusters:
                min_c = min(min_c, (cluster.kdistance(point), cluster))

            min_c[1].merge_clusters(point)

        self.update()
        
        
def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    """
     
    points = sorted(cluster_list, key = lambda cluster: cluster.total_population(), reverse=True)
    clusters = Clusters(points, num_clusters)

    for n in xrange(num_iterations):
        clusters.calc()
        
    return clusters.clusters

def gen_random_clusters(num_clusters):
    """
    gen random clusters
    """

    clusters = []
    
    for num in xrange(num_clusters):
        clusters.append(cl.Cluster(set([num]), random.uniform(-1,1), random.uniform(-1,1), 1, 0))

    return clusters




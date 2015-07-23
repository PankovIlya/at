"""
implement five functions:

slow_closest_pair(cluster_list)
fast_closest_pair(cluster_list)
closest_pair_strip(cluster_list, horiz_center, half_width)
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)

"""

import math, random
#import cluster as alg_cluster
import alg_cluster



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
        mid = abs(clusters[mid].horiz_center() + clusters[mid-1].horiz_center())/2.0
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
 
##print closest_pair_strip([alg_cluster.Cluster(set([]), 0, 0, 1, 0), alg_cluster.Cluster(set([]), 1, 0, 1, 0),
##                           alg_cluster.Cluster(set([]), 2, 0, 1, 0), alg_cluster.Cluster(set([]), 3, 0, 1, 0)], 1.5, 1.0)
##
##
##print closest_pair_strip([alg_cluster.Cluster(set([]), 1.0, 1.0, 1, 0), alg_cluster.Cluster(set([]), 1.0, 5.0, 1, 0),
##                           alg_cluster.Cluster(set([]), 1.0, 4.0, 1, 0), alg_cluster.Cluster(set([]), 1.0, 7.0, 1, 0)], 1.0, 3.0)

##print closest_pair_strip([alg_cluster.Cluster(set([]), 0.32, 0.16, 1, 0), alg_cluster.Cluster(set([]), 0.39, 0.4, 1, 0),
##                          alg_cluster.Cluster(set([]), 0.54, 0.8, 1, 0),
##                          alg_cluster.Cluster(set([]), 0.61, 0.8, 1, 0),
##                          alg_cluster.Cluster(set([]), 0.76, 0.94, 1, 0)], 0.46500000000000002, 0.070000000000000007)
##print closest_pair_strip([alg_cluster.Cluster(set([]), -4.0, 0.0, 1, 0),
##                    alg_cluster.Cluster(set([]), 0.0, -1.0, 1, 0),
##                    alg_cluster.Cluster(set([]), 0.0, 1.0, 1, 0),
##                    alg_cluster.Cluster(set([]), 4.0, 0.0, 1, 0)], 0.0, 4.1231059999999999)
## expected one of the tuples in set([(2.0, 1, 2)]) 

#([(1.0, 1, 2)]) but received (1.0, 0, 1)    

##print fast_closest_pair([alg_cluster.Cluster(set([]), 0, 0, 1, 0),
##                         alg_cluster.Cluster(set([]), 1, 0, 1, 0),
##                         alg_cluster.Cluster(set([]), 2, 0, 1, 0),
##                         alg_cluster.Cluster(set([]), 3, 0, 1, 0)])

#expected one of the tuples in set([(1.0, 1, 2), (1.0, 0, 1), (1.0, 2, 3)])

##print fast_closest_pair([alg_cluster.Cluster(set([]), 0.32, 0.16, 1, 0),
##                         alg_cluster.Cluster(set([]), 0.39, 0.4, 1, 0),
##                         alg_cluster.Cluster(set([]), 0.54, 0.8, 1, 0),
##                         alg_cluster.Cluster(set([]), 0.61, 0.8, 1, 0),
##                         alg_cluster.Cluster(set([]), 0.76, 0.94, 1, 0)])

#expected one of the tuples in set([(0.069999999999999951, 2, 3)])
#but received (0.25, 0, 1)


##print fast_closest_pair([alg_cluster.Cluster(set([]), 0.05, 0.11, 1, 0),
##                         alg_cluster.Cluster(set([]), 0.26, 0.92, 1, 0),
##                         alg_cluster.Cluster(set([]), 0.34, 0.57, 1, 0),
##                         alg_cluster.Cluster(set([]), 0.35, 0.15, 1, 0),
##                         alg_cluster.Cluster(set([]), 0.6, 0.41, 1, 0),
##                         alg_cluster.Cluster(set([]), 0.89, 0.28, 1, 0)])
#expected one of the tuples in set([(0.30265491900843111, 0, 3)])



######################################################################
# Code for hierarchical clustering

COMP = lambda cls1, cls2: 1 if cls1.horiz_center() > cls2.horiz_center() else ( -1 if cls1.horiz_center() < cls2.horiz_center() else 0)


def insert_claster(clasters, cmpv, val):
    """
    helper foo, insert into sorted list
    """
    if not clasters:
        return [val]
    else:
        mid = len(clasters)//2
        res = cmpv(clasters[mid], val)
        if res == 1:
            return insert_claster(clasters[:mid], cmpv, val) + clasters[mid:]
        elif res == -1:
            return clasters[:mid+1] + insert_claster(clasters[mid+1:], cmpv, val)
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
        clusters = insert_claster(clusters, COMP, cls)
        #clusters.sort(key = lambda cls: cls.horiz_center())

    return clusters


######################################################################
# Code for k-means clustering

class KCluster(alg_cluster.Cluster):
    """
    Child Class, main Cluster 
    """
    def __init__(self, cluster):
        """
        Create a cluster 
        """
        alg_cluster.Cluster.__init__(self,
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


"""
implement five functions:

slow_closest_pair(cluster_list)
fast_closest_pair(cluster_list)
closest_pair_strip(cluster_list, horiz_center, half_width)
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)

"""

import sys, math, random
import cluster as cl
from itertools import combinations
import old_clustering as old



######################################################
# Code for closest pairs of clusters

def slow_closest_pair(clusters):
    """
    Compute the distance between the closest pair of clusters in a list (slow)
    """
    return min(map(lambda cls: (cls[0].distance(cls[1]), cls[0], cls[1]), combinations(clusters, 2)))


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
       
        return min(expect, closest_pair_strip(xclusters, yclusters, get_mid(xclusters[mid-1], xclusters[mid]), expect[0]))

def closest_pair_strip(xclusters, yclusters, horiz_center, half_width):
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
    xclusters = [cls.copy() for cls in cluster_list]
    xclusters.sort(key = lambda cls: cls.horiz_center())
    yclusters = sorted(xclusters, key = lambda cls: cls.vert_center())

    while len(xclusters) > num_clusters:
        if not len(xclusters)%10:
            # this is for you )
            sys.stdout.flush()
            print "\r processing {0}%".format(round((num_clusters*100.0/len(xclusters)),1)),
        min_cc = fast_closest_pair(xclusters, yclusters)
        cls1, cls2 = min_cc[1], min_cc[2] 
        new_cls = cls1.merge_clusters(cls2)

        #Yes, but del a cluster of Y-clusters by index still does not work and del from list it's O(n)
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


if __name__ == '__main__':

    for nn in xrange(100):

        _clusters = gen_random_clusters(200)
        
        ogxclusters = sorted(_clusters, key = lambda cluster: cluster.horiz_center())

        gxclusters = sorted(_clusters, key = lambda cluster: cluster.horiz_center())
        gyclusters = sorted(_clusters, key = lambda cluster: cluster.vert_center())

        print 'go ' + str(nn)
        a = fast_closest_pair(gxclusters, gyclusters)
        b = old.fast_closest_pair(ogxclusters)
        c = slow_closest_pair(ogxclusters)

        assert a[0] == b[0] == c[0]

        c = hierarchical_clustering(_clusters, 50)
        d = old.hierarchical_clustering(_clusters, 50)

        for idx in xrange(len(c)):
            assert c[idx].fips_codes()^d[idx].fips_codes() == set([])   

    



 



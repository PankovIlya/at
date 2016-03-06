"""
'old' style for owltest implement
"""

import sys
sys.path.append('../3_closest_pairs_&_clustering_algorithms/data')

import data.cluster as cl


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


######################################################################
# Code for hierarchical clustering

compx = lambda cls1, cls2: 1 if cls1.horiz_center() > cls2.horiz_center() else ( -1 if cls1.horiz_center() < cls2.horiz_center() else 0)

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

    



 



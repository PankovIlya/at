"""
Student template code for Project 3
Student will implement five functions:

slow_closest_pair(cluster_list)
fast_closest_pair(cluster_list)
closest_pair_strip(cluster_list, horiz_center, half_width)
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)

where cluster_list is a 2D list of clusters in the plane
"""

import math
#import cluster as alg_cluster



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
    n = len(clusters)

    if n <= 3:
        return slow_closest_pair(clusters)
    else:
        m = n//2
        #print m
        minl = fast_closest_pair(clusters[:m])
        minr = fast_closest_pair(clusters[m:])
        #print minl, minr
        minr =  (minr[0], minr[1]+m, minr[2]+m)
        #print minl, minr 
        expect = min(minl, minr)
        mid = abs(clusters[m].horiz_center() + clusters[m-1].horiz_center())/2.0
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
                
    #print horiz_center, half_width 
    sub_clusters = [cls for cls in clusters if abs(cls.horiz_center() - horiz_center) < half_width]
    sub_clusters.sort(key = lambda cluster: cluster.vert_center())
    #sub_clusters.sort(key = lambda cluster: cluster.horiz_center() - horiz_center)
    #print sub_clusters
    cnt = len(sub_clusters)
    min_d = (float('inf'), -1, -1)
    idx1, idx2 = -1, -1 

    for idx1 in xrange(cnt-1):
        for idx2 in xrange(idx1+1, min(idx1+4, cnt)):
            dist = pair_distance(sub_clusters, idx1, idx2)
            #print idx1, idx2, dist 
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
######################################################################
# Code for hierarchical clustering

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

def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    """
    while len(cluster_list) > num_clusters:
        min_cc = fast_closest_pair(cluster_list)
        cluster_list[min_cc[1]].merge_clusters(cluster_list[min_cc[2]])
        del cluster_list[min_cc[2]]
    
    return cluster_list


######################################################################
# Code for k-means clustering

    
def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Note: the function may not mutate cluster_list
    
    Input: List of clusters, integers number of clusters and number of iterations
    Output: List of clusters whose length is num_clusters
    """

    # position initial clusters at the location of clusters with largest populations
            
    return []


import sys
sys.path.append('../../closest_pairs_&_clustering_algorithms')
import load_clusters as lc
import clustering as clr
import cluster as cl
import plot_clusters as pc
import alg_clusters_matplotlib as cplot
import time


data_table = lc.load_data_table(lc.DATA_896_URL) #DATA_3108_URL DATA_290_URL
    
singleton_list = []
for line in data_table:
    singleton_list.append(cl.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))

cluster_list = clr.hierarchical_clustering(singleton_list, 15)

        
cplot.plot_clusters(data_table, cluster_list, True)
    


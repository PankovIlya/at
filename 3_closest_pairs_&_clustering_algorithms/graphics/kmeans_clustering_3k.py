import sys

sys.path.append('../../3_closest_pairs_&_clustering_algorithms')

import data.load_clusters as lc
import clustering as clr
import data.cluster as cl
import alg_clusters_matplotlib as cp



data_table = lc.load_data_table(lc.DATA_3108_URL) #DATA_3108_URL
    
singleton_list = []
for line in data_table:
    singleton_list.append(cl.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))


cluster_list = clr.kmeans_clustering(singleton_list, 7, 7)

cp.plot_clusters(data_table, cluster_list, True)
    


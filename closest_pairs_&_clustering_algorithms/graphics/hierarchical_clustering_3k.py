import load_clusters as lc
import sys
sys.path.append('../../closest_pairs_&_clustering_algorithms')
import clustering as clr
import cluster as cl
import old_clustering as old
import plot_clusters as pc
import alg_clusters_matplotlib as cplot


data_table = lc.load_data_table(lc.DATA_290_URL) #DATA_3108_URL
    
singleton_list = []
for line in data_table:
    singleton_list.append(cl.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
    
cluster_list = clr.hierarchical_clustering(singleton_list, 15)
#cluster_list = alg_project3_solution.kmeans_clustering(singleton_list, 9, 5)	
    
            
cplot.plot_clusters(data_table, cluster_list, True)
    


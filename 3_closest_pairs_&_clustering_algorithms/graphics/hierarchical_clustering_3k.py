import sys
sys.path.append('../../3_closest_pairs_&_clustering_algorithms')
import data.load_clusters as lc
import data.cluster as cl
import clustering as clr
import alg_clusters_matplotlib as cplot

data_table = lc.load_data_table(lc.DATA_896_URL) #DATA_3108_URL DATA_290_URL
    
singleton_list = []
for line in data_table:
    singleton_list.append(cl.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))

c = 7 # cluster count

cluster_list = clr.hierarchical_clustering(singleton_list, c)

        
cplot.plot_clusters(data_table, cluster_list, True)
    


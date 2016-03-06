"""
Example code for creating and visualizing
cluster of county-based cancer risk data

Note that you must download the file
http://www.codeskulptor.org/#alg_clusters_matplotlib.py
to use the matplotlib version of this code
"""
import urllib2
import os



###################################################
# Code to load data tables

# URLs for cancer risk data tables of various sizes
# Numbers indicate number of counties in data table

##DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
##DATA_3108_URL = DIRECTORY + "data_clustering/unifiedCancerData_3108.csv"
##DATA_896_URL = DIRECTORY + "data_clustering/unifiedCancerData_896.csv"
##DATA_290_URL = DIRECTORY + "data_clustering/unifiedCancerData_290.csv"
##DATA_111_URL = DIRECTORY + "data_clustering/unifiedCancerData_111.csv"


DIRECTORY = os.path.dirname(__file__)
DATA_3108_URL = os.path.join(DIRECTORY, "unifiedCancerData_3108.csv")
DATA_896_URL = os.path.join(DIRECTORY, "unifiedCancerData_896.csv")
DATA_290_URL = os.path.join(DIRECTORY, "unifiedCancerData_290.csv")
DATA_111_URL = os.path.join(DIRECTORY, "unifiedCancerData_111.csv")


def load_data_table(data):
    """
    Import a table of county-based cancer risk data
    from a csv format file
    """
    #data_file = urllib2.urlopen(data_url)
    data_file = open(data)
    data = data_file.read()
    data_lines = data.split('\n')
    print "Loaded", len(data_lines), "data points"
    data_tokens = [line.split(',') for line in data_lines]
    return [[tokens[0], float(tokens[1]), float(tokens[2]), int(tokens[3]), float(tokens[4])] 
            for tokens in data_tokens]





    





  
        






        





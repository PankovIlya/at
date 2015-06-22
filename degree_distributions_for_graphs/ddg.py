""" Degree distributions for graphs """
import random

EX_GRAPH0 = {0:set([1,2]), 1:set([]),2:set([])}

EX_GRAPH1 = {0:set([1,4,5]),1:set([2,6]),2:set([3]),3:set([0]),4:set([1]),5:set([2]),6:set([])}

EX_GRAPH2 = {0:set([1,4,5]),1:set([2,6]),2:set([3,7]),3:set([7]),4:set([1]),5:set([2]),6:set([]),\
             7:set([3]),8:set([1,2]),9:set([0,3,4,5,6,7])}


def make_complete_graph(num_nodes):
    """ returns a dictionary corresponding to a complete directed graph with the specified number of nodes """
    graph = {}
    for idx1 in xrange(num_nodes):
        graph[idx1] = set([idx2 for idx2 in xrange(num_nodes) if idx2 != idx1])
    return graph

def make_complete_graph_p(num_nodes, p):
    """ returns a dictionary corresponding to a complete directed graph with the specified number of nodes """
    graph = {}
    for idx1 in xrange(num_nodes):
        graph[idx1] = set([idx2 for idx2 in xrange(num_nodes) if idx2 != idx1 and random.random() < p])
    return graph

def make_complete_ugraph_p(num_nodes, p):
    """ returns a dictionary corresponding to a complete directed graph with the specified number of nodes """
    graph = {}
    for idx1 in xrange(num_nodes):
        graph[idx1] = set([idx2 for idx2 in xrange(num_nodes) if idx2 != idx1 and random.random() < p])
    return graph




#print make_complete_graph(5)

def compute_in_degrees(digraph):
    """ computes the in-degrees for the nodes in the graph """
    graph = {}
    for node in digraph:
        graph.setdefault(node, 0)
        for item in digraph[node]:
            graph.setdefault(item, 0)
            graph[item] += 1
    return graph

        
#print compute_in_degrees(EX_GRAPH2)


def in_degree_distribution(digraph):
    """ omputes the unnormalized distribution of the in-degrees of the graph """
    graph = {}
    graph_in_degrees = compute_in_degrees(digraph)
    for node in graph_in_degrees:
        deegree = graph_in_degrees[node]
        graph.setdefault(deegree, 0)
        graph[deegree] += 1
    return graph

def norm_degree_distribution(deg_distr):
    sum_val = sum(deg_distr.values())
    return dict([(node*1.0, deg_distr[node]*1.0/sum_val) for node in deg_distr])



    


#print in_degree_distribution(EX_GRAPH2)
    

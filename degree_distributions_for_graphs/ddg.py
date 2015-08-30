""" Degree distributions for graphs """
import sys, random


def make_complete_graph(num_nodes):
    """ returns a dictionary corresponding to a complete directed graph with the specified number of nodes """
    graph = {}
    for idx1 in xrange(num_nodes):
        if not idx1%100:
            sys.stdout.flush()
            print "\r processing {0}%".format(idx1*100/num_nodes),
        graph[idx1] = set([idx2 for idx2 in xrange(num_nodes) if idx2 != idx1])
    return graph

def make_complete_graph_p(num_nodes, p):
    """ returns a dictionary corresponding to a complete directed graph with the specified number of nodes """
    graph = {}
    for idx1 in xrange(num_nodes):
        if not idx1%100:
            sys.stdout.flush()
            print "\r processing {0}%".format(idx1*100/num_nodes),
        graph[idx1] = set([idx2 for idx2 in xrange(num_nodes) if idx2 != idx1 and random.random() < p])
    return graph

def make_complete_ugraph_p(num_nodes, p):
    """ returns a dictionary corresponding to a complete directed graph with the specified number of nodes """
    graph = {}
    for idx1 in xrange(num_nodes):
        graph.setdefault(idx1, set([]))
        graph[idx1] = graph[idx1].union(set([idx2 for idx2 in xrange(idx1+1, num_nodes) if random.random() < p]))
        for node in graph[idx1]:
            graph.setdefault(node, set([]))
            graph[node].add(idx1)
    
    return graph


def compute_in_degrees(digraph):
    """ computes the in-degrees for the nodes in the graph """
    graph = {}
    for node in digraph:
        graph.setdefault(node, 0)
        for item in digraph[node]:
            graph.setdefault(item, 0)
            graph[item] += 1
    return graph


def compute_degrees(ugraph):
    """ computes the in-degrees for the nodes in the graph """
    graph = {}
    for node in ugraph:
        graph[node] = len(ugraph[node])

    return graph

        
def in_degree_distribution(digraph):
    """ omputes the unnormalized distribution of the in-degrees of the graph """
    graph = {}
    graph_in_degrees = compute_in_degrees(digraph)
    for node in graph_in_degrees:
        deegree = graph_in_degrees[node]
        graph.setdefault(deegree, 0)
        graph[deegree] += 1
    return graph


def degree_distribution(ugraph):
    """ omputes the unnormalized distribution of the in-degrees of the graph """
    graph = {}
    graph_degrees = compute_degrees(ugraph)
    for node in graph_degrees:
        deegree = graph_degrees[node]
        graph.setdefault(deegree, 0)
        graph[deegree] += 1
    return graph



def norm_degree_distribution(deg_distr):
    sum_val = sum(deg_distr.values())
    return dict([(node, deg_distr[node]*1.0/sum_val) for node in deg_distr])




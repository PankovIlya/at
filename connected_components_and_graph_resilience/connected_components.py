""" Connected components and graph resilience """
import dsu as mdsu
import data
import urllib2
import random

def bfs_visited(ugraph, start_node):
    """ Algorithm BFS-Visited """
    visited = set([start_node])
    queue = [start_node]
    while queue:
        node = queue.pop(0)
        if node in ugraph:
            for child in ugraph[node]:
                if child not in visited:
                    queue.append(child)
                    visited.add(child)
        else:
            visited.remove(node)        
    return visited

def cc_visited(ugraph):
    """ connected components  """
    scc = []
    remaining = set(ugraph.keys())
    while remaining:
        node = remaining.pop()
        set_con = bfs_visited(ugraph, node)
        scc += [set_con]
        remaining -= set_con
    return scc

def largest_cc_size(ugraph):
    """ returns the size of the largest connected component in ugraph"""
    graphs = cc_visited(ugraph)
    if graphs:
        return max([len(graph) for graph in graphs])
    else:
        return 0

def compute_resilience (ugraph, attack_order):
    """ graph resilience """
    rgraph = {}
    agraph = []

    for node in ugraph:
        if node not in attack_order:
            rgraph[node] = ugraph[node]
        
    agraph = reduce(lambda graph, node : [node] + graph, attack_order, [])
      
    scc = cc_visited(rgraph)
    dsu = mdsu.DSU()
    for nodes in scc:
       head = nodes.pop() 
       dsu.make(head)
       while nodes: 
           dsu.add(nodes.pop(), head)


    dcc = [dsu.count()]
    for anode in agraph:
        nodes = ugraph[anode]
        dsu.make(anode)
        for node in nodes:
            head = dsu.find(node)
            if head != None:
                dsu.join(anode, head)
        dcc = [dsu.count()] + dcc

    return  dcc

def compute_resilience2 (ugraph, attack_order):
    """ graph resilience """

    ccs = [largest_cc_size(ugraph)]
    for node in attack_order:
        del ugraph[node]
        ccs += [largest_cc_size(ugraph)]

    return ccs



def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Returns a dictionary that models a graph
    """
    #graph_file = urllib2.urlopen(graph_url)
    graph_file = open("ccdata.txt")
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[ : -1]
    
    print "Loaded graph with", len(graph_lines), "nodes"
    
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph

if __name__ == "__main__":
    net_url = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"
    cr = compute_resilience(data.GRAPH2, [1, 3, 5, 7, 2, 4, 6, 8])
    assert ( cr ==  [8, 7, 6, 5, 1, 1, 1, 1, 0])
    ugraph = load_graph(net_url)
    print 'LOAD'
    atack = set([random.choice(ugraph.keys()) for _ in xrange(len(ugraph)//3)])
    assert (compute_resilience(ugraph, atack) == compute_resilience2(ugraph, atack))

    



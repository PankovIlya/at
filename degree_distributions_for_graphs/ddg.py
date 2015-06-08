EX_GRAPH0 = {0:set([1,2]), 1:set([]),2:set([])}
EX_GRAPH1 = {0:set([1,4,5]),1:set([2,6]),2:set([3]),3:set([0]),4:set([1]),5:set([2]),6:set([])}
EX_GRAPH2 = {0:set([1,4,5]),1:set([2,6]),2:set([3,7]),3:set([7]),4:set([1]),5:set([2]),6:set([]),\
             7:set([3]),8:set([1,2]),9:set([0,3,4,5,6,7])}

def make_complete_graph(num_nodes):
    graph = {}
    for idx1 in xrange(num_nodes):
        graph[idx1] = set([idx2 for idx2 in xrange(num_nodes) if idx2 != idx1])
    return graph

print make_complete_graph(5)

def compute_in_degrees(digraph):
    pass

def in_degree_distribution(digraph):
    pass

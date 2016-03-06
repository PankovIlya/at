""" Connected components and graph resilience """
import dsu as mdsu
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
    """ graph resilience with DSU O(n+m) """
    rgraph = {}
    agraph = []
    
    rgraph = copy_graph(ugraph)             

    for node in set(attack_order):
        del rgraph[node]
        
    agraph = attack_order[::-1] 
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

def copy_graph(graph):
    """
    Make a copy of a graph
    """
    new_graph = {}
    for node in graph:
        new_graph[node] = set(graph[node])
    return new_graph

def compute_resilience_simple (ugraph, attack_order):
    """ graph resilience O(n(n+m)) """

    cgraph = copy_graph(ugraph)
    ccs = [largest_cc_size(cgraph)]
    for node in attack_order:
        del cgraph[node] 
        ccs += [largest_cc_size(cgraph)]

    return ccs


def renum_keys(ugraph):
    ord_graph = {}
    idx = 0 
    res_graph = {}    
    for node in ugraph:
        ord_graph[node] = idx
        idx += 1

    for hnode in ugraph:
        idx = ord_graph[hnode]
        res_graph.setdefault(idx, set([]))
        for cnode in ugraph[hnode]:
            res_graph[idx].add(ord_graph[cnode])

    return res_graph



    



import dsu
""" Connected components and graph resilience """

def bfs_visited(ugraph, start_node):
    """ Algorithm BFS-Visited """
    visited = set([start_node])
    queue = [start_node]
    while queue:
        node = queue.pop(0)
        for child in ugraph[node]:
            if child not in visited:
                queue.append(child)
                visited.add(child)
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
    return max([len(graph) for graph in cc_visited(ugraph)])

def compute_resilience (ugraph, attack_order):

    rgraph = {}
    agraph = {}

    for node in ugraph:
        if node not in attack_order:
            rgraph[node] = ugraph[node]
        else:
            agraph[node] = ugraph[node]
        
    scc = cc_visited(rgraph)
    dsu = dsu.DSU()
    for setc in scc:
       head = setc[0]
       dsu.make(head)
       for node in setc:
           dsu.add(node, head)

    dcc = {}
    for anode in agraph:
        cnt = dsu.count
        for node in agraph[node]:
            dsu.join(anode, node)     
        dcc[anode] = cnt - dsu.count

    return dcc
           

def ack(m, n):
    """ Ackermann function """
    if m == 0:
        return n + 1
    elif m > 0 and n == 0:
        return ack(m-1,1)
    else: #m > 0 and n > 0:
        return ack(m-1, ack(m, n-1))



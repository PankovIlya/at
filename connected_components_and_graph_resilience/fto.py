import data, time
import connected_components as cc


def fast_targeted_order(ugraph):
    """
    Fasy Compute a targeted attack order consisting
    of nodes of maximal degree
    O(n+m)
    """
    fgraph = cc.copy_graph(ugraph)
    
    sdegree = {}
    
    for node in xrange(len(fgraph)):
        sdegree[node] = set([])
       
    for node in fgraph:
        cnt = len(ugraph[node])
        sdegree[cnt].add(node)

    rnodes = []    
    for k in xrange(len(ugraph)-1, 0, -1):
        nodes = sdegree[k]
        while nodes:
            rnode = nodes.pop()
            for node in fgraph[rnode]:
                cnt = len(fgraph[node])
                if node in sdegree[cnt]:  
                    sdegree[cnt].remove(node)
                    sdegree[cnt-1].add(node)

            rnodes.append(rnode)

    return rnodes

def targeted_order(ugraph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree
    O(n(n+m))
    """
    # copy the graph
    new_graph = cc.copy_graph(ugraph)
    
    order = []    
    while len(new_graph) > 0:
        max_degree = -1
        for node in new_graph:
            if len(new_graph[node]) > max_degree:
                max_degree = len(new_graph[node])
                max_degree_node = node
        
        neighbors = new_graph[max_degree_node]
        new_graph.pop(max_degree_node)
        for neighbor in neighbors:
            new_graph[neighbor].remove(max_degree_node)

        order.append(max_degree_node)
    return order

def time_run(ugraf, foo):
    ts = time.time()
    foo(ugraf)
    return time.time() - ts
    
    
    

if __name__ == "__main__":
    import sys
    sys.path.append('/home/ilya/Documents/at/degree_distributions_for_graphs')
    import upa as mupa
    import matplotlib.pyplot as plt
 
       
    cntx = []
    toy = []
    ftoy = []

    for cnt in xrange(10,1000,10):
        cntx += [cnt]
        upa_graph = mupa.upa(5, cnt)
        toy += [time_run(upa_graph, targeted_order)]
        ftoy += [time_run(upa_graph, fast_target_order)]

    plt.plot(cntx, toy, "r", label='Target Order')
    plt.plot(cntx, ftoy, "g", label='Fast Target Order')

    title = 'Running times of these Target Order and Fast Target Order on UPA graphs'
    plt.title(title)

    plt.xlabel('number of nodes')
    plt.ylabel('running time, sec')

    plt.legend(loc='upper right')
    plt.show()
        
    






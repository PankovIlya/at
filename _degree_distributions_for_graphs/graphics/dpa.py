""""
implement the DPA algorithm, compute a DPA graph
"""
import random, math
import matplotlib.pyplot as plt
import sys
sys.path.append("../../_degree_distributions_for_graphs")
import ddg



class DPATrial:
    """
    Simple class to encapsulate optimized trials for DPA algorithm
    """

    def __init__(self, num_nodes):
        """
        Initialize a DPATrial object corresponding to a 
        complete graph with num_nodes nodes
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in xrange(num_nodes) for _ in xrange(num_nodes)]


    def run_trial(self, num_nodes):
        """
        Conduct num_node trials using by applying random.choice()
        to the list of node numbers
        """
        new_node_neighbors = set()
        for _ in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))

        self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))
        
        self._num_nodes += 1
        return new_node_neighbors



def dpa(m, n):
    graph = ddg.make_complete_graph(m)
    in_dpa = DPATrial(m)

    for idx in xrange(m, n):
        graph[idx] = in_dpa.run_trial(m)     
            
    return graph

if __name__ == "__main__":

    n = 28000 #all nodes
    m = 13 # mx is an integer that is close to the average out-degree of the physics citation graph.

    graph = dpa(m, n)

    in_degre_distrib = ddg.in_degree_distribution(graph)
    norm_degree_distr = ddg.norm_degree_distribution(in_degre_distrib)
    graph = norm_degree_distr

    mx = sum(x*graph[x] for x in graph)
    sigma = sum(((x - mx)**2)*graph[x] for x in graph)**0.5
    print mx, sigma

    plt.loglog(norm_degree_distr.keys(), norm_degree_distr.values(), 'o')
    plt.title('loglog plot of DPA normalized in-degree distribution, n = {}, m = {}'.format(n, m))
    plt.xlabel('in-degree')
    plt.ylabel('normalized distribution')
    plt.show()

    





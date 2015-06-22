""" Connected components and graph resilience """
#import dsu
#import data
import urllib2
import random

class DSU (object):
    """ disjoint-set data structure """
    
    def __init__(self):
        """ init """
        self._dsu = {}
        self._head = {}
        self._count = 0

    def cmax(self, cnt):
        """ check max count """
        if self._count < cnt:
            self._count = cnt

    def count(self):
        """ count set connected components """
        return self._count

    def make(self, node):
        """ set head """
        self._dsu[node] = node
        self._head[node] = 1
        self.cmax(self._head[node])

    def add(self, node, parent):
        """ add node """ 
        self._dsu[node] = parent
        self._head[parent] = +1
        self.cmax(self._head[parent])
          
    def find(self, node):
        """ find head on node """
        if node not in self._dsu:
            return None
        
        return self._find(node)

    def _find(self, node):
        """ find head on node """
        if self._dsu[node] == node:
            return node
        else:
            return self._find(self._dsu[node])


    def join(self, node1, node2):
        """ join two cc """
        head1 = self.find(node1)
        head2 = self.find(node2)

        #print 'head1', head1, 'head2', head2, 'dsu', self._dsu 
        
        if head1 == head2:
            return head1
        
        if random.randint(0,1):
            tmp = head1
            head1 = head2
            head2 = tmp

        self._dsu[head2] = head1
        self._head[head1] += self._head[head2]
        del self._head[head2]
        self.cmax(self._head[head1])
        
        return head1


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
    dsu = DSU()
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


NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"


def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Returns a dictionary that models a graph
    """
    graph_file = urllib2.urlopen(graph_url)
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

NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"
ugraph = load_graph(NETWORK_URL)

print 'LOAD'
print compute_resilience2(ugraph, [22, 50, 114, 136, 210, 4, 6, 8])
#(alg_module2_graphs.GRAPH2, [1, 3, 5, 7, 2, 4, 6, 8]) expected [8, 7, 6, 5, 1, 1, 1, 1, 0]




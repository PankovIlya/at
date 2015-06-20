import urllib2, math, ddg, pda
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"

def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Returns a dictionary that models a graph
    """
    graph_file = open("alg_phys-cite.txt")
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

citation_graph = load_graph(CITATION_URL)
in_degre_distrib = ddg.in_degree_distribution(citation_graph)
norm_degree_distr = ddg.norm_degree_distribution(in_degre_distrib)
norm1 =  [(x, in_degre_distrib[x]) for x in in_degre_distrib]
norm1.sort()
norm = map(lambda x: (math.log10(x[0]),x[1]) if x[0] else (x[0],x[1]), norm1)
norm = map(lambda x: (x[0], math.log10(x[1])) if x[1] else (x[0],x[1]), norm) 
graph = norm
mx = sum([x[0]*1.0*x[1] for x in graph])/sum([y[1] for y in graph])
sigma = (sum([(x[0] - mx)**2 for x in graph])/len(graph))**0.5
print mx, sigma, len(citation_graph), sum([y[1] for y in graph])
arry = mlab.normpdf(np.array([x[0] for x in norm]), mx, sigma)

plt.loglog([x[0] for x in norm1], arry)
#pltloglog(norm_degree_distr.keys(), norm_degree_distr.values(), 'o')

plt.title('loglog plot of Citation normalized in-degree distribution')
plt.xlabel('in-degree')
plt.ylabel('normalized distribution')
plt.show()



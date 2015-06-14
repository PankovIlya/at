import urllib2, math, ddg, dpa
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
graph = dpa.dpa(13,28000)
dpa_in_degre_distrib = ddg.in_degree_distribution(graph)
dpa_norm_degree_distr = ddg.norm_degree_distribution(dpa_in_degre_distrib)



citation_graph = load_graph(CITATION_URL)
in_degre_distrib = ddg.in_degree_distribution(citation_graph)
norm_degree_distr = ddg.norm_degree_distribution(in_degre_distrib)
graph = in_degre_distrib
mx = sum([x*1.0*graph[x] for x in graph])/sum(graph.values())
sigma = (sum([(x - mx)**2 for x in graph])/len(graph.values()))**0.5
print mx, sigma, len(citation_graph)

_, dpa =  plt.subplots()
cit = dpa.twinx()

dpa.loglog(dpa_norm_degree_distr.keys(), dpa_norm_degree_distr.values(), 'bo')
cit.loglog(norm_degree_distr.keys(), norm_degree_distr.values(), 'ro')
plt.title('loglog plot of DPA & Citation normalized in-degree distribution, n = 28000, m = 13')
dpa.set_xlabel('in-degree', color = 'k')
dpa.set_ylabel('dpa normalized distribution', color = 'b')
cit.set_ylabel('citation normalized distribution', color='r')
plt.show()



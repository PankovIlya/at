import urllib2, math, ddg
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

#citation_graph = load_graph(CITATION_URL)

citation_graph = ddg.make_complete_graph_p(10000, 0.1)
#citation_graph = pda.pda_alg(50, 28000)
in_degre_graphs = ddg.in_degree_distribution(citation_graph)

print in_degre_graphs

sumd = sum(in_degre_graphs.values())

#print in_degre_graphs[0]*1.0/sumd, in_degre_graphs[1]*1.0/sumd 

arr = []
arr2 = []
sumlog2 = 0.0
for node in in_degre_graphs:
    val = in_degre_graphs[node]*1.0
    val1 = val/sumd
    if val1:
        val1 = math.log10(val1)
    sumlog2 += val
    if node:
        arr.append((math.log10(node), val1))
        arr2.append((node, val))
    else:
        arr.append((node, val1))
        arr2.append((node, val))

arr.sort()
arr2.sort()
sumlog = sum([y[1] for y in arr2])
print sumd, sumlog, sumlog2

mu = 0.0
for mi in arr2:
    mu += mi[0]*mi[1] 

mu = mu*1.0/sumd

sigma = math.pow(sum([math.pow(xi[0]-mu,2) for xi in arr2])/len(arr2),0.5)


print mu, sigma



        
#x = np.arange(0, 5, 0.1);
#y = np.sin(x)
 

# example data
#mu = 100 # mean of distribution
#sigma = 15 # standard deviation of distribution
#x = mu + sigma * np.random.randn(10000)

#num_bins = 50
# the histogram of the data
#n, bins, patches = plt.hist(x, num_bins, normed=1, facecolor='green', alpha=0.5)
# add a 'best fit' linens
#print bins
twin, ax1 = plt.subplots()
ax2 = ax1.twinx()
arrx = np.array([x[0] for x in arr])
arry = np.array([y[1] for y in arr])
yp = mlab.normpdf(np.array([x[0] for x in arr2]), mu, sigma)
#yp = map(lambda x : x if x else x, yp) 
yp = map(lambda x : math.log10(x) if x else x, yp) 
ax1.plot([x[0] for x in arr], [y[1] for y in arr], 'o')
ax2.plot([x[0] for x in arr], yp) 
#plt.xlabel('Smarts')
#plt.ylabel('Probabiliy')
#plt.title(r'Histogram of IQ: $\mu=100$, $\sigma=15$')

# Tweak spacing to prevent clipping of ylabel
#plt.subplots_adjust(left=0.15)
plt.show()



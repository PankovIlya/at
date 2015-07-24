import clustering as cl
import math, random
import matplotlib.pyplot as plt



for cnt in xrange(200)
    clusters = cl.gen_random_clusters(cnt)
    clusters

count = [x for x in xrange(len(atack))]

plt.plot(count, cn_cr[1:], "r", label='Computer Network')
plt.plot(count, er_cr[1:], "b",  label='ER')
plt.plot(count, upa_cr[1:], "g", label='UPA')

title = 'Resilience of the graph, with random choice, n = {0} , p = {1}, m = {2}'.format(cnt, p, int(mx))
plt.title(title)

plt.xlabel('number of removed nodes')
plt.ylabel('the size of the largest connected component')

plt.legend(loc='upper right')
plt.grid(True)
plt.show()

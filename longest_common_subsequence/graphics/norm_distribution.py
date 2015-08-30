import sys
sys.path.append('../../longest_common_subsequence')
import compute_alignment as ca 
import compare_protein as cp
import matplotlib.pyplot as plt
import load_data as ld


scores_m = ld.read_scoring_matrix(ld.PAM50_URL)
human = ld.read_protein(ld.HUMAN_EYELESS_URL)
fruitfly = ld.read_protein(ld.FRUITFLY_EYELESS_URL)
consesus = ld.read_protein(ld.CONSENSUS_PAX_URL)
amino = "ACBEDGFIHKMLNQPSRTWVYXZ"

print "generate null distribution:"
distribution = cp.generate_null_distribution(human,
                                             fruitfly,
                                             scores_m, 1000)

lmatrix = ca.compute_alignment_matrix(human, fruitfly, scores_m, False)
cmp_hf = ca.compute_local_alignment(human, fruitfly, scores_m, lmatrix)

mx = sum([distribution[scor]*scor for scor in distribution])
sigma = (sum([((scor-mx)**2)*distribution[scor] for scor in distribution]))**0.5
zfactor = (cmp_hf[0] - mx)*1.0/sigma

print mx, sigma, zfactor, 1.0/(zfactor**2)

inf = "mx = " + str(mx) + "\n sigma = " + str(sigma) + "\n z = " + str(zfactor)

fig, ax = plt.subplots()
rects1 = plt.bar(distribution.keys(), distribution.values(), label = inf)

plt.legend(loc='upper right')
plt.xlabel('scores')
plt.ylabel('normalized distribution')
plt.title('Distribution scores for the local alignment of \n Human Eyeless Protein and Random Fruitfly Eyeless Protein ')
plt.show()

import sys
sys.path.append('../../4_longest_common_subsequence')
import compute_alignment as ca 
import compare_protein as cp
import matplotlib.pyplot as plt
import data.load_data as ld

scores_m = ld.read_scoring_matrix(ld.PAM50_URL)
human = ld.read_protein(ld.HUMAN_EYELESS_URL)
fruitfly = ld.read_protein(ld.FRUITFLY_EYELESS_URL)
consesus = ld.read_protein(ld.CONSENSUS_PAX_URL)

amino = "ACBEDGFIHKMLNQPSRTWVYXZ"

print 'generate null distribution (wait 5 min)'
distribution = cp.generate_null_distribution(human,
                                             fruitfly,
                                             scores_m, 500)


lmatrix = ca.compute_alignment_matrix(human, fruitfly, scores_m, False)
cmp_hf = ca.compute_local_alignment(human, fruitfly, scores_m, lmatrix)

mx = sum(distribution[scor]*scor for scor in distribution)
sigma = sum(((scor-mx)**2)*distribution[scor] for scor in distribution)**0.5
zfactor = (cmp_hf[0] - mx)*1.0/sigma

inf = "mx = {} sigma = {} z = {}".format(mx, sigma, zfactor)

fig, ax = plt.subplots()
rects1 = plt.bar(distribution.keys(), distribution.values(), label = inf)

plt.legend(loc='upper right')
plt.xlabel('scores')
plt.ylabel('normalized distribution')
plt.title('Distribution scores for the local alignment of \n Human Eyeless Protein and Random Fruitfly Eyeless Protein ')
plt.show()

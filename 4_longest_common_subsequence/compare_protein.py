"""
Compare Human Eyeless Protein and Fruitfly Eyeless Protein
Consensus PAX Domain contains a "consensus" sequence of the PAX domain;
that is, the sequence of amino acids in the PAX domain in any organism. 
"""

import random

import compute_alignment as ca


def compare_protein(protein1, protein2, base, scores):
    """ compare two protein """
    lmatrix = ca.compute_alignment_matrix(protein1, protein2, scores, False)
    cmp_hf = ca.compute_local_alignment(protein1, protein2, scores, lmatrix)

    remove_dash = lambda g: g != '-'

    xseq = filter(remove_dash, cmp_hf[1])
    yseq = filter(remove_dash, cmp_hf[2])

    ghmatrix = ca.compute_alignment_matrix(xseq, base, scores, True)
    cmp_xp = ca.compute_global_alignment(xseq, base, scores, ghmatrix)

    gfmatrix = ca.compute_alignment_matrix(yseq, base, scores, True)
    cmp_yp = ca.compute_global_alignment(yseq, base, scores, gfmatrix)

    return sum(1 for x, y in zip(cmp_xp[1], cmp_xp[2]) if x == y)*1.0/len(cmp_xp[1]), \
           sum(1 for x, y in zip(cmp_yp[1], cmp_yp[2]) if x == y)*1.0/len(cmp_yp[1])

def generate_null_distribution(seq_x, seq_y, scores, num_trials):
    """  statistical hypothesis testing """    
    rand_y = [x for x in seq_y]
    distribution = {}

    for num in xrange(num_trials):
        random.shuffle(rand_y)

        lmatrix = ca.compute_alignment_matrix(seq_x, rand_y, scores, False)
        cmp_hr = ca.compute_local_alignment(seq_x, rand_y, scores, lmatrix)

        score = cmp_hr[0]

        distribution.setdefault(score, 0)
        distribution[score] += 1

    sum_val = sum(distribution.values())
    return dict((itm, distribution[itm]*1.0/sum_val) for itm in distribution)

    
if __name__ == "__main__":

    import data.load_data as ld

    scores_m = ld.read_scoring_matrix(ld.PAM50_URL)
    human = ld.read_protein(ld.HUMAN_EYELESS_URL)
    fruitfly = ld.read_protein(ld.FRUITFLY_EYELESS_URL)
    consesus = ld.read_protein(ld.CONSENSUS_PAX_URL)
    amino = "ACBEDGFIHKMLNQPSRTWVYXZ"

    lenh, lenf, lena = len(human), len(fruitfly), len(amino)

    print compare_protein(human, fruitfly, consesus, scores_m)




    
    






    


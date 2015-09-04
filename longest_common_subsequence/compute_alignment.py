# -*- coding: utf-8 -*-
""" use of dynamic programming in measuring the similarity between two sequences of characters
    Given an alphabet Σ and a scoring matrix M defined over Σ∪{′−′},
    the dynamic programming method computed a score that measured the similarity
    of two sequences X and Y based on the values of this scoring matrix.
"""



def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    """ build scoring matrix """
    scores = {}
    for itm1 in alphabet:
        sub_scores = {}
        for itm2 in alphabet:
            if itm1 == itm2:
                sub_scores[itm2] = diag_score
            else:
                sub_scores[itm2] = off_diag_score
        sub_scores['-'] = dash_score
        scores[itm1] = sub_scores

    sub_scores = {}
    for itm in alphabet:
        sub_scores[itm] = dash_score
    sub_scores['-'] = dash_score

    scores['-'] = sub_scores

    return scores

def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
    """ compute global or local alignment matrix """
    cam = [[0 for _ in xrange(len(seq_y)+1)] for _ in xrange(len(seq_x)+1)]

    cam[0][0] = 0
    
    for idx in xrange(1, len(seq_x)+1):
        score = cam[idx-1][0] + scoring_matrix[seq_x[idx-1]]['-']

        if not global_flag and score < 0:
            score = 0

        cam[idx][0] = score

    for idy in xrange(1, len(seq_y)+1):
        score = cam[0][idy-1] + scoring_matrix['-'][seq_y[idy-1]]

        if not global_flag and score < 0:
            score = 0

        cam[0][idy] = score
        
    for idx in xrange(1,len(seq_x)+1):
        for idy in xrange(1,len(seq_y)+1):
            cxy = cam[idx-1][idy-1] + scoring_matrix[seq_x[idx-1]][seq_y[idy-1]]
            cx_ = cam[idx-1][idy] + scoring_matrix[seq_x[idx-1]]['-']
            c_y = cam[idx][idy-1] + scoring_matrix['-'][seq_y[idy-1]]

            score = max([cxy, cx_, c_y])

            if not global_flag and score < 0:
                score = 0

            cam[idx][idy] = score
            
    return cam

def levenshtein_distance(seq_x, seq_y):
    """ compute global or local alignment matrix """

    cam = [0] 

        
    if seq_x < seq_y:
        seq_x, seq_y = seq_y, seq_x 

    lx, ly = len(seq_x), len(seq_y)

    for j in xrange(1, ly+1):
        cam.append(j)

    change = lambda a, b:  0 if a == b else 1

    for i in xrange(1, lx+1):
        current = [i]
        for j in xrange(1, ly+1):
            cxy = cam[j-1] + change(seq_x[i-1], seq_y[j-1]) 
            cx_ = current[j-1] + 1
            c_y = cam[j] +1

            score = min([cxy, cx_, c_y])

            current.append(score)

        cam = current
            
    return cam[ly]


def compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """compute global alignment """ 
    idx, idy = len(seq_x), len(seq_y)
    alx, aly = '', ''
    
    
    while idx > 0 and idy > 0:
        if alignment_matrix[idx][idy] == alignment_matrix[idx-1][idy-1] + scoring_matrix[seq_x[idx-1]][seq_y[idy-1]]:
            alx, aly = seq_x[idx-1] + alx, seq_y[idy-1] + aly
            idx -= 1
            idy -= 1
        elif alignment_matrix[idx][idy] == alignment_matrix[idx-1][idy] + scoring_matrix[seq_x[idx-1]]['-']:
            alx, aly = seq_x[idx-1] + alx, '-' + aly
            idx -= 1
        else: #alignment_matrix[idx][idy] == alignment_matrix[idx][idy-1] + scoring_matrix['-'][seq_y[idy-1]]:
            alx, aly = '-' + alx, seq_y[idy-1] + aly
            idy -= 1
     
    for idi in xrange(idx, 0, -1):
        alx, aly = seq_x[idi-1] + alx, '-' + aly

    for idi in xrange(idy, 0, -1):
        alx, aly = '-' + alx, seq_y[idi-1] + aly
        
    score = 0
    for idx, idy in zip(alx, aly):
        score += scoring_matrix[idx][idy]

    return (score, alx, aly)


def max_alignment_matrix(lenx, leny, alignment_matrix):
    """ find start max for alignment_matrix"""
    res = (0, lenx, leny)
    for idx in xrange(lenx,0,-1):
        for idy in xrange(leny,0,-1):
            if alignment_matrix[idx][idy] > res[0]:
                res = (alignment_matrix[idx][idy], idx, idy)
    return res[1], res[2]


def compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """compute local alignment"""
    idx, idy = max_alignment_matrix(len(seq_x), len(seq_y), alignment_matrix)
    alx, aly = '', ''

    while idx > 0 and idy > 0:
        if alignment_matrix[idx][idy] == alignment_matrix[idx-1][idy-1] + scoring_matrix[seq_x[idx-1]][seq_y[idy-1]]:
            alx, aly = seq_x[idx-1] + alx, seq_y[idy-1] + aly
            idx -= 1
            idy -= 1
        elif alignment_matrix[idx][idy] == alignment_matrix[idx-1][idy] + scoring_matrix[seq_x[idx-1]]['-']:
            alx, aly = seq_x[idx-1] + alx, '-' + aly
            idx -= 1
        elif alignment_matrix[idx][idy] == alignment_matrix[idx][idy-1] + scoring_matrix['-'][seq_y[idx-1]]:
            alx, aly = '-' + alx, seq_y[idy-1] + aly
            idy -= 1
        else:
            break
        
    score = 0
    for idx, idy in zip(alx, aly):
        score += scoring_matrix[idx][idy]

    return (score, alx, aly)

def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    """ build scoring matrix """
    scores = {}
    for itm1 in alphabet:
        sub_scores = {}
        for itm2 in alphabet:
            if itm1 == itm2:
                sub_scores[itm2] = diag_score
            else:
                sub_scores[itm2] = off_diag_score
        sub_scores['-'] = dash_score
        scores[itm1] = sub_scores

    sub_scores = {}
    for itm in alphabet:
        sub_scores[itm] = dash_score
    sub_scores['-'] = dash_score

    scores['-'] = sub_scores

    return scores

if __name__ == "__main__":
    scores = build_scoring_matrix(set(['A','T']), 10, 4, -6)
    print scores
    g_matrix = compute_alignment_matrix('AA','TAAT', scores, True)
    l_matrix = compute_alignment_matrix('AA','TAAT', scores, False)
    print g_matrix
    print l_matrix
    print compute_global_alignment('AA','TAAT', scores, g_matrix)
    print compute_local_alignment('AA','TAAT', scores, l_matrix)
    scores = build_scoring_matrix(set(['A','T']), -6, 0, 6)
    print scores
    g_matrix = compute_alignment_matrix('AA','TA', scores, True)
    print g_matrix
    print compute_global_alignment('AA','TA', scores, g_matrix)

    a, b = 'BBAAYYY', 'BSBSAYY' 
    m_levenshtein_distance = build_scoring_matrix(set(a+b), 2, 1, 0)
    lg_matrix = compute_alignment_matrix(a,b, m_levenshtein_distance, True)
    global_levenshtein = compute_global_alignment(a,b, m_levenshtein_distance, lg_matrix)
    print global_levenshtein, len(a), len(b), len(a) + len(b) - global_levenshtein[0]
    print levenshtein_distance(a, b)





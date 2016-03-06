"""
  Spelling Corrector - ngramms method
  see optimized ngramms method - o_ngramms.py
  see ngramms_test.py
"""

import heapq
import compute_alignment as ca
import data.load_data as ld


def get_ngramms3(word):
    """ create ngramms """
    extended_word = word
    if len(word) <= 5:
        extended_word = '_' + extended_word + '_'

    return set([extended_word[i:i+3] for i in xrange(len(extended_word)-2)])

def create_ngramms(odictionary):
    """ create ngramms dict """
    ngramms = {}
    for word in odictionary:
        for ngramm in get_ngramms3(word):
            ngramms.setdefault(ngramm, set([]))
            ngramms[ngramm].add(word)
    return ngramms    


def find_word(checked_word, ng_dict):
    """ create ngramms of checked_word
        find in ngramms dict
        calc levenshtein distance
    """
    
    in_ng_dict = set([])
    best = []

    ngramms = get_ngramms3(checked_word)
    
    for ng in ngramms:
        in_ng_dict = in_ng_dict | ng_dict.get(ng, set([]))

    print "number of words after find ngramms {}".format(len(in_ng_dict))
        
    for word in in_ng_dict:
        # realy levenshtein distance
        score = ca.levenshtein_distance(checked_word, word)

        heapq.heappush(best, (1.0/(score + 1), word))
        if len(best) > 5:
            heapq.heappop(best)


    best.sort(reverse=True)        
    return best




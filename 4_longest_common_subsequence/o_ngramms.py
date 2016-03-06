"""
  Spelling Corrector - optimized ngramms method
  see ngramms_test.py
"""


import heapq

import compute_alignment as ca

#import redis
#r = redis.StrictRedis(host='localhost', port=6379, db=0)



def o_get_ngramms3(word):
    """ create ngramms """
    extended_word = word
    if len(word) <= 5:
        extended_word = '_' + extended_word + '_'

    #extended_word = '_' + word + '_'

    return [extended_word[i:i+3] for i in xrange(len(extended_word)-2)]

def o_create_ngramms(odictionary):
    """ create ngramms dict """
    def add_word (n, ng, sword):
        ngramms.setdefault(n, {})
        ngramms[n].setdefault(ng, set([]))
        ngramms[n][ng].add(sword)
        #r.rpush(str(n) + ng, sword)
        
    ngramms = {}
    for word in odictionary:
        word_ng = o_get_ngramms3(word)

        if not word_ng:
            continue


        for n, ngramm in enumerate(word_ng):
            for i in xrange(max(0, n-1), n+2):
                add_word(i, ngramm, word)


    return ngramms    

def o_find_word(checked_word, ng_dict):
    """ create ngramms of checked_word
        find in ngramms dict
        calc levenshtein distance
    """
    
    in_ng_dict = set([])
    best = []

    ngramms = o_get_ngramms3(checked_word)
      
    i, n = 0, len(checked_word) -1

    for i, ng in enumerate(ngramms):
        sub_dict = ng_dict.get(i, None)
        if sub_dict:
            in_ng_dict = in_ng_dict | sub_dict.get(ng, set([]))


    print "number of words after find ngramms {}".format(len(in_ng_dict)) # str()
            
    for word in in_ng_dict:
        # realy levenshtein distance
        score = ca.levenshtein_distance(checked_word, word)

        heapq.heappush(best, (1.0/(score + 1), word))
        if len(best) > 5:
            heapq.heappop(best)


    best.sort(reverse=True)        
    return best


    # def get_ng(n, ng):
    #     words = r.lrange(str(n)+ng, 0, -1)
    #     if not words:
    #         words = []
    #     return set(words)


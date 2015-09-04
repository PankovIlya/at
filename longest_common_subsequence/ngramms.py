import heapq
import load_data as ld
import compute_alignment as ca



def get_ngramms3(word):
    """ create ngramms """
    extended_word = '_' + word + '-'
    return set([extended_word[i:i+3] for i in xrange(len(extended_word)-2)])

def dict_ngramms(odictionary):
    """ create ngramms dict """
    ngramms = {}
    for word in odictionary:
        for ngramm in get_ngramms3(word):
            ngramms.setdefault(ngramm, set([]))
            ngramms[ngramm].add(word)
    return ngramms    

def find_ng (checked_word, ng_dict, distance):
    """ create ngramms of checked_word
        find in ngramms dict
        calc levenshtein distance
    """
    
    in_ng_dict = set([])
    best = []

    ngramms = get_ngramms3(checked_word)
    
    for ng in ngramms:
        in_ng_dict = in_ng_dict | ng_dict.get(ng, set([]))

    print "number of words after find ngramms" + str(len(in_ng_dict))
        
    for word in in_ng_dict:
        # levenshtein distance
        lg_matrix = ca.compute_alignment_matrix(checked_word, word, distance, True)
        score = ca.compute_global_alignment(checked_word, word, distance, lg_matrix)[0]

        heapq.heappush(best, (1.0/(len(checked_word) + len(word) - score + 1), word))

        if len(best) > 5:
            heapq.heappop(best)


    best.sort(reverse=True)        
    return best

def find_ng_l (checked_word, ng_dict):
    """ create ngramms of checked_word
        find in ngramms dict
        calc levenshtein distance
    """
    
    in_ng_dict = set([])
    best = []

    ngramms = get_ngramms3(checked_word)
    
    for ng in ngramms:
        in_ng_dict = in_ng_dict | ng_dict.get(ng, set([]))

    print "number of words after find ngramms" + str(len(in_ng_dict))
        
    for word in in_ng_dict:
        # realy levenshtein distance
        score = ca.levenshtein_distance(checked_word, word)

        heapq.heappush(best, (1.0/(score + 1), word))
        if len(best) > 5:
            heapq.heappop(best)


    best.sort(reverse=True)        
    return best

if __name__ == "__main__":

    import time

    dictionary = set(ld.read_words(ld.WORD_LIST_URL))
    dictionary.add('cotok')
    dictionary.add('synchrophasotrone')
    _alphabet = 'qwertyuiopasdfghjklzxcvbnm'
    
    ng_dict = dict_ngramms(dictionary)
    m_levenshtein_distance = ca.build_scoring_matrix(_alphabet, 2, 1, 0)

    def runtimes(check_word, correct_word):
        print 'global alignment for levenstein'
        print 'check word "' + check_word + '" correct word "' + correct_word + '"'
        t = time.time()
        print 'O(n^2) top 5', find_ng(check_word, ng_dict, m_levenshtein_distance)
        print 'running time', time.time() - t
        t = time.time()
        print 'O(n) top 5', find_ng_l(check_word, ng_dict)
        print 'running time', time.time() - t
        print \
        

    runtimes('codok', 'cotok')
    runtimes('wirefqlye', 'firefly') 
    runtimes('fwre', 'fire')
    runtimes('fwre', 'fire')
    runtimes('zyncrqophayrne', 'synchrophasotrone')



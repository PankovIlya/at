import load_data as ld
import time
import compute_alignment as ca


_alphabet = 'qwertyuiopasdfghjklzxcvbnm'
alphabet = list(_alphabet) + ['']


def expansion(words, score):

    check_words = set([])
    
    if not score:
        return check_words

    for word in words:
        for var in xrange(len(word)+1):
            for char in alphabet:
                check_words.add(word[:var] + char + word[var+1:])
                check_words.add(word[:var] + char + word[var:])

    return check_words & dictionary or expansion(check_words, score-1)


def e_alg(words):
    check_words = set([words])    
    return check_words & dictionary or expansion(check_words, 3) or check_words


def liner_search(checked_word, dist):
    levenshtein_distance = ca.build_scoring_matrix(_alphabet, 2, 1, 0)
    result = []
    for word in dictionary:
        lg_matrix = ca.compute_alignment_matrix(checked_word, word, levenshtein_distance, True)
        score = ca.compute_global_alignment(checked_word, word, levenshtein_distance, lg_matrix)[0]
        if len(checked_word) + len(word) - score <= dist:
            result.append(word)
    return result

if __name__ == "__main__":

    dictionary = set(ld.read_words(ld.WORD_LIST_URL))

    def foo_time(foo, args):
        time1 = time.time() 
        return foo.__name__,  args[0], foo(*args), time.time() - time1 

    a = "humbyle" #1
    print foo_time(e_alg, [a])
    print foo_time(liner_search, [a, 1])
    b = "farefliy" #2
    print foo_time(e_alg, [b])
    print foo_time(liner_search, [b, 2])
    c = "firefliyqt" #3
    print foo_time(e_alg, [c])
    print foo_time(liner_search, [c, 3])
    print 'see module ngramms )'


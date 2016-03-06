import ngramms as ng
import o_ngramms as ong
import data.load_data as ld
import time, random

def random_dict():
    _alphabet = 'qwertyuiopasdfghjklzxcvbnm'
    ac = (5, 9)
    wc = 300000


    r_dict = set([])
    for n in xrange(*ac):
        for _ in xrange(wc):
            word = ''
            for _ in xrange(n):
                word += _alphabet[random.randint(0, len(_alphabet)-1)]
            r_dict.add(word)
    return r_dict


def _run(foo, word, ndict):
    t = time.time()
    top = foo(word, ndict)
    t = time.time() - t
    return t, top


def runtimes(check_word, correct_word):
    print 'check word "' + check_word + '" correct word "' + correct_word + '"'
    print 'running time {} ng method top 5 {}'.format(*_run(ng.find_word, check_word, ng_dict))
    print 'running time {} ong method top 5 {}'.format(*_run(ong.o_find_word, check_word, ong_dict))
    print \


if __name__ == '__main__':

    dictionary = set(ld.read_words(ld.WORD_LIST_URL))
    #dictionary = set([])

    dictionary.add('python')
    dictionary.add('flask')
    dictionary.add('synchrophasotrone')
    dictionary.add('levenshtein')
    dictionary.add('fire')
    dictionary.add('irrational')


    print 'extension dict'
    #dictionary = dictionary | random_dict()
    print 'len dict', len(dictionary)

    print 'creating ngramms'
    ng_dict = ng.create_ngramms(dictionary)
    print 'creating opt ngramms'
    ong_dict = ong.o_create_ngramms(dictionary)
    print \

    runtimes('pyton', 'python')
    runtimes('flesk', 'flask')
    runtimes('lefenshtain', 'levenshtein')
    runtimes('fzre', 'fire')
    runtimes('zyncrqophayrne', 'synchrophasotrone')
    runtimes('erationnal', 'irrational')


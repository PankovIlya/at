"""
Load Data
"""

import urllib2
import os



# URLs for data files
##PAM50_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_PAM50.txt"
##HUMAN_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_HumanEyelessProtein.txt"
##FRUITFLY_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_FruitflyEyelessProtein.txt"
##CONSENSUS_PAX_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_ConsensusPAXDomain.txt"
##WORD_LIST_URL = "http://storage.googleapis.com/codeskulptor-assets/assets_scrabble_words3.txt"


path = os.path.dirname(__file__)

PAM50_URL            = os.path.join(path, "alg_PAM50.txt")
HUMAN_EYELESS_URL    = os.path.join(path, "alg_HumanEyelessProtein.txt")
FRUITFLY_EYELESS_URL = os.path.join(path, "alg_FruitflyEyelessProtein.txt")
CONSENSUS_PAX_URL    = os.path.join(path, "alg_ConsensusPAXDomain.txt")
WORD_LIST_URL        = os.path.join(path, "assets_scrabble_words3.txt")



###############################################
# provided code

def read_scoring_matrix(filename):
    """
    Read a scoring matrix from the file named filename.  

    Argument:
    filename -- name of file containing a scoring matrix

    Returns:
    A dictionary of dictionaries mapping X and Y characters to scores
    """
    scoring_dict = {}
    #scoring_file = urllib2.urlopen(filename)
    scoring_file = open(filename)
    ykeys = scoring_file.readline()
    ykeychars = ykeys.split()
    for line in scoring_file.readlines():
        vals = line.split()
        xkey = vals.pop(0)
        scoring_dict[xkey] = {}
        for ykey, val in zip(ykeychars, vals):
            scoring_dict[xkey][ykey] = int(val)
    return scoring_dict




def read_protein(filename):
    """
    Read a protein sequence from the file named filename.

    Arguments:
    filename -- name of file containing a protein sequence

    Returns:
    A string representing the protein
    """
    #protein_file = urllib2.urlopen(filename)
    protein_file = open(filename)
    protein_seq = protein_file.read()
    protein_seq = protein_seq.rstrip()
    return protein_seq


def read_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    # load assets
    #word_file = urllib2.urlopen(filename)
    word_file = open(filename)
    
    # read in files as string
    words = word_file.read()
    
    # template lines and solution lines list of line string
    word_list = words.split('\n')
    print "Loaded a dictionary with", len(word_list), "words"
    return word_list




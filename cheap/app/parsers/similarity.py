__author__ = 'vantani'
#http://stackoverflow.com/questions/653157/a-better-similarity-ranking-algorithm-for-variable-length-strings
def get_bigrams(string):
    '''
    Takes a string and returns a list of bigrams
    '''
    s = string.lower()
    return [s[i:i+2] for i in xrange(len(s) - 1)]

def string_similarity(str1, str2):
    '''
    Perform bigram comparison between two strings
    and return a percentage match in decimal form
    '''
    pairs1 = get_bigrams(str1.lower().strip())
    pairs2 = get_bigrams(str2.lower().strip())
    union  = len(pairs1) + len(pairs2)
    hit_count = 0
    for x in pairs1:
        for y in pairs2:
            if x == y:
                hit_count += 1
                break
    return (2.0 * hit_count) / union

if __name__ == "__main__":
    '''
    Run a test using the example taken from:
    http://www.catalysoft.com/articles/StrikeAMatch.html
    '''
    w1 = 'algorithms'
    words = ['The Algorithm Design Manual', 'Distributed Computing South Asian Edition: Principles, Algorithms, and Systems', 'ALGORITHMS', 'Programming Problems: Advanced Algorithms', 'Data Structures and Algorithms Made Easy : Second Edition: Data Structure and Algorithmic Puzzles', 'Sold']

    for w2 in words:
        print('Healed --- ' + w2)
        print(string_similarity(w1, w2))
        print

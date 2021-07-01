"""Spelling Corrector in Python 3; see http://norvig.com/spell-correct.html

Copyright (c) 2007-2016 Peter Norvig
MIT license: www.opensource.org/licenses/mit-license.php
"""

################ Spelling Corrector 

import re
from collections import Counter

def words(text): return re.findall(r'\w+', text.lower())

file = open('E:\\big.txt', 'r', encoding='utf8')

WORDS = Counter(words(file.read()))

def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return WORDS[word] / N

def correction(word): 
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

################ Test Code 

def unit_tests():
    assert correction('soletar') == 'soletrar'              # insert
    assert correction('korrijido') == 'corrigido'           # replace 2
    assert correction('bicikleta') == 'bicicleta'               # replace
    assert correction('incoveninent') == 'inconveniente'       # insert 2
    assert correction('arranjaddo') == 'arranjado'            # delete
    assert correction('poeisa') =='poesia'                  # transpose
    assert correction('pooiesa') =='poesia'                 # transpose + delete
    assert correction('palavra') == 'palavra'                     # known
    assert correction('quintessência') == 'quintessência'  # unknown
    assert words('Isso é um TESTE.') == ['isso', 'é', 'um', 'teste']
    assert Counter(words('Isso é um TESTE. 123; Um TESTE isso é.')) == (
           Counter({'123': 1, 'um': 2, 'é': 2, 'teste': 2, 'isso': 2}))
    assert len(WORDS) == 32192
    assert sum(WORDS.values()) == 1115504
    assert WORDS.most_common(10) == [
     ('o', 79808),
     ('de', 40024),
     ('e', 38311),
     ('para', 28765),
     ('em', 22020),
     ('um', 21124),
     ('que', 12512),
     ('ele', 12401),
     ('era', 11410),
     ('isso', 10681)]
    assert WORDS['o'] == 79808
    assert P('quintessential') == 0
    assert 0.07 < P('o') < 0.08
    return 'unit_tests pass'

def spelltest(tests, verbose=False):
    "Run correction(wrong) on all (right, wrong) pairs; report results."
    import time
    start = time.clock()
    good, unknown = 0, 0
    n = len(tests)
    for right, wrong in tests:
        w = correction(wrong)
        good += (w == right)
        if w != right:
            unknown += (right not in WORDS)
            if verbose:
                print('correction({}) => {} ({}); expected {} ({})'
                      .format(wrong, w, WORDS[w], right, WORDS[right]))
    dt = time.clock() - start
    print('{:.0%} of {} correct ({:.0%} unknown) at {:.0f} words per second '
          .format(good / n, n, unknown / n, n / dt))
    
def Testset(lines):
    "Parse 'right: wrong1 wrong2' lines into [('right', 'wrong1'), ('right', 'wrong2')] pairs."
    return [(right, wrong)
            for (right, wrongs) in (line.split(':') for line in lines)
            for wrong in wrongs.split()]

if __name__ == '__main__':
    print(unit_tests())
    spelltest(Testset(open('spell-testset1.txt')))
    spelltest(Testset(open('spell-testset2.txt')))

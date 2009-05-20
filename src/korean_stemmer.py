# -*- coding: utf-8 -*-

# (C) 2009 Dan Bravender

from korean_conjugator import *

def iterate_chop_last(string):
    for i in reversed(range(1, len(string))):
        yield string[0:-i]
    yield string

def generate_stems(verb):
    yield (False, verb[:-1] + join(lead(verb[-1]), u'ㅣ'))
    yield (True, verb)
    for p in [u'ᆸ',u'ᆯ', u'ᆺ']:
        yield (False, verb[:-1] + join(lead(verb[-1]), vowel(verb[-1]), p))
    yield (False, verb[:-1] + join(lead(verb[-1]), vowel(verb[-1])))

def stem(verb):
    # remove all conjugators that return what was passed in
    results = []
    ignore_indicies = [i for (i, conj) in \
                       enumerate(conjugation.perform('test')) \
                       if conj[1] == 'test']
    for possible_base_stem in iterate_chop_last(verb):
        for (original, possible_stem) in generate_stems(possible_base_stem):
            if verb in [x[1] for (i, x) in \
                        enumerate(conjugation.perform(possible_stem)) \
                        if (i not in ignore_indicies) or not original]:
                return possible_stem + u'다'
    return list(set(results))

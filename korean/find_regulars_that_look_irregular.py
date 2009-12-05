# -*- coding: utf-8 -*-

from conjugator import *
import time

import sqlite3

c = sqlite3.connect('korean_verbs.sqlite3')

def is_s_irregular(infinitive):
    return match(base(infinitive)[-1], u'*', u'*', u'ᆺ')

def is_l_irregular(infinitive):
    return match(base(infinitive)[-1], u'ᄅ', u'ㅡ', None)

def is_h_irregular(infinitive):
    return (padchim(base(infinitive)[-1]) == u'ᇂ' or base(infinitive)[-1] == u'러')

def is_p_irregular(infinitive):
    return match(base(infinitive)[-1], u'*', u'*', u'ᆸ')

def is_d_irregular(infinitive):
    return match(base(infinitive)[-1], u'*', u'*', u'ᆮ')

irregular_types = {
    u'ㅅ irregular': is_s_irregular,
    u'ㄹ irregular': is_l_irregular,
    u'ㅎ irregular': is_h_irregular,
    u'ㅂ irregular': is_p_irregular,
    u'ㄷ irregular': is_d_irregular
}

both_regular_and_irregular = [
    u'일다',
    u'곱다',
    u'파묻다',
    u'누르다',
    u'묻다',
    u'이르다',
    u'되묻다',
    u'썰다',
    u'붓다',
    u'들까불다',
    u'굽다',
    u'걷다',
    u'뒤까불다',
    u'이다',
    u'까불다'
]

from collections import defaultdict
results = defaultdict(lambda: [])

data = c.execute('select infinitive.word, conj.word from entry infinitive inner join entry conj on conj.infinitive_id = infinitive.id and conj.verb_tense_id = 2 where infinitive.infinitive_id = 0').fetchall()

for infinitive, conjugated in data:
    if infinitive in both_regular_and_irregular:
        continue
    for irregular_name, func in irregular_types.iteritems():
        if func(infinitive):
            if declarative_present_informal_low(infinitive, True) == conjugated:
                results[u'not ' + irregular_name].append(infinitive[:-1])

# I just wanted to use pprint... but man... Python and unicode => :-(
# Python 3 makes me happy... unicode everywhere as it should be...
# but I can't use it everywhere yet ;-)

for key, value in results.iteritems():
    print "'%s': [%s]".encode('utf-8') % (key, ', '.join(map(lambda x:u"u'%s'" % x, list(set(value)))))


# -*- coding: utf-8 -*-

from korean_conjugator import *
import time

mappings = {
2: declarative_present_informal_low,
3: declarative_past_informal_low,
4: declarative_future_informal_low,
5: inquisitive_present_informal_low,
6: inquisitive_past_informal_low,
#7: inquisitive_future_informal_low,
#8: imperative_present_informal_low,
9: propositive_present_informal_low,
10: declarative_present_informal_high,
11: declarative_past_informal_high}

skips = [u'이러이러다', 
         u'곱다', # both regular and irregular
         u'걷다', # both regular and irregular
         u'묻다', # both regular and irregular
         u'굽다', # both regular and irregular
         u'붓다', # irregular is out of usage as far as I can tell
         u'늘어놓다', # orthographic variant is all that fails
         u'되묻다', # both regular and irregular
         u'파묻다', # both regular and irregular
         u'부릍다', # looks like a contraction of 부르트다
         u'및다', # contraction of 미치다
         u'뉘웇다', # contraction of 뉘우치다
         u'펴다', # entry looks wrong in the db
         u'켜다', # entry looks wrong
         u'여립켜다', # entry looks wrong
         u'실켜다', # entry looks wrong
         u'실켜다', # entry looks wrong
         u'들이켜다', # entry looks wrong
         u'날아예다', # looks old
         ]

import sqlite3

c = sqlite3.connect('korean_verbs.sqlite3')

check_verbs = ['기다', '지다', '가깝다', '적다', '남다', '가다', '내다', '만들다', '부르다', 
               '살다', '주다', '외우다', '보다', '까맣다', '애쓰다', '바르다', '뛰다', '되다', 
               '걷다', '하다', '오다', '잇다', '서다', '담그다', '쓰다', '눕다', '그러다', 
               '푸르다', '켜다', '낫다', '누르다', '깨닫다', '돕다', '아니다', '이다', '푸다']

for check_verb in check_verbs:
    for id, verb in ((x[0], x[1]) for x in c.execute('''select id, word from entry where infinitive_id = 0 and word = '%s' ''' % check_verb)):
        if verb in skips or verb.endswith(u'놓다'):
            continue
        conjugations = dict(((x[0], x[1]) for x in c.execute('select verb_tense_id, word from entry where infinitive_id = ' + str(id))))
        for id in mappings:
            from pprint import pprint
            try:
                print (u"""yield check, %s, u'%s', u'%s'""" % (mappings[id].__name__, verb, conjugations[id])).encode('utf-8')
            except KeyError:
                continue

#12: informal_high_declarative_future,
#13: informal_high_inquisitive_present,
#14: informal_high_inquisitive_past,
#15: informal_high_inquisitive_future,
#16: informal_high_imperative,
#17: informal_high_propositive,
#18: formal_low_declarative_present,
#19: formal_low_declarative_past,
#20: formal_low_declarative_future,
#21: formal_low_inquisitive_present,
#22: formal_low_inquisitive_past,
#23: formal_low_inquisitive_future,
#24: formal_low_imperative,
#25: formal_low_propositive,
#26: formal_high_declarative_present,
#27: formal_high_declarative_past,
#28: formal_high_declarative_future,
#29: formal_high_inquisitive_present,
#30: formal_high_inquisitive_past,
#31: formal_high_inquisitive_future,
#32: formal_high_imperative,
#33: formal_high_propositive}
#34|and [connective]
#35|or [connective]
#36|but [connective]
#37|so [connective]
#38|in order to [connective]
#39|if [connective]
#40|present [modifier]
#41|past [modifier]
#42|future [modifier]
#43|adverbial
#44|nominal
#45|honorific



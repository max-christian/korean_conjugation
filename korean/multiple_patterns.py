# -*- coding: utf-8 -*-

# (c) 2010 Dan Bravender - licensed under the AGPL 3.0

from hangeul_utils import *
from korean_conjugator import *
import time

import sqlite3

c = sqlite3.connect('korean_verbs.sqlite3')

verbs = {}

for id, verb, c_model in ((x[0], x[1], x[3]) for x in c.execute('select e1.id, e1.word, e1.conjugation_model, e2.word from entry e1 inner join entry e2 on e2.infinitive_id = e1.id and e2.verb_tense_id = 2 where e1.infinitive_id = 0')):
    models = verbs.get(verb.encode('utf-8'), [])
    if c_model.endswith(u'놔'):
        continue
    if len(models):
        try:
            new_x = merge(models[0][:-1], models[0][-1])
            if c_model != new_x:
                models.append(c_model)
        except:
            models.append(c_model)
    else:
        models.append(c_model)
    verbs[verb.encode('utf-8')] = list(set(models))

print (u"\n".join((x.decode('utf-8') + u' -- ' + u" ".join(y) for (x, y) in verbs.iteritems() if len(y) > 1))).encode('utf-8')

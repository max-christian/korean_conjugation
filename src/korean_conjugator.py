# -*- coding: utf-8 -*-

# (C) 2009 Dan Bravender

from hangeul_utils import *
from pprint import pformat

def no_padchim_rule(character):
    u'''no_padchim_rule is a helper function for defining merges where a 
        character will take the padchim of a merged character if the first 
        character doesn't already have a padchim, .e.g. 습 -> 가 + 습니다 -> 갑니다.
     '''
    def rule(x, y):
        if not padchim(x[-1]) and y[0] == character:
            return x[:-1] + join(lead(x[-1]), 
                                 vowel(x[-1]), 
                                 padchim(character)) + y[1:]
    return rule

def vowel_contraction(vowel1, vowel2, new_vowel):
    u'''vowel contraction is a helper function for defining common contractions 
        between a character without a padchim and a character that starts with 
        u'ᄋ', e.g. ㅐ + ㅕ -> ㅐ when applied to 해 + 였 yields 했.
     '''
    def rule(x, y):
        return match(x[-1], u'*', vowel1, None) and \
               match(y[0], u'ᄋ', vowel2) and \
               x[:-1] + join(lead(x[-1]), new_vowel, padchim(y[0])) + y[1:]
    return rule

# merge rules is a list of rules that are applied in order when merging a verb 
#             stem with a tense ending
merge_rules = []

# no padchim + 을
merge_rules.append(no_padchim_rule(u'을'))

# no padchim + 습, 읍
merge_rules.append(no_padchim_rule(u'습'))
merge_rules.append(no_padchim_rule(u'읍'))

# no padchim + 는
merge_rules.append(no_padchim_rule(u'는'))

# no padchim + 음
merge_rules.append(no_padchim_rule(u'음'))

# ㄹ irregular
# a true ㄹ pachim (not one that was converted from ㄷ -> ㄹ) is often 
merge_rules.append(lambda x, y: padchim(x[-1]) == u'ᆯ' and y[0] == u'는' and \
                   x[:-1] + join(lead(x[-1]), vowel(x[-1]), u'ᆫ') + y[1:])
merge_rules.append(lambda x, y: padchim(x[-1]) == u'ᆯ' and y[0] == u'습' and \
                   x[:-1] + join(lead(x[-1]), vowel(x[-1]), u'ᆸ') + y[1:])
merge_rules.append(lambda x, y: padchim(x[-1]) == u'ᆯ' and y[0] == u'읍' and \
                   x[:-1] + join(lead(x[-1]), vowel(x[-1]), u'ᆸ') + y[1:])
merge_rules.append(lambda x, y: padchim(x[-1]) == u'ᆯ' and y[0] == u'니' and \
                   x[:-1] + join(lead(x[-1]), vowel(x[-1])) + y)
merge_rules.append(lambda x, y: padchim(x[-1]) == u'ᆯ' and y[0] == u'세' and \
                   x[:-1] + join(lead(x[-1]), vowel(x[-1])) + y)
merge_rules.append(lambda x, y: padchim(x[-1]) == u'ᆯ' and y[0] == u'십' and \
                   x[:-1] + join(lead(x[-1]), vowel(x[-1])) + y)
merge_rules.append(lambda x, y: padchim(x[-1]) == u'ᆯ' and y[0] == u'을' and \
                   x + y[1:])
merge_rules.append(lambda x, y: padchim(x[-1]) == u'ᆯ' and y[0] == u'면' and \
                   x + y)
merge_rules.append(lambda x, y: padchim(x[-1]) == u'ᆯ' and y[0] == u'음' and \
                   join(lead(x[-1]), vowel(x[-1]), u'ᆱ'))

# vowel contractions
merge_rules.append(vowel_contraction(u'ㅐ', u'ㅓ', u'ㅐ'))
merge_rules.append(vowel_contraction(u'ㅡ', u'ㅓ', u'ㅓ'))
merge_rules.append(vowel_contraction(u'ㅜ', u'ㅓ', u'ㅝ'))
merge_rules.append(vowel_contraction(u'ㅗ', u'ㅏ', u'ㅘ'))
merge_rules.append(vowel_contraction(u'ㅚ', u'ㅓ', u'ㅙ'))
merge_rules.append(vowel_contraction(u'ㅘ', u'ㅓ', u'ㅘ'))
merge_rules.append(vowel_contraction(u'ㅝ', u'ㅓ', u'ㅝ'))
merge_rules.append(vowel_contraction(u'ㅏ', u'ㅏ', u'ㅏ'))
merge_rules.append(vowel_contraction(u'ㅡ', u'ㅏ', u'ㅏ'))
merge_rules.append(vowel_contraction(u'ㅣ', u'ㅓ', u'ㅕ'))
merge_rules.append(vowel_contraction(u'ㅓ', u'ㅓ', u'ㅓ'))
merge_rules.append(vowel_contraction(u'ㅔ', u'ㅓ', u'ㅔ'))
merge_rules.append(vowel_contraction(u'ㅕ', u'ㅓ', u'ㅕ'))
merge_rules.append(vowel_contraction(u'ㅏ', u'ㅕ', u'ㅐ'))

# 면 connective
merge_rules.append(lambda x, y: padchim(x[-1]) and y[0] == u'면' and \
                   x + u'으' + y)

# 세 command
merge_rules.append(lambda x, y: padchim(x[-1]) and y[0] == u'세' and \
                   x + u'으' + y)

# 십 command
merge_rules.append(lambda x, y: padchim(x[-1]) and y[0] == u'십' and \
                   x + u'으' + y)

# default rule - just append the contents
merge_rules.append(lambda x, y: x + y)

def apply_rules(x, y, verbose=False, rules=[]):
    u'''apply_rules concatenates every element in a list using the rules to 
        merge the strings
     '''
    for i, rule in enumerate(rules):
        output = rule(x, y)
        if output:
            if verbose:
                print("rule %03d: %s + %s => %s" % 
                      (i, pformat(x), pformat(y), pformat(output)))
            return output

merge = lambda x, y: apply_rules(x, y, rules=merge_rules, verbose=False)

class conjugation:
    u'''conjugation is a singleton decorator that simply builds a list of 
        all the conjugation rules
     '''
    def __init__(self):
        self.tenses = {}
        self.tense_order = []

    def perform(self, infinitive):
        u'''perform returns the result of the application of all of the
            conjugation rules on one infinitive
         '''
        results = []
        for tense in self.tense_order:
            results.append((tense, self.tenses[tense](infinitive)))
        return results

    def __call__(self, f):
        self.tense_order.append(f.__name__)
        self.tenses.update({f.__name__: f})
        return f

conjugation = conjugation()

@conjugation
def base(infinitive):
    if infinitive[-1] == u'다':
        return infinitive[:-1]
    else:
        return infinitive

@conjugation
def base2(infinitive):
    infinitive = base(infinitive)
    # ㅂ irregular
    if match(infinitive[-1], u'*', u'*', u'ᆸ') and vowel(infinitive[-1]) in [u'ㅗ', u'ㅜ']:
        return merge(infinitive[:-1] + join(lead(infinitive[-1]), 
                     vowel(infinitive[-1])),
                     join(u'ᄋ', vowel(infinitive[-1])))
    # ㄷ irregular
    elif match(infinitive[-1], u'*', u'*', u'ᆮ') and \
         infinitive not in [u'믿', u'받', u'얻', u'닫']:
        infinitive = Geulja(infinitive[:-1] + join(lead(infinitive[-1]), 
                                                   vowel(infinitive[-1]), 
                                                   u'ᆯ'))
        infinitive.original_padchim = u'ᆮ'
    elif match(infinitive[-1], u'*', u'*', u'ᆺ') and \
         infinitive not in [u'벗', u'웃', u'씻', u'빗']:
        infinitive = Geulja(infinitive[:-1] + join(lead(infinitive[-1]), 
                                                   vowel(infinitive[-1])))
        infinitive.hidden_padchim = True
    return infinitive

def base3(infinitive):
    infinitive = base(infinitive)
    if match(infinitive[-1], u'*', u'ㅗ', u'ᆸ'):
        return join(lead(infinitive[-1]), vowel(infinitive[-1])) + u'우'
    else:
        return base2(infinitive)

@conjugation
def declarative_present_informal_low(infinitive):
    infinitive = base2(infinitive)
    # 르 irregular
    if match(infinitive[-1], u'ᄅ', u'ㅡ'):
        new_ending = join(lead(infinitive[-2]), vowel(infinitive[-2]), u'ᆯ')
        if vowel(infinitive[-2]) in [u'ㅗ', u'ㅏ']:
            return infinitive[:-2] + merge(new_ending, u'라')
        else:
            return infinitive[:-2] + merge(new_ending, u'러')
    elif infinitive[-1] == u'하':
        return infinitive[:-1] + merge(infinitive[-1], u'여')
    elif vowel(infinitive[-1]) in [u'ㅗ', u'ㅏ']:
        return infinitive[:-1] + merge(infinitive[-1], u'아')
    else:
        return infinitive[:-1] + merge(infinitive[-1], u'어')

@conjugation
def declarative_present_informal_high(infinitive):
    return merge(declarative_present_informal_low(infinitive), u'요')

@conjugation
def declarative_present_formal_low(infinitive):
    return merge(base(infinitive), u'는다')

@conjugation
def declarative_present_formal_high(infinitive):
    return merge(base(infinitive), u'습니다')

@conjugation
def past_base(infinitive):
    ps = declarative_present_informal_low(infinitive)
    if vowel(ps[-1]) in [u'ㅗ', u'ㅏ']:
        return ps[:-1] + merge(ps[-1], u'았')
    else:
        return ps[:-1] + merge(ps[-1], u'었')

@conjugation
def declarative_past_informal_low(infinitive):
    return merge(past_base(infinitive), u'어')

@conjugation
def declarative_past_informal_high(infinitive):
    return merge(declarative_past_informal_low(infinitive), u'요')

@conjugation
def declarative_past_formal_low(infinitive):
    return merge(past_base(infinitive), u'다')

@conjugation
def declarative_past_formal_high(infinitive):
    return merge(past_base(infinitive), u'습니다')

@conjugation
def future_base(infinitive):
    return merge(base3(infinitive), u'을')

@conjugation
def declarative_future_informal_low(infinitive):
    return merge(future_base(infinitive), u' 거야')

@conjugation
def declarative_future_informal_high(infinitive):
    return merge(future_base(infinitive), u' 거예요')

@conjugation
def declarative_future_formal_low(infinitive):
    return merge(future_base(infinitive), u' 거다')

@conjugation
def declarative_future_formal_high(infinitive):
    return merge(future_base(infinitive), u' 겁니다')

@conjugation
def declarative_future_conditional_informal_low(infinitive):
    return merge(base(infinitive), u'겠어')

@conjugation
def declarative_future_conditional_informal_high(infinitive):
    return merge(base(infinitive), u'겠어요')

@conjugation
def declarative_future_conditional_formal_low(infinitive):
    return merge(base(infinitive), u'겠다')

@conjugation
def declarative_future_conditional_formal_high(infinitive):
    return merge(base(infinitive), u'겠습니다')

@conjugation
def inquisitive_present_informal_low(infinitive):
    return merge(declarative_present_informal_low(infinitive), u'?')

@conjugation
def inquisitive_present_informal_high(infinitive):
    return merge(declarative_present_informal_high(infinitive), u'?')

@conjugation
def inquisitive_present_formal_low(infinitive):
    return merge(base(infinitive), u'니?')

@conjugation
def inquisitive_present_formal_high(infinitive):
    return merge(base(infinitive), u'습니까?')

@conjugation
def inquisitive_past_informal_low(infinitive):
    return declarative_past_informal_low(infinitive) + u'?'

@conjugation
def inquisitive_past_informal_high(infinitive):
    return merge(declarative_past_informal_high(infinitive), u'?')

@conjugation
def inquisitive_past_formal_low(infinitive):
    return merge(past_base(infinitive), u'니?')

@conjugation
def inquisitive_past_formal_high(infinitive):
    return merge(past_base(infinitive), u'습니까?')

@conjugation
def imperative_present_informal_low(infinitive):
    return declarative_present_informal_low(infinitive)

@conjugation
def imperative_present_informal_high(infinitive):
    return merge(base3(infinitive), u'세요')

@conjugation
def imperative_present_formal_low(infinitive):
    return merge(imperative_present_informal_low(infinitive), u'라')

@conjugation
def imperative_present_formal_high(infinitive):
    return merge(base3(infinitive), u'십시오')

@conjugation
def propositive_present_informal_low(infinitive):
    return declarative_present_informal_low(infinitive)

@conjugation
def propositive_present_informal_high(infinitive):
    return declarative_present_informal_high(infinitive)

@conjugation
def propositive_present_formal_low(infinitive):
    return merge(base(infinitive), u'자')

@conjugation
def propositive_present_formal_high(infinitive):
    return merge(base3(infinitive), u'읍시다')

@conjugation
def connective_if(infinitive):
    return merge(base2(infinitive), u'면')

@conjugation
def connective_and(infinitive):
    return merge(base(infinitive), u'고')

@conjugation
def nominal_ing(infinitive):
    return merge(base2(infinitive), u'음')

#for x, y in conjugation.perform(u'놓다'):
#    print x, y
#print(pformat(list(conjugation.tenses.keys())))

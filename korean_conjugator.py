# -*- coding: utf-8 -*-

from hangeul_utils import *
from pprint import pformat

def no_padchim_rule(character):
    u'''no_padchim_rule is a helper function for defining merges where a character will take the padchim of a merged
       character if the first character doesn't already have a padchim, .e.g. 습 -> 가 + 습니다 -> 갑니다.'''
    def rule(x, y):
        if not padchim(x[-1]) and y[0] == character:
            return x[:-1] + join(lead(x[-1]), vowel(x[-1]), padchim(character)) + y[1:]
    return rule

def vowel_contraction(vowel1, vowel2, new_vowel):
    u'''vowel contraction is a helper function for defining common contractions between a character without a padchim
       and a character that starts with u'ᄋ', e.g. ㅐ + ㅕ -> ㅐ when applied to 해 + 였 yields 했.'''
    def rule(x, y):
        return match(x[-1], u'*', vowel1, None) and match(y[0], u'ᄋ', vowel2) and x[:-1] + join(lead(x[-1]), new_vowel, padchim(y[0])) + y[1:]
    return rule

# merge rules is a list of rules that are applied in order when merging a verb stem with a tense ending
merge_rules = []

# no padchim + 을
merge_rules.append(no_padchim_rule(u'을'))

# no padchim + 습, 읍
merge_rules.append(no_padchim_rule(u'습'))

# no padchim + 는
merge_rules.append(no_padchim_rule(u'는')) 

# ㄹ irregular
# a true ㄹ pachim (not one that was converted from ㄷ -> ㄹ) is dropped in many merges 
merge_rules.append(lambda x, y: padchim(x[-1]) == u'ᆯ' and y[0] == u'는' and x[:-1] + join(lead(x[-1]), vowel(x[-1]), u'ᆫ') + y[1:])
merge_rules.append(lambda x, y: padchim(x[-1]) == u'ᆯ' and y[0] == u'습' and x[:-1] + join(lead(x[-1]), vowel(x[-1]), u'ᆸ') + y[1:])
merge_rules.append(lambda x, y: padchim(x[-1]) == u'ᆯ' and y[0] == u'니' and x[:-1] + join(lead(x[-1]), vowel(x[-1])) + y)
merge_rules.append(lambda x, y: padchim(x[-1]) == u'ᆯ' and y[0] == u'세' and x[:-1] + join(lead(x[-1]), vowel(x[-1])) + y)
merge_rules.append(lambda x, y: padchim(x[-1]) == u'ᆯ' and y[0] == u'십' and x[:-1] + join(lead(x[-1]), vowel(x[-1])) + y)
merge_rules.append(lambda x, y: padchim(x[-1]) == u'ᆯ' and y[0] == u'을' and x + y[1:])
merge_rules.append(lambda x, y: padchim(x[-1]) == u'ᆯ' and y[0] == u'면' and x + y)

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
merge_rules.append(lambda x, y: padchim(x[-1]) and y[0] == u'면' and x + u'으면' + y[1:])

# 세 command
merge_rules.append(lambda x, y: padchim(x[-1]) and y[0] == u'세' and x + u'으' + y)

# default rule - just append the contents
merge_rules.append(lambda x, y: x + y)

def apply_rules(x, y, verbose=False, rules=[]):
    u'''apply_rules concatenates every element in a list using the rules to merge the strings'''
    for i, rule in enumerate(rules):
        output = rule(x, y)
        if output:
            if verbose:
                print("rule %03d: %s + %s => %s" % (i, pformat(x), pformat(y), pformat(output)))
            return output

merge = lambda x, y: apply_rules(x, y, rules=merge_rules, verbose=False)

class conjugation:
    u''''conjugation is a singleton decorator that simply builds a list of all the conjugation rules'''
    def __init__(self):
        self.tenses = {}
        self.tense_order = []

    def perform(self, infinitive):
        u'''perform returns the result of the application of all of the conjugation rules on one infinitive'''
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
    if match(infinitive[-1], u'*', u'*', u'ᆸ'):
        return merge(infinitive[:-1] + join(lead(infinitive[-1]), vowel(infinitive[-1])), u'우')
    # ㄷ irregular
    elif match(infinitive[-1], u'*', u'*', u'ᆮ') and infinitive not in [u'믿', u'받', u'얻', u'닫']:
        infinitive = Geulja(infinitive[:-1] + join(lead(infinitive[-1]), vowel(infinitive[-1]), u'ᆯ'))
        infinitive.original_padchim = u'ᆮ'
    elif match(infinitive[-1], u'*', u'*', u'ᆺ') and infinitive not in [u'벗', u'웃', u'씻', u'빗']:
        infinitive = Geulja(infinitive[:-1] + join(lead(infinitive[-1]), vowel(infinitive[-1])))
        infinitive.hidden_padchim = True
    return infinitive

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
    return merge(base2(infinitive), u'을')

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
    return declarative_present_informal_high(infinitive) + u'?'

@conjugation
def inquisitive_present_formal_low(infinitive):
    return merge(base(infinitive), u'니?')

@conjugation
def inquisitive_present_formal_high(infinitive):
    return merge(base(infinitive), u'습니까?')

@conjugation
def imperative_present_informal_low(infinitive):
    return declarative_present_informal_low(infinitive)

@conjugation
def imperative_present_informal_high(infinitive):
    return merge(base2(infinitive), u'세요')

@conjugation
def imperative_present_formal_low(infinitive):
    return merge(imperative_present_informal_low(infinitive), u'라')

@conjugation
def imperative_present_formal_high(infinitive):
    return merge(base2(infinitive), u'십시오')

@conjugation
def connective_if(infinitive):
    return merge(base2(infinitive), u'면')

assert merge(u'오', u'아요') == u'와요'
assert merge(u'오', u'아') == u'와'
assert merge(u'갔', u'면') == u'갔으면'
assert merge(u'일어나', u'면') == u'일어나면'
assert merge(u'맡', u'세요') == u'맡으세요'

assert declarative_present_informal_low(u'하') == u'해'
assert declarative_present_informal_low(u'가') == u'가'
assert declarative_present_informal_low(u'오') == u'와'
assert declarative_present_informal_low(u'피우') == u'피워'
assert declarative_present_informal_low(u'듣') == u'들어'
assert declarative_present_informal_low(u'춥') == u'추워'
assert declarative_present_informal_low(u'낫') == u'나아'
assert declarative_present_informal_low(u'알') == u'알아'
assert declarative_present_informal_low(u'기다리') == u'기다려'
assert declarative_present_informal_low(u'마르') == u'말라'
assert declarative_present_informal_low(u'부르다') == u'불러'
assert declarative_present_informal_low(u'되') == u'돼'
assert declarative_present_informal_low(u'쓰') == u'써'
assert declarative_present_informal_low(u'서') == u'서'
assert declarative_present_informal_low(u'세') == u'세'
assert declarative_present_informal_low(u'기다리다') == u'기다려'
assert declarative_present_informal_low(u'굽다') == u'구워'
assert declarative_present_informal_low(u'걷다') == u'걸어'
assert declarative_present_informal_low(u'짓다') == u'지어'
assert declarative_present_informal_low(u'웃다') == u'웃어'
assert declarative_present_informal_low(u'걸다') == u'걸어'
assert declarative_present_informal_low(u'깨닫다') == u'깨달아'
assert declarative_present_informal_low(u'남다') == u'남아'
assert declarative_present_informal_low(u'오르다') == u'올라'

assert declarative_present_informal_high(u'가다') == u'가요'

assert declarative_present_formal_low(u'가다') == u'간다'
assert declarative_present_formal_low(u'믿다') == u'믿는다'
assert declarative_present_formal_low(u'걷다') == u'걷는다'
assert declarative_present_formal_low(u'짓다') == u'짓는다'
assert declarative_present_formal_low(u'부르다') == u'부른다'
assert declarative_present_formal_low(u'살다') == u'산다'
assert declarative_present_formal_low(u'오르다') == u'오른다'

assert declarative_present_formal_high(u'가다') == u'갑니다'
assert declarative_present_formal_high(u'믿다') == u'믿습니다'
assert declarative_present_formal_high(u'걸다') == u'겁니다'
assert declarative_present_formal_high(u'깨닫다') == u'깨닫습니다'
assert declarative_present_formal_high(u'알다') == u'압니다'

assert past_base(u'하') == u'했'
assert past_base(u'가') == u'갔'
assert past_base(u'기다리') == u'기다렸'
assert past_base(u'기다리다') == u'기다렸'
assert past_base(u'마르다') == u'말랐'
assert past_base(u'드르다') == u'들렀'

assert declarative_past_informal_low(u'하') == u'했어'
assert declarative_past_informal_low(u'가') == u'갔어'
assert declarative_past_informal_low(u'먹') == u'먹었어'
assert declarative_past_informal_low(u'오') == u'왔어'

assert declarative_past_informal_high(u'하다') == u'했어요'
assert declarative_past_informal_high(u'가다') == u'갔어요'

assert declarative_past_formal_low(u'가다') == u'갔다'

assert declarative_past_formal_high(u'가다') == u'갔습니다'

assert declarative_future_informal_low(u'가다') == u'갈 거야'
assert declarative_future_informal_low(u'믿다') == u'믿을 거야'
assert declarative_future_informal_low(u'알다') == u'알 거야'

assert declarative_future_informal_high(u'가다') == u'갈 거예요'
assert declarative_future_informal_high(u'믿다') == u'믿을 거예요'
assert declarative_future_informal_high(u'걷다') == u'걸을 거예요'
assert declarative_future_informal_high(u'알다') == u'알 거예요'

assert declarative_future_formal_low(u'가다') == u'갈 거다'
assert declarative_future_formal_low(u'앉다') == u'앉을 거다'
assert declarative_future_formal_low(u'알다') == u'알 거다'

assert declarative_future_formal_high(u'가다') == u'갈 겁니다'
assert declarative_future_formal_high(u'앉다') == u'앉을 겁니다'
assert declarative_future_formal_high(u'알다') == u'알 겁니다'

assert declarative_future_conditional_informal_low(u'가다') == u'가겠어'

assert declarative_future_conditional_informal_high(u'가다') == u'가겠어요'

assert declarative_future_conditional_formal_low(u'가다') == u'가겠다'

assert declarative_future_conditional_formal_high(u'가다') == u'가겠습니다'

assert inquisitive_present_informal_low(u'가다') == u'가?'
assert inquisitive_present_informal_low(u'하다') == u'해?'

assert inquisitive_present_informal_high(u'가다') == u'가요?'

assert inquisitive_present_formal_low(u'가다') == u'가니?'
assert inquisitive_present_formal_low(u'알다') == u'아니?'

assert inquisitive_present_formal_high(u'가다') == u'갑니까?'

assert imperative_present_informal_low(u'가다') == u'가'

assert imperative_present_informal_high(u'가다') == u'가세요'
assert imperative_present_informal_high(u'돕다') == u'도우세요'
assert imperative_present_informal_high(u'걷다') == u'걸으세요'
assert imperative_present_informal_high(u'눕다') == u'누우세요'
assert imperative_present_informal_high(u'살다') == u'사세요'

assert imperative_present_formal_low(u'가다') == u'가라'
assert imperative_present_formal_low(u'굽다') == u'구워라'
assert imperative_present_formal_low(u'살다') == u'살아라'
assert imperative_present_formal_low(u'서') == u'서라'

assert imperative_present_formal_high(u'가다') == u'가십시오'
assert imperative_present_formal_high(u'돕다') == u'도우십시오'
assert imperative_present_formal_high(u'알다') == u'아십시오'

assert connective_if(u'낫') == u'나으면'
assert connective_if(u'짓') == u'지으면'
assert connective_if(u'짖') == u'짖으면'
assert connective_if(u'가') == u'가면'
assert connective_if(u'알') == u'알면'
assert connective_if(u'살') == u'살면'

#for x, y in conjugation.perform(u'놓다'):
#    print x, y
#print(pformat(list(conjugation.tenses.keys())))

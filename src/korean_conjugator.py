# -*- coding: utf-8 -*-

# (C) 2009 Dan Bravender

from hangeul_utils import join, lead, vowel, padchim, find_vowel_to_append, match, Geulja

def no_padchim_rule(characters):
    u'''no_padchim_rule is a helper function for defining merges where a 
        character will take the padchim of a merged character if the first 
        character doesn't already have a padchim, .e.g. 습 -> 가 + 습니다 -> 갑니다.
     '''
    def rule(x, y):
        if not padchim(x[-1]) and y[0] in characters:
            return (u'borrow padchim', x[:-1] + join(lead(x[-1]), 
                                                    vowel(x[-1]), 
                                                    padchim(y[0])) +
                                       y[1:])
    return rule

def vowel_contraction(vowel1, vowel2, new_vowel):
    u'''vowel contraction is a helper function for defining common contractions 
        between a character without a padchim and a character that starts with 
        u'ᄋ', e.g. ㅐ + ㅕ -> ㅐ when applied to 해 + 였 yields 했.
     '''
    def rule(x, y):
        if match(x[-1], u'*', vowel1, None) and \
           match(y[0], u'ᄋ', vowel2):
            return (u'vowel contraction [%s + %s -> %s]' % 
                               (vowel1, vowel2, new_vowel),
                    x[:-1] + 
                    join(lead(x[-1]), 
                         new_vowel, 
                         padchim(y[0])) + 
                    y[1:])
    return rule

def drop_l(characters):
    def rule(x, y):
        if padchim(x[-1]) in [u'ᆯ'] and \
           y[0] in characters:
            return (u'drop %s' % padchim(x[-1]),
                                x[:-1] + 
                                join(lead(x[-1]), vowel(x[-1])) + 
                                y)
    return rule

def drop_l_and_borrow_padchim(characters):
    def rule(x, y):
        if padchim(x[-1]) in [u'ᆯ'] and \
           y[0] in characters:
            return (u'drop %s borrow padchim' % padchim(x[-1]),
                                              x[:-1] + 
                                              join(lead(x[-1]), 
                                                   vowel(x[-1]), 
                                                   padchim(y[0])) + 
                                              y[1:])
    return rule

def insert_eh(characters):
    def rule(x, y):
        if padchim(x[-1]) and y[0] in characters:
            return (u'padchim + consonant -> insert 으', x + u'으' + y)
    return rule

# merge rules is a list of rules that are applied in order when merging a verb 
#             stem with a tense ending
merge_rules = []

merge_rules.append(no_padchim_rule([u'을', u'습', u'읍', u'는', u'음']))

# ㄹ irregular
merge_rules.append(drop_l_and_borrow_padchim([u'는', u'습', u'읍', u'을']))
merge_rules.append(drop_l([u'니', u'세', u'십']))

merge_rules.append(lambda x, y: padchim(x[-1]) == u'ᆯ' and y[0] == u'면' and \
                   ('join', x + y))
merge_rules.append(lambda x, y: padchim(x[-1]) == u'ᆯ' and y[0] == u'음' and \
                   [u'ㄹ + ㅁ -> ᆱ', x[:-1] + join(lead(x[-1]), vowel(x[-1]), u'ᆱ')])


# vowel contractions
merge_rules.append(vowel_contraction(u'ㅐ', u'ㅓ', u'ㅐ'))
merge_rules.append(vowel_contraction(u'ㅡ', u'ㅓ', u'ㅓ'))
merge_rules.append(vowel_contraction(u'ㅜ', u'ㅓ', u'ㅝ'))
merge_rules.append(vowel_contraction(u'ㅗ', u'ㅏ', u'ㅘ'))
merge_rules.append(vowel_contraction(u'ㅚ', u'ㅓ', u'ㅙ'))
merge_rules.append(vowel_contraction(u'ㅙ', u'ㅓ', u'ㅙ'))
merge_rules.append(vowel_contraction(u'ㅘ', u'ㅓ', u'ㅘ'))
merge_rules.append(vowel_contraction(u'ㅝ', u'ㅓ', u'ㅝ'))
merge_rules.append(vowel_contraction(u'ㅏ', u'ㅏ', u'ㅏ'))
merge_rules.append(vowel_contraction(u'ㅡ', u'ㅏ', u'ㅏ'))
merge_rules.append(vowel_contraction(u'ㅣ', u'ㅓ', u'ㅕ'))
merge_rules.append(vowel_contraction(u'ㅓ', u'ㅓ', u'ㅓ'))
merge_rules.append(vowel_contraction(u'ㅓ', u'ㅣ', u'ㅐ'))
merge_rules.append(vowel_contraction(u'ㅏ', u'ㅣ', u'ㅐ'))
merge_rules.append(vowel_contraction(u'ㅑ', u'ㅣ', u'ㅒ'))
merge_rules.append(vowel_contraction(u'ㅒ', u'ㅓ', u'ㅒ'))
merge_rules.append(vowel_contraction(u'ㅔ', u'ㅓ', u'ㅔ'))
merge_rules.append(vowel_contraction(u'ㅕ', u'ㅓ', u'ㅕ'))
merge_rules.append(vowel_contraction(u'ㅏ', u'ㅕ', u'ㅐ'))
merge_rules.append(vowel_contraction(u'ㅖ', u'ㅓ', u'ㅖ'))
merge_rules.append(vowel_contraction(u'ㅞ', u'ㅓ', u'ㅞ'))

# 으 insertion
merge_rules.append(insert_eh([u'면', u'세', u'십']))

# default rule - just append the contents
merge_rules.append(lambda x, y: ('join', x + y))

def apply_rules(x, y, verbose=False, rules=[]):
    u'''apply_rules concatenates every element in a list using the rules to 
        merge the strings
     '''
    for i, rule in enumerate(rules):
        output = rule(x, y)
        if output:
            conjugation.reasons.append(u'%s (%s + %s -> %s)' % 
                                       (output[0] and output[0] or '', 
                                        x, 
                                        y, 
                                        output[1]))
            return output[1]

merge = lambda x, y: apply_rules(x, y, rules=merge_rules, verbose=False)

class conjugation:
    u'''conjugation is a singleton decorator that simply builds a list of 
        all the conjugation rules
     '''
    def __init__(self):
        self.tenses = {}
        self.tense_order = []
        self.reasons = []

    def perform(self, infinitive, regular=False):
        u'''perform returns the result of the application of all of the
            conjugation rules on one infinitive
         '''
        results = []
        for tense in self.tense_order:
            self.reasons = []
            c = self.tenses[tense](infinitive, regular)
            results.append((tense, c, self.reasons))
        return results
    
    def __call__(self, f):
        self.tense_order.append(f.__name__)
        self.tenses.update({f.__name__: f})
        return f

conjugation = conjugation()

def is_s_irregular(infinitive, regular=False):
    return match(infinitive[-1], u'*', u'*', u'ᆺ') and \
         infinitive[-1] not in [u'벗', u'웃', u'씻', u'빗', 
                                u'앗', u'뺏', u'솟', u'밧',
                                u'긋', u'깃', u'엇']

def is_l_irregular(infinitive, regular=False):
    if regular or infinitive in [u'따르']:
        return False
    return match(infinitive[-1], u'ᄅ', u'ㅡ', None)

def is_h_irregular(infinitive, regular=False):
    if regular:
        return False
    return (padchim(infinitive[-1]) == u'ᇂ' or infinitive[-1] == u'러') and \
           infinitive[-1] not in [u'낳', u'넣', u'좋', u'찧', u'놓', u'쌓', u'닿']

def is_p_irregular(infinitive, regular=False):
    if regular or infinitive in [u'에굽', u'예굽']:
        return False
    if infinitive in [u'바잡', u'빛접', u'숫접', u'흉업']:
        return True
    return match(infinitive[-1], u'*', u'*', u'ᆸ') and \
           infinitive[-1] not in [u'잡', u'입', u'씹', u'줍', u'접',
                                  u'좁', u'집', u'뽑', u'업']

def is_d_irregular(infinitive, regular=False):
    if regular or infinitive in [u'욱걷', u'치걷', u'덧묻', u'줄밑걷', 
                                 u'활걷', u'겉묻', u'그러묻', u'껴묻',
                                 u'뒤묻', u'부르돋', u'북돋', u'부르걷']:
        return False
    elif infinitive in [u'깨닫', u'파묻']:
        return True
    return match(infinitive[-1], u'*', u'*', u'ᆮ') and \
           infinitive[-1] not in [u'굳', u'믿', u'받', u'얻', u'벋', 
                                  u'닫', u'뜯', u'딛', u'뻗']

@conjugation
def base(infinitive, regular=False):
    if infinitive[-1] == u'다':
        return infinitive[:-1]
    else:
        return infinitive

@conjugation
def base2(infinitive, regular=False):
    infinitive = base(infinitive, regular)
    
    if infinitive == u'뵙':
        return u'뵈'
    
    if infinitive == u'푸':
        return u'퍼'
    
    new_infinitive = infinitive
    if is_h_irregular(infinitive, regular):
        new_infinitive = merge(infinitive[:-1] + 
                               join(lead(infinitive[-1]),
                                    vowel(infinitive[-1])),
                               u'이')
        conjugation.reasons.append(u'ㅎ irregular (%s -> %s)' % (infinitive,
                                                                new_infinitive))
    # ㅂ irregular
    elif is_p_irregular(infinitive, regular):
        if infinitive[-1] in [u'돕', u'곱']:
            new_vowel = u'ㅗ'
        else:
            new_vowel = u'ㅜ'
        new_infinitive = merge(infinitive[:-1] + 
                               join(lead(infinitive[-1]), 
                                    vowel(infinitive[-1])),
                               join(u'ᄋ', new_vowel))
        conjugation.reasons.append(u'ㅂ irregular (%s -> %s)' % (infinitive, 
                                                                new_infinitive))
    # ㄷ irregular
    elif is_d_irregular(infinitive, regular):
        new_infinitive = Geulja(infinitive[:-1] + join(lead(infinitive[-1]), 
                                                       vowel(infinitive[-1]), 
                                                       u'ᆯ'))
        new_infinitive.original_padchim = u'ᆮ'
        conjugation.reasons.append(u'ㄷ irregular (%s -> %s)' % (infinitive,
                                                                new_infinitive))
    elif is_s_irregular(infinitive, regular):
        new_infinitive = Geulja(infinitive[:-1] + join(lead(infinitive[-1]), 
                                                       vowel(infinitive[-1])))
        new_infinitive.hidden_padchim = True
        conjugation.reasons.append(u'ㅅ irregular (%s -> %s [hidden padchim])' % 
                                   (infinitive, new_infinitive))
    return new_infinitive

@conjugation
def base3(infinitive, regular=False):
    infinitive = base(infinitive, regular)
    if infinitive == u'뵙':
        return u'뵈'
    if is_h_irregular(infinitive, regular):
        return infinitive[:-1] + join(lead(infinitive[-1]), vowel(infinitive[-1]))
    elif is_p_irregular(infinitive, regular):
        return infinitive[:-1] + join(lead(infinitive[-1]), vowel(infinitive[-1])) + u'우'
    else:
        return base2(infinitive, regular)

@conjugation
def base4(infinitive, regular=False):
    infinitive = base(infinitive, regular)
    if is_h_irregular(infinitive, regular):
        return infinitive[:-1] + join(lead(infinitive[-1]), vowel(infinitive[-1]))
    else:
        return base2(infinitive, regular)

@conjugation
def declarative_present_informal_low(infinitive, regular=False):
    infinitive = base2(infinitive, regular)
    # 르 irregular
    if is_l_irregular(infinitive, regular):
        new_base = infinitive[:-2] + join(lead(infinitive[-2]), 
                                          vowel(infinitive[-2]), u'ᆯ')
        if infinitive[-2:] in [u'푸르', u'이르']:
            new_base = new_base + join(u'ᄅ', 
                                       vowel(find_vowel_to_append(new_base)))
            conjugation.reasons.append(u'irregular stem + %s -> %s' % 
                                       (infinitive, new_base))
            return infinitive + u'러'
        elif find_vowel_to_append(infinitive[:-1]) == u'아':
            new_base += u'라'
            conjugation.reasons.append(u'르 irregular stem change [%s -> %s]' %
                                       (infinitive, new_base))
            return new_base
        else:
            new_base += u'러'
            conjugation.reasons.append(u'르 irregular stem change [%s -> %s]' %
                                       (infinitive, new_base))
            return new_base
    elif infinitive[-1] == u'하':
        return merge(infinitive, u'여')
    elif is_h_irregular(infinitive, regular):
        return merge(infinitive, u'이')
    return merge(infinitive, find_vowel_to_append(infinitive))

@conjugation
def declarative_present_informal_high(infinitive, regular=False):
    return merge(declarative_present_informal_low(infinitive, regular), u'요')

@conjugation
def declarative_present_formal_low(infinitive, regular=False):
    return merge(base(infinitive, regular), u'는다')

@conjugation
def declarative_present_formal_high(infinitive, regular=False):
    return merge(base(infinitive, regular), u'습니다')

@conjugation
def past_base(infinitive, regular=False):
    ps = declarative_present_informal_low(infinitive, regular)
    if find_vowel_to_append(ps) == u'아':
        return merge(ps, u'았')
    else:
        return merge(ps, u'었')

@conjugation
def declarative_past_informal_low(infinitive, regular=False):
    return merge(past_base(infinitive, regular), u'어')

@conjugation
def declarative_past_informal_high(infinitive, regular=False):
    return merge(declarative_past_informal_low(infinitive, regular), u'요')

@conjugation
def declarative_past_formal_low(infinitive, regular=False):
    return merge(past_base(infinitive, regular), u'다')

@conjugation
def declarative_past_formal_high(infinitive, regular=False):
    return merge(past_base(infinitive, regular), u'습니다')

@conjugation
def future_base(infinitive, regular=False):
    return merge(base3(infinitive, regular), u'을')

@conjugation
def declarative_future_informal_low(infinitive, regular=False):
    return merge(future_base(infinitive, regular), u' 거야')

@conjugation
def declarative_future_informal_high(infinitive, regular=False):
    return merge(future_base(infinitive, regular), u' 거예요')

@conjugation
def declarative_future_formal_low(infinitive, regular=False):
    return merge(future_base(infinitive, regular), u' 거다')

@conjugation
def declarative_future_formal_high(infinitive, regular=False):
    return merge(future_base(infinitive, regular), u' 겁니다')

@conjugation
def declarative_future_conditional_informal_low(infinitive, regular=False):
    return merge(base(infinitive, regular), u'겠어')

@conjugation
def declarative_future_conditional_informal_high(infinitive, regular=False):
    return merge(base(infinitive, regular), u'겠어요')

@conjugation
def declarative_future_conditional_formal_low(infinitive, regular=False):
    return merge(base(infinitive, regular), u'겠다')

@conjugation
def declarative_future_conditional_formal_high(infinitive, regular=False):
    return merge(base(infinitive, regular), u'겠습니다')

@conjugation
def inquisitive_present_informal_low(infinitive, regular=False):
    return merge(declarative_present_informal_low(infinitive, regular), u'?')

@conjugation
def inquisitive_present_informal_high(infinitive, regular=False):
    return merge(declarative_present_informal_high(infinitive, regular), u'?')

@conjugation
def inquisitive_present_formal_low(infinitive, regular=False):
    return merge(base(infinitive, regular), u'니?')

@conjugation
def inquisitive_present_formal_high(infinitive, regular=False):
    return merge(base(infinitive, regular), u'습니까?')

@conjugation
def inquisitive_past_informal_low(infinitive, regular=False):
    return declarative_past_informal_low(infinitive, regular) + u'?'

@conjugation
def inquisitive_past_informal_high(infinitive, regular=False):
    return merge(declarative_past_informal_high(infinitive, regular), u'?')

@conjugation
def inquisitive_past_formal_low(infinitive, regular=False):
    return merge(past_base(infinitive, regular), u'니?')

@conjugation
def inquisitive_past_formal_high(infinitive, regular=False):
    return merge(past_base(infinitive, regular), u'습니까?')

@conjugation
def imperative_present_informal_low(infinitive, regular=False):
    return declarative_present_informal_low(infinitive, regular)

@conjugation
def imperative_present_informal_high(infinitive, regular=False):
    return merge(base3(infinitive, regular), u'세요')

@conjugation
def imperative_present_formal_low(infinitive, regular=False):
    return merge(imperative_present_informal_low(infinitive, regular), u'라')

@conjugation
def imperative_present_formal_high(infinitive, regular=False):
    return merge(base3(infinitive, regular), u'십시오')

@conjugation
def propositive_present_informal_low(infinitive, regular=False):
    return declarative_present_informal_low(infinitive, regular)

@conjugation
def propositive_present_informal_high(infinitive, regular=False):
    return declarative_present_informal_high(infinitive, regular)

@conjugation
def propositive_present_formal_low(infinitive, regular=False):
    return merge(base(infinitive, regular), u'자')

@conjugation
def propositive_present_formal_high(infinitive, regular=False):
    return merge(base3(infinitive, regular), u'읍시다')

@conjugation
def connective_if(infinitive, regular=False):
    return merge(base4(infinitive, regular), u'면')

@conjugation
def connective_and(infinitive, regular=False):
    infinitive = base(infinitive, regular)
    return merge(base(infinitive, regular), u'고')

@conjugation
def nominal_ing(infinitive, regular=False):
    infinitive = base(infinitive, regular)
    return merge(base3(infinitive, regular), u'음')

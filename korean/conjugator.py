# -*- coding: utf-8 -*-

# (C) 2009 Dan Bravender

from hangeul import join, lead, vowel, padchim, find_vowel_to_append, match, Geulja
from pronunciation import pronunciation

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
            p = pronunciation(c)
            tense = tense.replace('_', ' ')
            results.append((tense, c, p, self.reasons))
        return results
    
    def __call__(self, f):
        self.tense_order.append(f.__name__)
        self.tenses.update({f.__name__: f})
        return f

conjugation = conjugation()

both_regular_and_irregular = [
    u'일', u'곱', u'파묻', u'누르', u'묻', u'이르',
    u'되묻', u'썰', u'붓', u'들까불', u'굽', u'걷',
    u'뒤까불', u'까불'
]

not_p_irregular = dict([(u'털썩이잡', True), (u'넘겨잡', True), (u'우접', True), (u'입', True), (u'맞접', True), (u'문잡', True), (u'다잡', True), (u'까뒤집', True), (u'배좁', True), (u'목잡', True), (u'끄집', True), (u'잡', True), (u'옴켜잡', True), (u'검잡', True), (u'되순라잡', True), (u'내씹', True), (u'모집', True), (u'따잡', True), (u'엇잡', True), (u'까집', True), (u'겹집', True), (u'줄통뽑', True), (u'버르집', True), (u'지르잡', True), (u'추켜잡', True), (u'업', True), (u'되술래잡', True), (u'되접', True), (u'좁디좁', True), (u'더위잡', True), (u'말씹', True), (u'내뽑', True), (u'집', True), (u'걸머잡', True), (u'휘어잡', True), (u'꿰입', True), (u'황잡', True), (u'에굽', True), (u'내굽', True), (u'따라잡', True), (u'맞뒤집', True), (u'둘러업', True), (u'늘잡', True), (u'끄잡', True), (u'우그려잡', True), (u'어줍', True), (u'언걸입', True), (u'들이곱', True), (u'껴잡', True), (u'곱 접', True), (u'훔켜잡', True), (u'늦추잡', True), (u'갈아입', True), (u'친좁', True), (u'희짜뽑', True), (u'마음잡', True), (u'개미잡', True), (u'옴씹', True), (u'치잡', True), (u'그러잡', True), (u' 움켜잡', True), (u'씹', True), (u'비집', True), (u'꼽', True), (u'살잡', True), (u'죄입', True), (u'졸잡', True), (u'가려잡', True), (u'뽑', True), (u'걷어잡', True), (u'헐잡', True), (u'돌라입', True), (u'덧잡', True), (u'얕잡', True), (u'낫잡', True), (u'부여잡', True), (u'맞붙잡', True), (u'걸입', True), (u'주름잡', True), (u'걷어입', True), (u'빌미잡', True), (u'개잡', True), (u'겉잡', True), (u'안쫑잡', True), (u'좁', True), (u'힘입', True), (u'걷잡', True), (u'바르집', True), (u'감씹', True), (u'짓씹', True), (u'손잡', True), (u'포집', True), (u'붙잡', True), (u'낮잡', True), (u'책잡', True), (u'곱잡', True), (u'흉잡', True), (u'뒤집', True), (u'땡잡', True), (u'어림잡', True), (u'덧껴입', True), (u'수줍', True), (u'뒤잡', True), (u'꼬집', True), (u'예굽', True), (u'덮쳐잡', True), (u'헛잡', True), (u'되씹', True), (u'낮추잡', True), (u'날파람잡', True), (u'틀어잡', True), (u'헤집', True), (u'남의달잡', True), (u'바로잡', True), (u'흠잡', True), (u'파잡', True), (u'얼추잡', True), (u'손꼽', True), (u'접', True), (u'차려입', True), (u'골라잡', True), (u'거머잡', True), (u'후려잡', True), (u'머줍', True), (u'넉장뽑', True), (u'사로잡', True), (u'덧입', True), (u'껴입', True), (u'얼입', True), (u'우집', True), (u'설잡', True), (u'늦잡', True), (u'비좁', True), (u'고르잡', True), (u'때려잡', True), (u'떼집', True), (u'되잡', True), (u'홈켜잡', True), (u'내곱', True), (u'곱씹', True), (u'빼입', True), (u'들이굽', True), (u'새잡', True), (u'이르집', True), (u'떨쳐입', True)])
not_s_irregular = dict([(u'내솟', True), (u'빗', True), (u'드솟', True), (u'비웃', True), (u'뺏', True), (u'샘솟', True), (u'벗', True), (u'들이웃', True), (u'솟', True), (u'되뺏', True), (u'빼앗', True), (u'밧', True), (u'애긋', True), (u'짜드라웃', True), (u'어그솟', True), (u'들솟', True), (u'씻', True), (u'빨가벗', True), (u'깃', True), (u'벌거벗', True), (u'엇', True), (u'되빼앗', True), (u'웃', True), (u'앗', True), (u'헐벗', True), (u'용솟', True), (u'덧솟', True), (u'발가벗', True), (u'뻘거벗', True), (u'날솟', True), (u'치솟', True)])

not_d_irregular = dict([(u'맞받', True), (u'내딛', True), (u'내리받', True), (u'벋', True), (u'뒤닫', True), (u'주고받', True), (u'공얻', True), (u'무뜯', True), (u'물어뜯', True), (u'여닫', True), (u'그러묻', True), (u'잇닫', True), (u'덧묻', True), (u'되받', True), (u'뻗', True), (u'올리닫', True), (u'헐뜯', True), (u'들이닫', True), (u'활걷', True), (u'겉묻', True), (u'닫', True), (u'창받', True), (u'건네받', True), (u'물손받', True), (u'들이받', True), (u'강요받', True), (u'내리벋', True), (u' 받', True), (u'이어받', True), (u'부르걷', True), (u'응받', True), (u'검뜯', True), (u'인정받', True), (u'내려딛', True), (u'내쏟', True), (u'내리뻗', True), (u'너름받', True), (u'세받', True), (u'내 돋', True), (u'돌려받', True), (u'쥐어뜯', True), (u'껴묻', True), (u'본받', True), (u'뒤받', True), (u'강종받', True), (u'내리닫', True), (u'떠받', True), (u'테받', True), (u'내받', True), (u'흠뜯', True), (u'두남받', True), (u'치받', True), (u'부르돋', True), (u'대받', True), (u'설굳', True), (u' 처닫', True), (u'얻', True), (u'들이돋', True), (u'돋', True), (u'죄받', True), (u'쏟', True), (u'씨받', True), (u'딱장받', True), (u'치걷', True), (u'믿', True), (u'치벋', True), (u'버림받', True), (u'북돋', True), (u'딛', True), (u'치고받', True), (u'욱걷', True), (u'물려받', True), (u'뜯', True), (u'줴뜯', True), (u'넘겨받', True), (u'안받', True), (u'내뻗', True), (u'내리쏟', True), (u'벋딛', True), (u'뒤묻', True), (u'뻗딛', True), (u'치뻗', True), (u'치닫', True), (u'줄밑걷', True), (u'굳', True), (u'내닫', True), (u'내림받', True)])

not_h_irregular = dict([(u'들이좋', True), (u'터놓', True), (u'접어놓', True), (u'좋', True), (u'풀어놓', True), (u'내쌓', True), (u'꼴좋', True), (u'치쌓', True), (u'물어넣', True), (u'잇닿', True), (u'끝닿', True), (u'그러넣', True), (u'뽕놓', True), (u'낳', True), (u'내리찧', True), (u'힘닿', True), (u'내려놓', True), (u'세놓', True), (u'둘러놓', True), (u'들놓', True), (u'맞찧', True), (u'잡아넣', True), (u'돌라쌓', True), (u'덧쌓', True), (u'갈라땋', True), (u'주놓', True), (u'갈라놓', True), (u'들이닿', True), (u'집어넣', True), (u'닿', True), (u'의좋', True), (u'막놓', True), (u'내놓', True), (u'들여놓', True), (u'사놓', True), (u'썰레놓', True), (u'짓찧', True), (u'벋놓', True), (u'찧', True), (u'침놓', True), (u'들이찧', True), (u'둘러쌓', True), (u'털어놓', True), (u'담쌓', True), (u'돌라놓', True), (u'되잡아넣', True), (u'끌어넣', True), (u'덧놓', True), (u'맞닿', True), (u'처넣', True), (u'빻', True), (u'뻥놓', True), (u'내리쌓', True), (u'곱놓', True), (u'설레발놓', True), (u'우겨넣', True), (u'놓', True), (u'수놓', True), (u'써넣', True), (u'널어놓', True), (u'덮쌓', True), (u'연닿', True), (u'헛놓', True), (u'돌려놓', True), (u'되쌓', True), (u'욱여넣', True), (u'앗아넣', True), (u'올려놓', True), (u'헛방놓', True), (u'날아놓', True), (u'뒤놓', True), (u'업수놓', True), (u'가로놓', True), (u'맞놓', True), (u'펴놓', True), (u'내켜놓', True), (u'쌓', True), (u'끙짜놓', True), (u'들이쌓', True), (u'겹쌓', True), (u'기추놓', True), (u'넣', True), (u'불어넣', True), (u'늘어놓', True), (u'긁어놓', True), (u'어긋놓', True), (u'앞넣', True), (u'눌러놓', True), (u'땋', True), (u'들여쌓', True), (u'빗놓', True), (u'사이좋', True), (u'되놓', True), (u'헛불놓', True), (u'몰아넣', True), (u'먹놓', True), (u'밀쳐놓', True), (u'살닿', True), (u'피새놓', True), (u'빼놓', True), (u'하차놓', True), (u'틀어넣', True)])

not_l_irregular = dict([(u'우러르', True), (u'따르', True), (u'붙따르', True), (u'늦치르', True), (u'다다르', True), (u'잇따르', True), (u'치르', True)])

def is_s_irregular(infinitive, regular=False):
    if regular: 
        return False
    return match(infinitive[-1], u'*', u'*', u'ᆺ') and \
           not not_s_irregular.get(infinitive, False)

def is_l_irregular(infinitive, regular=False):
    if regular:
        return False
    return match(infinitive[-1], u'ᄅ', u'ㅡ', None) and \
           not not_l_irregular.get(infinitive, False)

def is_h_irregular(infinitive, regular=False):
    if regular:
        return False
    return (padchim(infinitive[-1]) == u'ᇂ' or infinitive[-1] == u'러') and \
           not not_h_irregular.get(infinitive, False)

def is_p_irregular(infinitive, regular=False):
    if regular:
        return False
    return match(infinitive[-1], u'*', u'*', u'ᆸ') and \
           not not_p_irregular.get(infinitive, False)

def is_d_irregular(infinitive, regular=False):
    if regular:
        return False
    return match(infinitive[-1], u'*', u'*', u'ᆮ') and \
           not not_d_irregular.get(infinitive, False)

@conjugation
def base(infinitive, regular=False):
    if infinitive[-1] == u'다':
        return infinitive[:-1]
    else:
        return infinitive

@conjugation
def base2(infinitive, regular=False):
    infinitive = base(infinitive, regular)
    
    if infinitive == u'아니':
        infinitive = Geulja(u'아니')
        infinitive.hidden_padchim = True
        return infinitive
    
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
        # only some verbs get ㅗ (highly irregular)
        if infinitive in [u'묻잡'] or infinitive[-1] in [u'돕', u'곱']:
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
    if infinitive == u'아니':
        return u'아니'
    if infinitive == u'푸':
        return u'푸'
    if infinitive == u'뵙':
        return u'뵈'
    if is_h_irregular(infinitive, regular):
        return infinitive[:-1] + join(lead(infinitive[-1]), vowel(infinitive[-1]))
    elif is_p_irregular(infinitive, regular):
        return infinitive[:-1] + join(lead(infinitive[-1]), vowel(infinitive[-1])) + u'우'
    else:
        return base2(infinitive, regular)

@conjugation
def declarative_present_informal_low(infinitive, regular=False, further_use=False):
    infinitive = base2(infinitive, regular)
    if not further_use and ((infinitive == u'이' and not getattr(infinitive, 'hidden_padchim', False)) or \
                            infinitive == u'아니'):
        conjugation.reasons.append(u'야 irregular')
        return infinitive + u'야'
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
    infinitive = base2(infinitive, regular)
    if (infinitive == u'이' and not getattr(infinitive, 'hidden_padchim', False)) or \
       infinitive == u'아니':
        conjugation.reasons.append(u'에요 irregular')
        return infinitive + u'에요'
    return merge(declarative_present_informal_low(infinitive, regular, further_use=True), u'요')

@conjugation
def declarative_present_formal_low(infinitive, regular=False):
    return merge(base(infinitive, regular), u'는다')

@conjugation
def declarative_present_formal_high(infinitive, regular=False):
    return merge(base(infinitive, regular), u'습니다')

@conjugation
def past_base(infinitive, regular=False):
    ps = declarative_present_informal_low(infinitive, regular, further_use=True)
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
    return merge(base3(infinitive, regular), u'면')

@conjugation
def connective_and(infinitive, regular=False):
    infinitive = base(infinitive, regular)
    return merge(base(infinitive, regular), u'고')

@conjugation
def nominal_ing(infinitive, regular=False):
    infinitive = base(infinitive, regular)
    return merge(base3(infinitive, regular), u'음')

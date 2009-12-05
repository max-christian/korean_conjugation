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

not_p_irregular = [
    u'털썩이잡', u'넘겨잡', u'우접', u'입', u'맞접', u'문잡', u'다잡', u'까뒤집',
    u'배좁', u'목잡', u'끄집', u'잡', u'옴켜잡', u'검잡', u'되순라잡', u'내씹',
    u'모집', u'따잡', u'엇잡', u'까집', u'겹집', u'줄통뽑', u'버르집', u'지르잡',
    u'추켜잡', u'업', u'되술래잡', u'되접', u'좁디좁', u'더위잡', u'말씹',
    u'내뽑', u'집', u'걸머잡', u'휘어잡', u'꿰입', u'황잡', u'에굽', u'내굽',
    u'따라잡', u'맞뒤집', u'둘러업', u'늘잡', u'끄잡', u'우그려잡', u'어줍',
    u'언걸입', u'들이곱', u'껴잡', u'곱접', u'훔켜잡', u'늦추잡', u'갈아입',
    u'친좁', u'희짜뽑', u'마음잡', u'개미잡', u'옴씹', u'치잡', u'그러잡',
    u'움켜잡', u'씹', u'비집', u'꼽', u'살잡', u'죄입', u'졸잡', u'가려잡',
    u'뽑', u'걷 어잡', u'헐잡', u'돌라입', u'덧잡', u'얕잡', u'낫잡', u'부여잡',
    u'맞붙잡', u'걸입', u'주름잡', u'걷어입', u'빌미잡', u'개잡', u'겉잡',
    u'안쫑잡', u'좁', u'힘입', u'걷잡', u'바르집', u'감씹', u'짓씹', u'손잡',
    u'포집', u'붙잡', u'낮잡', u'책잡', u'곱잡', u'흉잡', u'뒤집', u'땡잡',
    u'어림잡', u'덧껴 입', u'수줍', u'뒤잡', u'꼬집', u'예굽', u'덮쳐잡',
    u'헛잡', u'되씹', u'낮추잡', u'날파람잡', u'틀어잡', u'헤집', u'남의달잡',
    u'바로잡', u'흠잡', u'파잡', u'얼추잡', u'손꼽', u'접', u'차려입', u'골라잡',
    u'거머잡', u'후려잡', u'머줍', u'넉장뽑', u'사로잡', u'덧입', u'껴입',
    u'얼입', u'우집', u'설잡', u'늦잡', u'비좁', u'고르잡', u'때려잡', u'떼집',
    u'되잡', u'홈켜잡', u'내곱', u'곱씹', u'빼입', u'들이굽', u'새잡', u'이르집',
    u'떨쳐입'
]

not_s_irregular = [
    u'내솟', u'빗', u'드솟', u'비웃', u'뺏', u'샘솟', u'벗', u'들이웃', u'솟',
    u'되뺏', u'빼앗', u'밧', u'애긋', u'짜드라웃', u'어그솟', u'들솟', u'씻',
    u'빨가벗', u'깃', u'벌거벗', u'엇', u'되빼앗', u'웃', u'앗', u'헐벗',
    u'용솟', u'덧솟', u'발가벗', u'뻘거벗', u'날솟', u'치솟'
]

not_d_irregular = [
    u'맞받', u'내딛', u'내리받', u'벋', u'뒤닫', u'주고받', u'공얻', u'무뜯',
    u'물 어뜯', u'여닫', u'그러묻', u'잇닫', u'덧묻', u'되받', u'뻗', u'올리닫',
    u'헐뜯', u'들이닫', u'활걷', u'겉묻', u'닫', u'창받', u'건네받', u'물손받',
    u'들이받', u'강요받', u'내리벋', u'받', u'이어받', u'부르걷', u'응받', u'검뜯',
    u'인정받', u'내려딛', u'내쏟', u'내리뻗', u'너름받', u'세받', u'내돋', u'돌려받',
    u'쥐어뜯', u'껴묻', u'본받', u'뒤받', u'강종받', u'내리닫', u'떠받', u'테받', u'내받',
    u'흠뜯', u'두남받', u'치받', u'부르돋', u'대받', u'설굳', u'처닫', u'얻', u'들이돋',
    u'돋', u'죄받', u'쏟', u'씨받', u'딱장받', u'치걷', u'믿', u'치벋', u'버림받', u'북돋',
    u'딛', u'치고받', u'욱걷', u'물려받', u'뜯', u'줴뜯', u'넘겨받', u'안받', u'내뻗',
    u'내리쏟', u'벋딛', u'뒤묻', u'뻗딛', u'치뻗', u'치닫', u'줄밑걷', u'굳', u'내닫',
    u'내림받'
]

not_h_irregular = [
    u'들이좋', u'터놓', u'접어놓', u'좋', u'풀어놓', u'내쌓', u'꼴좋', u'치쌓', u'물어넣',
    u'잇닿', u'끝닿', u'그러넣', u'뽕놓', u'낳', u'내리찧', u'힘닿', u'내려놓', u'세놓',
    u'둘러놓', u'들놓', u'맞찧', u'잡아넣', u'돌라쌓', u'덧쌓', u'갈라땋', u'주놓',
    u'갈라놓', u'들이닿', u'집어넣', u'닿', u'의좋', u'막놓', u'내놓', u'들여놓', u'사놓',
    u'썰레놓', u'짓찧', u'벋놓', u'찧', u'침놓', u'들이찧', u'둘러쌓', u'털어놓', u'담쌓',
    u'돌라놓', u'되잡아넣', u'끌어넣', u'덧놓', u'맞닿', u'처넣', u'빻', u'뻥놓', u'내리쌓',
    u'곱놓', u'설레발놓', u'우겨넣', u'놓', u'수놓', u'써넣', u'널어놓', u'덮쌓', u'연닿',
    u'헛놓', u'돌려놓', u'되쌓', u'욱여넣', u'앗아넣', u'올려놓', u'헛방놓', u'날아놓',
    u'뒤놓', u'업수놓', u'가로놓', u'맞놓', u'펴놓', u'내켜놓', u'쌓', u'끙짜놓', u'들이쌓',
    u'겹쌓', u'기추놓', u'넣', u'불어넣', u'늘어놓', u'긁어놓', u'어긋놓', u'앞넣', u'눌러놓',
    u'땋', u'들여쌓', u'빗놓', u'사이좋', u'되놓', u'헛불놓', u'몰아넣', u'먹놓', u'밀쳐놓',
    u'살닿', u'피새놓', u'빼놓', u'하차놓', u'틀어넣'
]

not_l_irregular = [
    u'우러르', u'따르', u'붙따르', u'늦치르', u'다다르', u'잇따르', u'치르'
]


def is_s_irregular(infinitive, regular=False):
    if regular: 
        return False
    return match(infinitive[-1], u'*', u'*', u'ᆺ') and \
         infinitive not in not_s_irregular

def is_l_irregular(infinitive, regular=False):
    if regular:
        return False
    return match(infinitive[-1], u'ᄅ', u'ㅡ', None) and \
           infinitive not in not_l_irregular

def is_h_irregular(infinitive, regular=False):
    if regular:
        return False
    return (padchim(infinitive[-1]) == u'ᇂ' or infinitive[-1] == u'러') and \
           infinitive not in not_h_irregular

def is_p_irregular(infinitive, regular=False):
    if regular:
        return False
    return match(infinitive[-1], u'*', u'*', u'ᆸ') and \
           infinitive not in not_p_irregular

def is_d_irregular(infinitive, regular=False):
    if regular:
        return False
    return match(infinitive[-1], u'*', u'*', u'ᆮ') and \
           infinitive not in not_d_irregular

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

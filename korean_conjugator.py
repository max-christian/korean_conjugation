from hangeul_utils import *
from pprint import pformat

def no_padchim_rule(character):
    def rule(x, y):
        if not padchim(x[-1]) and y[0] == character:
            return x[:-1] + join(lead(x[-1]), vowel(x[-1]), padchim(character)) + y[1:]
    return rule

def vowel_contraction(vowel1, vowel2, new_vowel):
    def rule(x, y):
        return match(x[-1], '*', vowel1, None) and match(y[0], 'ᄋ', vowel2) and x[:-1] + join(lead(x[-1]), new_vowel, padchim(y[0])) + y[1:]
    return rule

merge_rules = []

# no padchim + 을
merge_rules.append(no_padchim_rule('을'))

# no padchim + 습, 읍
merge_rules.append(no_padchim_rule('습'))
merge_rules.append(no_padchim_rule('읍'))

# no padchim + 는
merge_rules.append(no_padchim_rule('는')) 

# 면 connective
merge_rules.append(lambda x, y: padchim(x[-1]) is not None and y[0] == '면' and x + '으면' + y[1:])

# ㄹ irregular
merge_rules.append(lambda x, y: padchim(x[-1]) == 'ᆯ' and y[0] == '는' and x[:-1] + join(lead(x[-1]), vowel(x[-1]), 'ᆫ') + y[1:])
merge_rules.append(lambda x, y: padchim(x[-1]) == 'ᆯ' and y[0] == '습' and x[:-1] + join(lead(x[-1]), vowel(x[-1]), 'ᆸ') + y[1:])

# vowel contractions
merge_rules.append(vowel_contraction('ㅐ', 'ㅓ', 'ㅐ'))
merge_rules.append(vowel_contraction('ㅡ', 'ㅓ', 'ㅓ'))
merge_rules.append(vowel_contraction('ㅜ', 'ㅓ', 'ㅝ'))
merge_rules.append(vowel_contraction('ㅗ', 'ㅏ', 'ㅘ'))
merge_rules.append(vowel_contraction('ㅚ', 'ㅓ', 'ㅙ'))
merge_rules.append(vowel_contraction('ㅏ', 'ㅏ', 'ㅏ'))
merge_rules.append(vowel_contraction('ㅡ', 'ㅏ', 'ㅏ'))
merge_rules.append(vowel_contraction('ㅣ', 'ㅓ', 'ㅕ'))
merge_rules.append(vowel_contraction('ㅓ', 'ㅓ', 'ㅓ'))
merge_rules.append(vowel_contraction('ㅔ', 'ㅓ', 'ㅔ'))
merge_rules.append(vowel_contraction('ㅕ', 'ㅓ', 'ㅕ'))
merge_rules.append(vowel_contraction('ㅏ', 'ㅕ', 'ㅐ'))
merge_rules.append(lambda x, y: padchim(x[-1]) and y[0] == '세' and x + '으' + y)

# default rule - just append the contents
merge_rules.append(lambda x, y: x + y)

def apply_rules(x, y, verbose=False, rules=[]):
    '''apply_rules concatenates every element in a list using the rules to merge the strings'''
    for i, rule in enumerate(rules):
        output = rule(x, y)
        if output:
            if verbose:
                print("rule %03d: %s, %s => %s" % (i, pformat(x), pformat(y), pformat(output)))
            return output

merge = partial(apply_rules, rules=merge_rules, verbose=True)

class Conjugation:
    ''''Conjugation is a decorator that simply builds a list of all the conjugation rules'''
    def __init__(self):
        self.tenses = {}
    def __call__(self, f):
        self.tenses.update({f.__name__: f})
        return f

conjugation = Conjugation()

@conjugation
def base(infinitive):
    if infinitive[-1] == '다':
        return infinitive[:-1]
    else:
        return infinitive

@conjugation
def base2(infinitive):
    infinitive = base(infinitive)
    # ㅂ irregular
    if match(infinitive[-1], '*', '*', 'ᆸ'):
        return merge(infinitive[:-1] + join(lead(infinitive[-1]), vowel(infinitive[-1])), '우')
    # ㄷ irregular
    elif match(infinitive[-1], '*', '*', 'ᆮ') and infinitive not in ['믿', '받', '얻', '닫']:
        return infinitive[:-1] + join(lead(infinitive[-1]), vowel(infinitive[-1]), 'ᆯ')
    elif match(infinitive[-1], '*', '*', 'ᆺ') and infinitive not in ['벗', '웃', '씻', '빗']:
        infinitive = Geulja(infinitive[:-1] + join(lead(infinitive[-1]), vowel(infinitive[-1])))
        infinitive.hidden_padchim = True
    return infinitive

@conjugation
def declarative_present_informal_low(infinitive):
    infinitive = base2(infinitive)
    # ㄹ irregular
    if match(infinitive[-1], 'ᄅ', 'ㅡ'):
        new_ending = join(lead(infinitive[-2]), vowel(infinitive[-2]), 'ᆯ')
        if vowel(infinitive[-2]) in ['ㅗ', 'ㅏ']:
            return infinitive[:-2] + merge(new_ending, '라')
        else:
            return infinitive[:-2] + merge(new_ending, '러')
    elif infinitive[-1] == '하':
        return infinitive[:-1] + merge(infinitive[-1], '여')
    elif vowel(infinitive[-1]) in ['ㅗ', 'ㅏ']:
        return infinitive[:-1] + merge(infinitive[-1], '아')
    else:
        return infinitive[:-1] + merge(infinitive[-1], '어')

@conjugation
def declarative_present_informal_high(infinitive):
    return merge(declarative_present_informal_low(infinitive), '요')

@conjugation
def declarative_present_formal_low(infinitive):
    return merge(base(infinitive), '는다')

@conjugation
def declarative_present_formal_high(infinitive):
    return merge(base(infinitive), '습니다')

@conjugation
def past_base(infinitive):
    ps = declarative_present_informal_low(infinitive)
    if vowel(ps[-1]) in ['ㅗ', 'ㅏ']:
        return ps[:-1] + merge(ps[-1], '았')
    else:
        return ps[:-1] + merge(ps[-1], '었')

@conjugation
def declarative_past_informal_low(infinitive):
    return merge(past_base(infinitive), '어')

@conjugation
def declarative_past_informal_high(infinitive):
    return merge(declarative_past_informal_low(infinitive), '요')

@conjugation
def declarative_past_formal_low(infinitive):
    return merge(past_base(infinitive), '다')

@conjugation
def declarative_past_formal_high(infinitive):
    return merge(past_base(infinitive), '습니다')

@conjugation
def future_base(infinitive):
    return merge(base2(infinitive), '을')

@conjugation
def declarative_future_informal_low(infinitive):
    return merge(future_base(infinitive), ' 거야')

@conjugation
def declarative_future_informal_high(infinitive):
    return merge(future_base(infinitive), ' 거예요')

@conjugation
def declarative_future_formal_low(infinitive):
    return merge(future_base(infinitive), ' 거다')

@conjugation
def declarative_future_formal_high(infinitive):
    return merge(future_base(infinitive), ' 겁니다')

@conjugation
def declarative_future_conditional_informal_low(infinitive):
    return merge(base(infinitive), '겠어')

@conjugation
def declarative_future_conditional_informal_high(infinitive):
    return merge(base(infinitive), '겠어요')

@conjugation
def declarative_future_conditional_formal_low(infinitive):
    return merge(base(infinitive), '겠다')

@conjugation
def declarative_future_conditional_formal_high(infinitive):
    return merge(base(infinitive), '겠습니다')

@conjugation
def inquisitive_present_informal_low(infinitive):
    return merge(base(infinitive), '?')

@conjugation
def inquisitive_present_informal_high(infinitive):
    return declarative_present_informal_high(infinitive) + '?'

@conjugation
def inquisitive_present_formal_low(infinitive):
    return merge(base(infinitive), '니?')

@conjugation
def inquisitive_present_formal_high(infinitive):
    return merge(base(infinitive), '읍니까?')

@conjugation
def imperative_present_informal_low(infinitive):
    return declarative_present_informal_low(infinitive)

@conjugation
def imperative_present_informal_high(infinitive):
    return merge(base2(infinitive), '세요')

@conjugation
def imperative_present_formal_low(infinitive):
    return merge(imperative_present_informal_low(infinitive), '라')

@conjugation
def imperative_present_formal_high(infinitive):
    return merge(base2(infinitive), '십시오')

@conjugation
def connective_if(infinitive):
    return merge(base2(infinitive), '면')

assert merge('오', '아요') == '와요'
assert merge('오', '아') == '와'
assert merge('갔', '면') == '갔으면'
assert merge('일어나', '면') == '일어나면'
assert merge('맡', '세요') == '맡으세요'

assert connective_if('낫') == '나으면'
assert connective_if('짓') == '지으면'
assert connective_if('짖') == '짖으면'
assert connective_if('가') == '가면'

assert declarative_present_informal_low('하') == '해'
assert declarative_present_informal_low('가') == '가'
assert declarative_present_informal_low('오') == '와'
assert declarative_present_informal_low('피우') == '피워'
assert declarative_present_informal_low('듣') == '들어'
assert declarative_present_informal_low('춥') == '추워'
assert declarative_present_informal_low('낫') == '나아'
assert declarative_present_informal_low('알') == '알아'
assert declarative_present_informal_low('기다리') == '기다려'
assert declarative_present_informal_low('마르') == '말라'
assert declarative_present_informal_low('부르다') == '불러'
assert declarative_present_informal_low('되') == '돼'
assert declarative_present_informal_low('쓰') == '써'
assert declarative_present_informal_low('서') == '서'
assert declarative_present_informal_low('세') == '세'
assert declarative_present_informal_low('기다리다') == '기다려'
assert declarative_present_informal_low('굽다') == '구워'
assert declarative_present_informal_low('걷다') == '걸어'
assert declarative_present_informal_low('짓다') == '지어'
assert declarative_present_informal_low('웃다') == '웃어'
assert declarative_present_informal_low('걸다') == '걸어'
assert declarative_present_informal_low('깨닫다') == '깨달아'
assert declarative_present_informal_low('남다') == '남아'
assert declarative_present_informal_low('오르다') == '올라'

assert declarative_present_informal_high('가다') == '가요'

assert declarative_present_formal_low('가다') == '간다'
assert declarative_present_formal_low('믿다') == '믿는다'
assert declarative_present_formal_low('걷다') == '걷는다'
assert declarative_present_formal_low('짓다') == '짓는다'
assert declarative_present_formal_low('부르다') == '부른다'
assert declarative_present_formal_low('살다') == '산다'
assert declarative_present_formal_low('오르다') == '오른다'

assert declarative_present_formal_high('가다') == '갑니다'
assert declarative_present_formal_high('믿다') == '믿습니다'
print(declarative_present_formal_high('걸다'))
assert declarative_present_formal_high('걸다') == '겁니다'
assert declarative_present_formal_high('깨닫다') == '깨닫습니다'

assert past_base('하') == '했'
assert past_base('가') == '갔'
assert past_base('기다리') == '기다렸'
assert past_base('기다리다') == '기다렸'
assert past_base('마르다') == '말랐'
assert past_base('드르다') == '들렀'

assert declarative_past_informal_low('하') == '했어'
assert declarative_past_informal_low('가') == '갔어'
assert declarative_past_informal_low('먹') == '먹었어'

assert declarative_past_informal_high('하다') == '했어요'
assert declarative_past_informal_high('가다') == '갔어요'

assert declarative_past_formal_low('가다') == '갔다'

assert declarative_past_formal_high('가다') == '갔습니다'

assert declarative_future_informal_low('가다') == '갈 거야'
assert declarative_future_informal_low('믿다') == '믿을 거야'

assert declarative_future_informal_high('가다') == '갈 거예요'
assert declarative_future_informal_high('믿다') == '믿을 거예요'
assert declarative_future_informal_high('걷다') == '걸을 거예요'

assert declarative_future_formal_low('가다') == '갈 거다'
assert declarative_future_formal_low('앉다') == '앉을 거다'

assert declarative_future_formal_high('가다') == '갈 겁니다'
assert declarative_future_formal_high('앉다') == '앉을 겁니다'

assert declarative_future_conditional_informal_low('가다') == '가겠어'

assert declarative_future_conditional_informal_high('가다') == '가겠어요'

assert declarative_future_conditional_formal_low('가다') == '가겠다'

assert declarative_future_conditional_formal_high('가다') == '가겠습니다'

assert inquisitive_present_informal_low('가다') == '가?'

assert inquisitive_present_informal_high('가다') == '가요?'

assert inquisitive_present_formal_low('가다') == '가니?'

assert inquisitive_present_formal_high('가다') == '갑니까?'

assert imperative_present_informal_low('가다') == '가'

assert imperative_present_informal_high('가다') == '가세요'
assert imperative_present_informal_high('돕다') == '도우세요'
assert imperative_present_informal_high('걷다') == '걸으세요'
assert imperative_present_informal_high('눕다') == '누우세요'

assert imperative_present_formal_low('가다') == '가라'
assert imperative_present_formal_low('굽다') == '구워라'
assert imperative_present_formal_low('살다') == '살아라'
assert imperative_present_formal_low('서') == '서라'

assert imperative_present_formal_high('가다') == '가십시오'
assert imperative_present_formal_high('돕다') == '도우십시오'

#print(pformat(list(conjugation.tenses.keys())))

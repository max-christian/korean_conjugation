from functools import reduce, partial
from pprint import pformat

def join(lead, vowel, padchim=None):
    lead_offset = ord(lead) - ord('ᄀ')
    vowel_offset = ord(vowel) - ord('ㅏ')
    if padchim:
        padchim_offset = ord(padchim) - ord('ᆨ')
    else:
        padchim_offset = -1
    return chr(padchim_offset + (vowel_offset) * 28 + (lead_offset) * 588 + 44032 + 1)

assert join('ᄀ', 'ㅏ') == '가'
assert join('ᄆ', 'ㅕ', 'ᆫ') == '면'
assert join('ᄈ', 'ㅙ', 'ᆶ') == '뾇'

def lead(character):
    return chr(int((ord(character) - 44032) / 588) + 4352)

assert lead('가') == 'ᄀ'
assert lead('만') == 'ᄆ'
assert lead('짉') == 'ᄌ'

def vowel(character):
    padchim_character = padchim(character)
    if not padchim_character:
        padchim_offset = -1
    else:
        padchim_offset = ord(padchim_character) - ord('ᆨ')
    return chr(int(((ord(character) - 44032 - padchim_offset) % 588) / 28) + ord('ㅏ'))

def padchim(character):
    p = chr(((ord(character) - 44032) % 28) + ord('ᆨ') - 1)
    if ord(p) == 4519:
        return None
    else:
        return p

assert vowel('갓') == 'ㅏ'
assert vowel('빩') == 'ㅏ'
assert vowel('법') == 'ㅓ'
assert vowel('가') == 'ㅏ'

def match(character, l, v, p=''):
    return all([lead(character) == l or l is None, vowel(character) == v or v is None, padchim(character) == p or p is ''])

assert match('아', None, 'ㅏ') == True
assert match('왅', None, 'ㅏ') == False
assert match('아', 'ᄋ', 'ㅏ') == True
assert match('아', 'ᄋ', 'ㅏ', None) == True
assert match('읽', None, None, 'ᆰ') == True
assert match('읽', None, None, None) == False

merge_rules = []
# ㄷ irregular
merge_rules.append(lambda x, y: padchim(x[-1]) == 'ᆮ' and lead(y[0]) == 'ᄋ' and join(lead(x[-1]), vowel(x[-1]), 'ᆯ') + y)
# ㅂ irregular
merge_rules.append(lambda x, y: padchim(x[-1]) == 'ᆸ' and y[0] == '어' and join(lead(x[-1]), vowel(x[-1])) + '워' + y[1:])
# ㅅ irregular
merge_rules.append(lambda x, y: padchim(x[-1]) == 'ᆺ' and y[0] == '아' and join(lead(x[-1]), vowel(x[-1])) + '아' + y[1:])
# 면 connective
merge_rules.append(lambda x, y: padchim(x[-1]) == 'ᆺ' and y[0] == '면' and join(lead(x[-1]), vowel(x[-1])) + '으' + y)
merge_rules.append(lambda x, y: padchim(x[-1]) is not None and y[0] == '면' and x + '으면' + y[1:])
# vowel contractions
def vowel_contraction(vowel1, vowel2, new_vowel):
    def rule(x, y):
        return match(x[-1], None, vowel1, None) and match(y[0], 'ᄋ', vowel2) and x[:-1] + join(lead(x[-1]), new_vowel, padchim(y[0])) + y[1:]
    return rule
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
merge_rules.append(lambda x, y: x + y)

def apply_rules(x, y, verbose=False, rules=[]):
    for i, rule in enumerate(rules):
        output = rule(x, y)
        if output:
            if verbose:
                print("rule %03d: %s, %s => %s" % (i, pformat(x), pformat(y), pformat(output)))
            return output

def present_simple(infinitive):
    if infinitive[-1] == '다':
        infinitive = infinitive[:-1]
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

def past_simple(infinitive):
    ps = present_simple(infinitive)
    if vowel(ps[-1]) in ['ㅗ', 'ㅏ']:
        return ps[:-1] + merge(ps[-1], '았')
    else:
        return ps[:-1] + merge(ps[-1], '었')

merge = partial(apply_rules, rules=merge_rules, verbose=True)
assert merge('오', '아요') == '와요'
assert merge('오', '아') == '와'
assert merge('갔', '면') == '갔으면'
assert merge('가', '면') == '가면'
assert merge('일어나', '면') == '일어나면'
assert merge('낫', '면') == '나으면'
assert merge('짓', '면') == '지으면'
assert merge('짖', '면') == '짖으면'
assert merge('맡', '세요') == '맡으세요'

assert present_simple('하') == '해'
assert present_simple('가') == '가'
assert present_simple('오') == '와'
assert present_simple('피우') == '피워'
assert present_simple('듣') == '들어'
assert present_simple('춥') == '추워'
assert present_simple('낫') == '나아'
assert present_simple('알') == '알아'
assert present_simple('기다리') == '기다려'
assert present_simple('마르') == '말라'
assert present_simple('되') == '돼'
assert present_simple('쓰') == '써'
assert present_simple('서') == '서'
assert present_simple('세') == '세'
assert present_simple('기다리다') == '기다려'

assert past_simple('하') == '했'
assert past_simple('가') == '갔'
assert past_simple('기다리') == '기다렸'
assert past_simple('기다리다') == '기다렸'
assert past_simple('마르다') == '말랐'
assert past_simple('드르다') == '들렀'



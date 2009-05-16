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

merge_rules = []
# ㄷ irregular
merge_rules.append(lambda x, y: padchim(x[-1]) == 'ᆮ' and lead(y[0]) == 'ᄋ' and join(lead(x[-1]), vowel(x[-1]), 'ᆯ') + y)
# ㅂ irregular
merge_rules.append(lambda x, y: padchim(x[-1]) == 'ᆸ' and y[0] == '어' and join(lead(x[-1]), vowel(x[-1])) + '워' + y[1:])
# ㅅ irregular
merge_rules.append(lambda x, y: padchim(x[-1]) == 'ᆺ' and y[0] == '아' and join(lead(x[-1]), vowel(x[-1])) + '아' + y[1:])
merge_rules.append(lambda x, y: vowel(x[-1]) == 'ㅏ' and padchim(x[-1]) is None and y[0] == '아' and x[-1] + y[1:])
merge_rules.append(lambda x, y: x[-1] == '오' and y[0] == '아' and x[:-1] + '와' + y[1:])
merge_rules.append(lambda x, y: x[-1] == '우' and y[0] == '어' and x[:-1] + '워' + y[1:])
merge_rules.append(lambda x, y: padchim(x[-1]) == 'ᆺ' and y[0] == '면' and join(lead(x[-1]), vowel(x[-1])) + '으면' + y[1:])
merge_rules.append(lambda x, y: padchim(x[-1]) is not None and y[0] == '면' and x + '으면' + y[1:])
merge_rules.append(lambda x, y: x + y)

def apply_rules(x, y, verbose=False, rules=[]):
    for i, rule in enumerate(rules):
        output = rule(x, y)
        if output:
            if verbose:
                print("rule %d: %s, %s => %s" % (i, pformat(x), pformat(y), pformat(output)))
            return output

def present_simple(infinitive):
    if vowel(infinitive[-1]) in ['ㅗ', 'ㅏ']:
        return infinitive[:-1] + merge(infinitive[-1], '아')
    else:
        return infinitive[:-1] + merge(infinitive[-1], '어')


def conjugate(tense, verb_stem):
    if verb_stem[-1] == '다':
        verb_stem = verb_stem[:-1]
    return conjugate_rules[tense](verb_stem)

merge = partial(apply_rules, rules=merge_rules, verbose=True)
assert reduce(merge, ['오', '아요']) == '와요'
assert reduce(merge, ['오', '아']) == '와'
assert reduce(merge, ['갔', '면']) == '갔으면'
assert reduce(merge, ['가', '면']) == '가면'
assert reduce(merge, ['일어나', '면']) == '일어나면'
assert reduce(merge, iter('낫면')) == '나으면'
assert reduce(merge, iter('짓면')) == '지으면'
assert reduce(merge, iter('짖면')) == '짖으면'

assert present_simple('가') == '가'
assert present_simple('오') == '와'
assert present_simple('피우') == '피워'
assert present_simple('듣') == '들어'
assert present_simple('춥') == '추워'
assert present_simple('낫') == '나아'

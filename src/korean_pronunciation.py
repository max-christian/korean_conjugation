# -*- coding: utf-8 -*-

# (C) 2009 Dan Bravender

from hangeul_utils import join, lead, vowel, padchim

def consonant_combination_rule(x_padchim=u'*', y_lead=u'*', 
                               new_padchim=u'*', new_lead=u'*',
                               y_vowel=None):
    def rule(x, y):
        if y_vowel and vowel(y[0]) != y_vowel:
            return
        if (padchim(x[-1]) == x_padchim or x_padchim == u'*') and \
           (lead(y[0]) == y_lead or y_lead == u'*'):
            return x[:-1] + join(lead(x[-1]),
                                 vowel(x[-1]), 
                                 new_padchim == u'*' and padchim(x[-1]) or new_padchim) + \
                            join(new_lead == u'*' and lead(y[0]) or new_lead,
                                 vowel(y[0]),
                                 padchim(y[0])) + \
                   y[1:]
    return rule

# WARNING: Please be careful when adding/modifying rules since padchim 
#          and lead characters are different Unicode characters. Please see:
#          http://www.kfunigraz.ac.at/~katzer/korean_hangul_unicode.html


# Rules from http://en.wikibooks.org/wiki/Korean/Advanced_Pronunciation_Rules

# merge rules is a list of rules that are applied in order when merging 
#             pronunciation rules
merge_rules = []

# ㄱㄴ becomes ㅇㄴ
merge_rules.append(consonant_combination_rule(u'ᆨ', u'ᄂ', u'ᆼ', u'ᄂ'))
# ㄱㅁ becomes ㅇㅁ
merge_rules.append(consonant_combination_rule(u'ᆨ', u'ᄆ', u'ᆼ', u'ᄆ'))
# ㅋㄴ becomes ㅇㄴ
merge_rules.append(consonant_combination_rule(u'ᆿ', u'ᄂ', u'ᆼ', u'ᄂ'))
# ㅋㅁ becomes ㅇㅁ
merge_rules.append(consonant_combination_rule(u'ᆿ', u'ᄆ', u'ᆼ', u'ᄆ'))
# ㄷㄴ becomes ㄴㄴ
merge_rules.append(consonant_combination_rule(u'ᆮ', u'ᄂ', u'ᆫ', u'ᄂ'))
# ㄷㅁ becomes ㄴㅁ
merge_rules.append(consonant_combination_rule(u'ᆮ', u'ᄆ', u'ᆫ', u'ᄆ'))
# ㅅㄴ becomes ㄴㄴ
merge_rules.append(consonant_combination_rule(u'ᆺ', u'ᄂ', u'ᆫ', u'ᄂ'))
# ㅆㄴ becomes ㄴㄴ
merge_rules.append(consonant_combination_rule(u'ᆻ', u'ᄂ', u'ᆫ', u'ᄂ'))
# ㅅㅁ becomes ㄴㅁ
merge_rules.append(consonant_combination_rule(u'ᆺ', u'ᄆ', u'ᆫ', u'ᄆ'))
# ㄱ ㅆ becomes ㄱ ㅆ
merge_rules.append(consonant_combination_rule(u'ᆨ', u'ᄉ', u'ᆨ', u'ᄊ'))
# ㅈㄴ becomes ㄴㄴ
merge_rules.append(consonant_combination_rule(u'ᆽ', u'ᄂ', u'ᆫ', u'ᄂ'))
#ㅈㅁ becomes ㄴㅁ
merge_rules.append(consonant_combination_rule(u'ᆽ', u'ᄆ', u'ᆫ', u'ᄆ'))
#ㅊㄴ becomes ㄴㄴ
merge_rules.append(consonant_combination_rule(u'ᆾ', u'ᄂ', u'ᆫ', u'ᄂ'))
#ㅊㅁ becomes ㄴㅁ
merge_rules.append(consonant_combination_rule(u'ᆾ', u'ᄆ', u'ᆫ', u'ᄆ'))
#ㅌㄴ becomes ㄴㄴ
merge_rules.append(consonant_combination_rule(u'ᇀ', u'ᄂ', u'ᆫ', u'ᄂ'))
#ㅌㅁ becomes ㄴㅁ
merge_rules.append(consonant_combination_rule(u'ᇀ', u'ᄆ', u'ᆫ', u'ᄆ'))
# ㅎㄴ becomes ㄴㄴ
merge_rules.append(consonant_combination_rule(u'ᇂ', u'ᄂ', u'ᆫ', u'ᄂ'))
# ㅎㅁ becomes ㄴㅁ
merge_rules.append(consonant_combination_rule(u'ᇂ', u'ᄆ', u'ᆫ', u'ᄆ'))
# ㅂㄴ becomes ㅁㄴ
merge_rules.append(consonant_combination_rule(u'ᆸ', u'ᄂ', u'ᆷ', u'ᄂ'))
#ㅂㅁ becomes ㅁㅁ
merge_rules.append(consonant_combination_rule(u'ᆸ', u'ᄆ', u'ᆷ', u'ᄆ'))
#ㅍㄴ becomes ㅁㄴ
merge_rules.append(consonant_combination_rule(u'ᇁ', u'ᄂ', u'ᆷ', u'ᄂ'))
#ㅍㅁ becomes ㅁㅁ
merge_rules.append(consonant_combination_rule(u'ᇁ', u'ᄆ', u'ᆷ', u'ᄆ'))
# ㄱㅎ becomes ㅋ
merge_rules.append(consonant_combination_rule(u'ᆨ', u'ᄒ', None, u'ᄏ'))
# ㅎㄱ becomes ㅋ
merge_rules.append(consonant_combination_rule(u'ᇂ', u'ᄀ', None, u'ᄏ'))
# ㅎㄷ becomes ㅌ
merge_rules.append(consonant_combination_rule(u'ᇂ', u'ᄃ', None, u'ᄐ'))
# ㄷㅎ becomes ㅌ
merge_rules.append(consonant_combination_rule(u'ᆮ', u'ᄒ', None, u'ᄐ'))
# ㅂㅎ becomes ㅍ
merge_rules.append(consonant_combination_rule(u'ᆸ', u'ᄒ', None, u'ᄑ'))
# ㅎㅂ becomes ㅍ
merge_rules.append(consonant_combination_rule(u'ᇂ', u'ᄇ', None, u'ᄑ'))
# ㅈㅎ becomes ㅊ
merge_rules.append(consonant_combination_rule(u'ᆽ', u'ᄒ', None, u'ᄎ'))
# ㅎㅈ becomes ㅊ
merge_rules.append(consonant_combination_rule(u'ᇂ', u'ᄌ', None, u'ᄎ'))
# ㅎㅅ becomes ㅆ
merge_rules.append(consonant_combination_rule(u'ᇂ', u'ᄉ', None, u'ᄊ'))
#ㄷ이 becomes 지
merge_rules.append(consonant_combination_rule(u'ᆮ', u'ᄋ', None, u'ᄌ',
                                              y_vowel=u'ㅣ'))
#ㅌ이 becomes 치
merge_rules.append(consonant_combination_rule(u'ᇀ', u'ᄋ', None, u'ᄎ', 
                                              y_vowel=u'ㅣ'))
#ㄱㄹ becomes ㅇㄴ
merge_rules.append(consonant_combination_rule(u'ᆨ', u'ᄅ', u'ᆼ', u'ᄂ'))
#ㄴㄹ becomes ㄹㄹ // TODO: (not sure how to fix this) also sometimes ㄴㄴ
merge_rules.append(consonant_combination_rule(u'ᆫ', u'ᄅ', u'ᆯ', u'ᄅ'))
# ㅁㄹ becomes ㅁㄴ
merge_rules.append(consonant_combination_rule(u'ᆷ', u'ᄅ', u'ᆷ', u'ᄂ'))
# ㅇㄹ becomes ㅇㄴ
merge_rules.append(consonant_combination_rule(u'ᆼ', u'ᄅ', u'ᆼ', u'ᄂ'))
# ㅂㄹ becomes ㅁㄴ
merge_rules.append(consonant_combination_rule(u'ᆸ', u'ᄅ', u'ᆷ', u'ᄂ'))

# 받침 followed by ㅇ: replace ㅇ with 받침 (use second 받침 if there are two). Otherwise, 받침 followed by consonant:

#    * ㄱ, ㅋ: like ㄱ
merge_rules.append(consonant_combination_rule(u'ᆸ', u'ᄅ', u'ᆷ', u'ᄂ'))
#    * ㄴ: like ㄴ
#    * ㄷ, ㅅ, ㅈ, ㅊ, ㅌ, ㅎ: like ㄷ
#    * ㄹ: like /l/
#    * ㅁ: like ㅁ
#    * ㅂ, ㅍ: like ㅂ
#    * ㅇ: like /ng/

# Double padchim rules
merge_rules.append(consonant_combination_rule(u'ᆱ', u'ᄋ', u'ᆯ', u'ᄆ'))
merge_rules.append(consonant_combination_rule(u'ᆱ', u'*', u'ᆷ', u'*'))

merge_rules.append(consonant_combination_rule(u'ᆶ', u'*', None, u'ᄅ'))

merge_rules.append(consonant_combination_rule(u'ᆬ', u'ᄋ', u'ᆫ', u'ᄌ'))
merge_rules.append(consonant_combination_rule(u'ᆬ', u'*', u'ᆫ', u'*'))


merge_rules.append(lambda x, y: x + y)

def apply_rules(x, y):
    u'''apply_rules concatenates every element in a list using the rules to 
        merge the strings
     '''
    for i, rule in enumerate(merge_rules):
        result = rule(x, y)
        if result:
            return result

def pronunciation(word):
    return reduce(apply_rules, iter(word))
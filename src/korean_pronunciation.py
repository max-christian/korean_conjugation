# -*- coding: utf-8 -*-

# (C) 2009 Dan Bravender

from hangeul_utils import join, lead, vowel, padchim, find_vowel_to_append, match

def consonant_combination_rule(x_padchim, y_lead, 
                               new_padchim, new_lead):
    def rule(x, y):
        if padchim(x[-1]) == x_padchim and \
           lead(y[0])     == y_lead:
            return x[:-1] + join(lead(x[-1]),
                                 vowel(x[-1]), 
                                 new_padchim) + \
                            join(new_lead,
                                 vowel(y[0]),
                                 padchim(y[0])) + \
                   y[1:]
    return rule

# Rules borrowed from http://en.wikibooks.org/wiki/Korean/Advanced_Pronunciation_Rules

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
# ex) 젖니 (baby tooth), pronounced [전니]
#ㅈㅁ becomes ㄴㅁ
# 낮말, pronounced (난말)
#ㅊㄴ becomes ㄴㄴ
# 옻나무 (lacquer tree), pronounced [온나무]
#ㅊㅁ becomes ㄴㅁ
#옻물 (lacquer sap), pronounced (온물)
#ㅌㄴ becomes ㄴㄴ
#ㅌㅁ becomes ㄴㅁ
# 낱말 (a word), pronounced (난말)
# ㅎㄴ becomes ㄴㄴ
# 놓는 (putting down, participle form), pronounced (논는)
# ㅎㅁ becomes ㄴㅁ
# ㅂㄴ becomes ㅁㄴ
# 굽는 (roasting, participle form), pronounced (굼는)
#ㅂㅁ becomes ㅁㅁ
#업무 (duties), pronounced (엄무)
#ㅍㄴ becomes ㅁㄴ
#엎는 (flipping, participle form), pronounced (엄는)
#ㅍㅁ becomes ㅁㅁ
# ㄱㅎ becomes ㅋ
# 북한 (North Korea), pronounced (부칸)
# ㅎㄱ becomes ㅋ
# ㅎㄷ becomes ㅌ
# ㄷㅎ becomes ㅌ
# ㅂㅎ becomes ㅍ
# ㅎㅂ becomes ㅍ
# ㅈㅎ becomes ㅊ
# ㅎㅈ becomes ㅊ
# ㅎㅅ becomes ㅆ
#ㄷ이 becomes 지
#ㅌ이 becomes 치
#ㄱㄹ becomes ㅇㄴ
#ㄴㄹ becomes ㄹㄹ // uh oh-> // or sometimes ㄴㄴ
# ㅁㄹ becomes ㅁㄴ
# ㅇㄹ becomes ㅇㄴ
# ㅂㄹ becomes ㅁㄴ

# 받침 followed by ㅇ: replace ㅇ with 받침 (use second 받침 if there are two). Otherwise, 받침 followed by consonant:

#    * ㄱ, ㅋ: like ㄱ
#    * ㄴ: like ㄴ
#    * ㄷ, ㅅ, ㅈ, ㅊ, ㅌ, ㅎ: like ㄷ
#    * ㄹ: like /l/
#    * ㅁ: like ㅁ
#    * ㅂ, ㅍ: like ㅂ
#    * ㅇ: like /ng/

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

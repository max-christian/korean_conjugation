# -*- coding: utf-8 -*-

from korean.hangeul import *
from qc import forall, characters

@forall(character=characters(minunicode=ord(u'가'), maxunicode=ord(u'힣')))
def test_is_hanguel(character):
    assert is_hangeul(character)

@forall(character=characters(minunicode=ord(u'힣') + 1, maxunicode=65535))
def test_is_not_hangeul_greater(character):
    assert not is_hangeul(character)

@forall(character=characters(minunicode=0, maxunicode=ord(u'가') + 1))
def test_is_not_hangeul_lower(character):
    assert not is_hangeul(character)

def test_find_vowel_to_append():
    assert find_vowel_to_append(u'아프') == u'아'
    assert find_vowel_to_append(u'흐르') == u'어'
    assert find_vowel_to_append(u'태우') == u'어'
    assert find_vowel_to_append(u'만들') == u'어'
    assert find_vowel_to_append(u'앗') == u'아'

def test_join():
    assert join(u'ᄀ', u'ㅏ') == u'가'
    assert join(u'ᄆ', u'ㅕ', u'ᆫ') == u'면'
    assert join(u'ᄈ', u'ㅙ', u'ᆶ') == u'뾇'

@forall(character=characters(minunicode=ord(u'가'), maxunicode=ord(u'힣')))
def test_join_randomly(character):
    assert join(lead(character), vowel(character), padchim(character)) == character

def test_lead():
    assert lead(u'가') == u'ᄀ'
    assert lead(u'만') == u'ᄆ'
    assert lead(u'짉') == u'ᄌ'

def test_vowel():
    assert vowel(u'갓') == u'ㅏ'
    assert vowel(u'빩') == u'ㅏ'
    assert vowel(u'법') == u'ㅓ'
    assert vowel(u'가') == u'ㅏ'

def test_match():
    assert match(u'아', u'*', u'ㅏ') == True
    assert match(u'왅', u'*', u'ㅏ') == False
    assert match(u'아', u'ᄋ', u'ㅏ') == True
    assert match(u'아', u'ᄋ', u'ㅏ', None) == True
    assert match(u'읽', u'*', u'*', u'ᆰ') == True
    assert match(u'읽', u'*', u'*', None) == False
    
    infinitive = Geulja(u'나')
    infinitive.hidden_padchim = True
    assert match(infinitive, u'*', u'*', None) == False

    infinitive = Geulja(u'나')
    infinitive.hidden_padchim = False
    assert match(infinitive, u'*', u'*', None) == True

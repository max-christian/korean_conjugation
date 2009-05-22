# -*- coding: utf-8 -*-

from hangeul_utils import *

def test_find_vowel_to_append():
    assert find_vowel_to_append(u'아프') == u'아'
    assert find_vowel_to_append(u'흐르') == u'어'
    assert find_vowel_to_append(u'태우') == u'어'
    assert find_vowel_to_append(u'만들') == u'어'

def test_join():
    assert join(u'ᄀ', u'ㅏ') == u'가'
    assert join(u'ᄆ', u'ㅕ', u'ᆫ') == u'면'
    assert join(u'ᄈ', u'ㅙ', u'ᆶ') == u'뾇'

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

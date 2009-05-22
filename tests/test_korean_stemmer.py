# -*- coding: utf-8 -*-

# (C) 2009 Dan Bravender

from korean_stemmer import *

def test_iterate_chop_last():
    assert list(iterate_chop_last('fred')) == ['f', 'fr', 'fre', 'fred']
    assert list(iterate_chop_last(u'안녕')) == [u'안', u'안녕']

def test_stem():
    assert stem(u'가') == u'가다'
    assert stem(u'가요') == u'가다'
    assert stem(u'가요') == u'가다'
    assert stem(u'가세요') == u'가다'
    assert stem(u'기다려') == u'기다리다'
    assert stem(u'기다렸어') == u'기다리다'
    assert stem(u'저었어') == u'젓다'
    assert stem(u'가셨습니까?') == u'가시다'
    assert stem(u'안녕하세요') == u'안녕하다'
    assert stem(u'추워요') == u'춥다'
    assert stem(u'지어') == u'짓다'
    assert stem(u'도와') == u'돕다'
    assert stem(u'더워') == u'덥다'
    assert stem(u'갑니까?') == u'갈다'
    assert stem(u'삶') == u'살다'
    assert stem(u'걸음') == u'걷다'

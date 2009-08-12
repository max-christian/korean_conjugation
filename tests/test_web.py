# -*- coding: utf-8 -*-

from korean.web import index

def test_web():
    root = index.Root()
    assert u'하다' in root.index().decode('utf-8')

def test_json():
    root = index.Root()
    assert u'해요' in root.index(json=True).decode('utf-8')

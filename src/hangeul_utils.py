# -*- coding: utf-8 -*-

#from functools import reduce, partial

class Geulja(unicode):
    u'''Geulja is used to track modifications that have been made to characters. Currently, it keeps track
       of characters original padchims (for ㄷ -> ㄹ irregulars) and if the character has no padchim but
       should be treated as if it does (for ㅅ irregulars). When substrings are extracted the Geulja class 
       keeps these markers for the last character only.'''
    hidden_padchim = False
    original_padchim = None
    
    def __getitem__(self, index):
        g = Geulja(unicode.__getitem__(self, index))
        # only keep the hidden padchim marker for the last item
        if index == -1:
            g.hidden_padchim = self.hidden_padchim
            g.original_padchim = self.original_padchim
        return g

def join(lead, vowel, padchim=None):
    lead_offset = ord(lead) - ord(u'ᄀ')
    vowel_offset = ord(vowel) - ord(u'ㅏ')
    if padchim:
        padchim_offset = ord(padchim) - ord(u'ᆨ')
    else:
        padchim_offset = -1
    return unichr(padchim_offset + (vowel_offset) * 28 + (lead_offset) * 588 + 44032 + 1)

assert join(u'ᄀ', u'ㅏ') == u'가'
assert join(u'ᄆ', u'ㅕ', u'ᆫ') == u'면'
assert join(u'ᄈ', u'ㅙ', u'ᆶ') == u'뾇'

def lead(character):
    return unichr(int((ord(character) - 44032) / 588) + 4352)

assert lead(u'가') == u'ᄀ'
assert lead(u'만') == u'ᄆ'
assert lead(u'짉') == u'ᄌ'

def vowel(character):
    padchim_character = padchim(character)
    # padchim returns a character or True if there is a hidden padchim, but a hidden padchim doesn't make sense for this offset
    if not padchim_character or padchim_character == True:
        padchim_offset = -1
    else:
        padchim_offset = ord(padchim_character) - ord(u'ᆨ')
    return unichr(int(((ord(character) - 44032 - padchim_offset) % 588) / 28) + ord(u'ㅏ'))

def padchim(character):
    if getattr(character, u'hidden_padchim', False):
        return True
    if getattr(character, u'original_padchim', False):
        return character.original_padchim
    p = unichr(((ord(character) - 44032) % 28) + ord(u'ᆨ') - 1)
    if ord(p) == 4519:
        return None
    else:
        return p

assert vowel(u'갓') == u'ㅏ'
assert vowel(u'빩') == u'ㅏ'
assert vowel(u'법') == u'ㅓ'
assert vowel(u'가') == u'ㅏ'

def match(character, l='*', v='*', p='*'):
    return (lead(character) == l or l == u'*') and (vowel(character) == v or v == u'*') and (padchim(character) == p or p == u'*')

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

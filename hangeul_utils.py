from functools import reduce, partial

class Geulja(str):
    '''Geulja is used to pass around strings that don't have a padchim but should be treated as if they do.
       When substrings are extracted the Geulja class keeps this marker for the last character only.'''
    hidden_padchim = False
    
    def __getitem__(self, index):
        g = Geulja(str.__getitem__(self, index))
        # only keep the hidden padchim marker for the last item
        if index == -1:
            g.hidden_padchim = self.hidden_padchim
        return g

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
    # padchim returns a character or True if there is a hidden padchim, but a hidden padchim doesn't make sense for this offset
    if not padchim_character or padchim_character == True:
        padchim_offset = -1
    else:
        padchim_offset = ord(padchim_character) - ord('ᆨ')
    return chr(int(((ord(character) - 44032 - padchim_offset) % 588) / 28) + ord('ㅏ'))

def padchim(character):
    if getattr(character, 'hidden_padchim', False):
        return True
    p = chr(((ord(character) - 44032) % 28) + ord('ᆨ') - 1)
    if ord(p) == 4519:
        return None
    else:
        return p

assert vowel('갓') == 'ㅏ'
assert vowel('빩') == 'ㅏ'
assert vowel('법') == 'ㅓ'
assert vowel('가') == 'ㅏ'

def match(character, l='*', v='*', p='*'):
    return all([lead(character) == l or l == '*', vowel(character) == v or v == '*', padchim(character) == p or p == '*'])

assert match('아', '*', 'ㅏ') == True
assert match('왅', '*', 'ㅏ') == False
assert match('아', 'ᄋ', 'ㅏ') == True
assert match('아', 'ᄋ', 'ㅏ', None) == True
assert match('읽', '*', '*', 'ᆰ') == True
assert match('읽', '*', '*', None) == False

infinitive = Geulja('나')
infinitive.hidden_padchim = True
assert match(infinitive, '*', '*', None) == False

infinitive = Geulja('나')
infinitive.hidden_padchim = False
assert match(infinitive, '*', '*', None) == True
